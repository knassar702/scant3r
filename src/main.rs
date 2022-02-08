#[macro_use] extern crate log;
extern crate simplelog;
use simplelog::*;
use std::collections::HashMap;
use futures::{stream, StreamExt, AsyncReadExt};
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

#[path = "scan/xss.rs"]
mod xss;
mod scan;
mod args;
mod requests;

#[tokio::main]
async fn main() {
     CombinedLogger::init(
        vec![
            TermLogger::new(LevelFilter::Warn, Config::default(), TerminalMode::Mixed, ColorChoice::Auto),
            WriteLogger::new(LevelFilter::Info, Config::default(), File::create("my_rust_binary.log").unwrap()),
        ]
    ).unwrap();
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
            let sub = arg.subcommand_matches("scan").unwrap();
            let file = File::open(sub.value_of("urls").unwrap()).unwrap();
            let urls = BufReader::new(file).lines().map(|x| x.unwrap()).collect::<Vec<String>>();
            let bar_style = logbar::Style::default()
                    .width(80) // 80 characters wide
                    .labels(false) // no XX% labels
                    .tick('↓').bar('-') // rendered as ↓---↓---↓ etc.
                    .indicator('V'); // indicating the progress with '█' characters
            let bar = logbar::ProgressBar::with_style(urls.len() as usize,bar_style);
            let mut scan_settings = scan::Scanner::new(vec!["xss"]);
            scan_settings.load_payloads();
            stream::iter(&urls)
                .for_each_concurrent(100, |url| {
                    let bar = &bar;
                    let mut scan_settings = scan_settings.clone();
                    async move {
                        let _msg = requests::Msg::new(
                            "GET",
                            &url,
                            HashMap::new(),
                            None,
                            Some(1_u32),
                            Some(10_u64),
                            Some("http://localhost:8080".parse().unwrap())
                        );
                        bar.inc(1);
                        xss::scan(_msg, scan_settings.payloads.get("xss").unwrap()).await;
                }
                }).await;
        }
        Some("passive") => {
            let sub = arg.subcommand_matches("passive").unwrap();
            for _ in sub.value_of("modules").unwrap().split(",") {
                let _msg = requests::Msg::new(
                    "GET",
                    sub.value_of("url").unwrap(),
                    HashMap::new(),
                    None,
                    Some(sub.value_of("redirect").unwrap_or("0").parse::<u32>().unwrap()),
                    Some(sub.value_of("timeout").unwrap_or("10").parse::<u64>().unwrap()),
                    None,
                );
            }
        },
        _ => println!("No subcommand was used"),
    }
}

