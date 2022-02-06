use std::collections::HashMap;
use futures::{stream, StreamExt};
use rand::{thread_rng, Rng};
use indicatif::ProgressBar;

#[path = "scan/xss.rs"]
mod xss;
mod args;
mod requests;
mod payloads;
mod zap;



#[tokio::main]
async fn main() {
    let mut c = zap::api::Zap::new("http://localhost:8080".to_string(),Some("9rn5nkfjqen8tvt433vda3ccjj".to_string()));
    c.childNode();
    let mut _bar = ProgressBar::new(1000);
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
            let sub = arg.subcommand_matches("scan").unwrap();
            stream::iter(vec![sub.value_of("url").unwrap()])
                .for_each_concurrent(sub.value_of("concurrency").unwrap().parse::<usize>().unwrap(), |url| async move {
                    for module in sub.value_of("modules").unwrap().split(",") {
                        let _msg = requests::Msg::new(
                            "GET",
                            url,
                            HashMap::new(),
                            None,
                            Some(sub.value_of("redirect").unwrap().parse::<u32>().unwrap()),
                            Some(sub.value_of("timeout").unwrap().parse::<u64>().unwrap()),
                            Some(sub.value_of("proxy").unwrap().to_string()),
                        );
                        match module {
                            "xss" => {
                                xss::scan(_msg);

                            }
                            _ => {
                                println!("{} module not found", module);
                            }
                        };
                    }
                        })
                    .await;
            _bar.finish();
        }
        Some("passive") => {
            let sub = arg.subcommand_matches("passive").unwrap();
            for module in sub.value_of("modules").unwrap().split(",") {
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

