use std::collections::HashMap;
use futures::{stream, StreamExt, AsyncReadExt};
use indicatif::{ProgressBar, ProgressStyle};
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
    let bar = ProgressBar::new(2000);
    let name = "Khaled";
    bar.set_style(ProgressStyle::default_bar()
            .template("[{elapsed_precise}] {bar:40.cyan/blue} {pos:>7}/{len:7} {msg}")
            .progress_chars("#>-"));
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
            let sub = arg.subcommand_matches("scan").unwrap();
            let file = File::open(sub.value_of("urls").unwrap()).unwrap();
            let urls = BufReader::new(file).lines().map(|x| x.unwrap()).collect::<Vec<String>>();
            stream::iter(&urls)
                .for_each_concurrent(100, |job| {
                    let bar = bar.clone();
                    async move {
                        let _msg = requests::Msg::new(
                            "GET",
                            job,
                            HashMap::new(),
                            None,
                            Some(1_u32),
                            Some(10_u64),
                            Some("http://localhost:8080".parse().unwrap())
                        );
                        xss::scan(_msg).await;
                        bar.inc(1);
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

