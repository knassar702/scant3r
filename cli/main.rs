extern crate scanners;
extern crate scant3r_utils;
extern crate simplelog;
use simplelog::*;

use scanners::scan;
use scant3r_utils::{
    extract_headers_vec,
    requests::{Msg, Settings},
};
use std::fs::read_to_string;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
mod args;

#[tokio::main]
async fn main() {
    CombinedLogger::init(vec![TermLogger::new(
        LevelFilter::Warn,
        Config::default(),
        TerminalMode::Mixed,
        ColorChoice::Auto,
    )])
    .unwrap();

    let arg = args::args();
    match arg.subcommand_name() {
        Some("urls") => {
            let sub = arg.subcommand_matches("urls").unwrap();
            let urls = {
                let read_file = File::open(sub.value_of("file").unwrap()).unwrap();
                BufReader::new(read_file)
                    .lines()
                    .map(|x| x.unwrap())
                    .collect::<Vec<String>>()
            };

            let config_file = read_to_string(sub.value_of("config").unwrap()).unwrap();
            let header = extract_headers_vec(
                sub.values_of("headers")
                    .unwrap()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>(),
            );
            let mut reqs: Vec<Msg> = Vec::new();
            urls.iter().for_each(|url| {
                let mut live_check = Msg::new()
                    .method(sub.value_of("method").unwrap().to_string())
                    .url(url.to_string())
                    .headers(header.clone())
                    .body(sub.value_of("data").unwrap_or("").to_string())
                    .url(url.to_string())
                    .delay(sub.value_of("delay").unwrap_or("0").parse::<u64>().unwrap());
                if sub.value_of("proxy").is_some() {
                    live_check.proxy(sub.value_of("proxy").unwrap().to_string());
                }
                reqs.push(live_check.clone());
            });
            drop(urls);
            let mut scan_settings =
                scan::Scanner::new(vec!["xss".to_string()], reqs, sub.is_present("keep-value"));
            scan_settings.load_config(&config_file);
            scan_settings
                .scan(
                    sub.value_of("concurrency")
                        .unwrap()
                        .parse::<usize>()
                        .unwrap(),
                )
                .await;
        }
        _ => println!("No subcommand was used"),
    }
}
