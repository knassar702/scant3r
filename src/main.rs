use std::collections::HashMap;
use futures::{stream, StreamExt};
use indicatif::{ProgressBar, ProgressStyle};

#[path = "scan/xss.rs"]
mod xss;
mod args;
mod requests;


#[tokio::main]
async fn main() {
    let bar = ProgressBar::new(151);
    bar.set_style(ProgressStyle::default_bar()
            .template("[{elapsed_precise}] {bar:40.cyan/blue} {pos:>7}/{len:7} {msg}")
            .progress_chars("#>-"));
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
//            let sub = arg.subcommand_matches("scan").unwrap();
            let urls = vec![
                "http://testphp.vulnweb.com/listproducts.php?cat=1",
                "http://testphp.vulnweb.com/artists.php?artist=1",
                "http://192.168.1.2:5000/search?u="
            ];
            stream::iter(urls)
                .for_each_concurrent(50, |job| {
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
                        println!("{}", job);
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

