extern crate scanners;
extern crate scant3r_utils;
extern crate simplelog;
use simplelog::*;

use scanners::scan;
use scant3r_utils::{
    extract_headers_vec,
    requests::{Msg, Settings},
};
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
    //  func::execute_lua("scripting/scripts/hello.lua");
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
            let sub = arg.subcommand_matches("scan").unwrap();
            let urls = {
                let read_file = File::open(sub.value_of("urls").unwrap()).unwrap();
                BufReader::new(read_file)
                    .lines()
                    .map(|x| x.unwrap())
                    .collect::<Vec<String>>()
            };

            // setup the scanner module
            let mut reqs = Vec::new();
            let header = extract_headers_vec(
                sub.values_of("headers")
                    .unwrap()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>(),
            );
            urls.iter().for_each(|url| {
                let mut live_check = Msg::new()
                    .method(sub.value_of("method").unwrap().to_string())
                    .url(url.clone())
                    .headers(header.clone())
                    .body(sub.value_of("data").unwrap_or("").to_string())
                    .url(url.clone())
                    .delay(sub.value_of("delay").unwrap_or("0").parse::<u64>().unwrap());
                if sub.value_of("proxy").is_some() {
                    live_check.proxy(sub.value_of("proxy").unwrap().to_string());
                }
                reqs.push(live_check.clone());
            });
            drop(urls);
            let scan_settings =
                scan::Scanner::new(vec!["xss"], reqs, sub.is_present("keep-value"));
            scan_settings.load_config();
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
