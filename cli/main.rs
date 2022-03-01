#[macro_use] extern crate log;
extern crate scant3r_utils;
extern crate scanners;
use futures::{stream, StreamExt};
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use indicatif::{ProgressStyle,ProgressBar};
use scant3r_utils::{
    requests::{
        Msg,
        Settings
    },
    extract_headers
};
use scanners::scan;
mod args;


#[tokio::main]
async fn main() {

    let arg = args::args();
    match arg.subcommand_name() {

        Some("scan") => {

            let sub = arg.subcommand_matches("scan").unwrap();

            // read urls file
            let urls = {
                let read_file = File::open(sub.value_of("urls").unwrap()).unwrap();
                BufReader::new(read_file).lines().map(|x| x.unwrap()).collect::<Vec<String>>()
            };

            let bar = ProgressBar::new(urls.len() as u64);
            // setup the scanner module
            let mut scan_settings = scan::Scanner::new(vec!["xss"],true,false);
            scan_settings.load_payloads();

            let header = sub.value_of("headers").map(|x| {
                                extract_headers(x.to_string())
            }).unwrap();

            bar.set_style(ProgressStyle::default_bar()
                .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos:>7}/{len:7} {msg}")
                .tick_chars("⠁⠂⠄⡀⢀⠠⠐⠈ ")
                .progress_chars("#>-"));

            stream::iter(&urls)

                .for_each_concurrent(sub.value_of("concurrency").unwrap().parse::<usize>().unwrap(), |url| {

                    let bar = &bar;
                    let scan_settings = &scan_settings;
                    let header = &header;

                    async move {

                        let mut live_check = Msg::new()
                            .method(sub.value_of("method")
                                    .unwrap()
                                    .to_string())
                            .url(url.clone())
                            .headers(header.clone())
                            .body(sub.value_of("data")
                                  .unwrap_or("")
                                  .to_string())
                            .url(url.clone())
                            .delay(sub.value_of("delay")
                                   .unwrap_or("0")
                                   .parse::<u64>()
                                   .unwrap());
                        if sub.value_of("proxy").is_some() {
                                live_check.proxy(sub.value_of("proxy")
                                                 .unwrap()
                                                 .to_string());
                        }

                        live_check.send().await;

                        if live_check.clone().error.unwrap_or(String::from("")) != "" {
                            error!("{}", live_check.clone().error.unwrap());

                        } else {
                            scan_settings.scan(live_check.clone(),&bar).await;
                        }

                        bar.inc(1);
                }
            }).await;

            bar.finish();
        }
        _ => println!("No subcommand was used"),
    }
}

