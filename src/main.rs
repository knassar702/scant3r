use std::collections::HashMap;
#[path = "scan/xss.rs"]
mod xss;
mod args;
mod requests;

#[tokio::main]
async fn main() {
    let arg = args::args();
    match arg.subcommand_name() {
        Some("scan") => {
            let sub = arg.subcommand_matches("scan").unwrap();
            for module in sub.value_of("modules").unwrap().split(",") {
                let _msg = requests::Msg::new(
                    "GET",
                    sub.value_of("url").unwrap(),
                    HashMap::new(),
                    None,
                    Some(sub.value_of("redirect").unwrap().parse::<u32>().unwrap()),
                    Some(sub.value_of("timeout").unwrap().parse::<u64>().unwrap()),
                    None,
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
        }
        _ => println!("No subcommand was used"),
    };
}
