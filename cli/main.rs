extern crate scant3r_utils;
extern crate scanners;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use std::collections::HashMap;
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

            // setup the scanner module
            let mut reqs = Vec::new();

            let header = sub.value_of("headers").map(|x| {
                                extract_headers(x.to_string())
            }).unwrap_or(HashMap::new());

            urls.iter().for_each(|url| {
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
                reqs.push(live_check.clone());
            });
            let mut scan_settings = scan::Scanner::new(vec!["xss"], reqs);
            scan_settings.load_payloads();
            scan_settings.scan(sub.value_of("concurrency").unwrap().parse::<usize>().unwrap()).await;
        }
        _ => println!("No subcommand was used"),
    }
}

