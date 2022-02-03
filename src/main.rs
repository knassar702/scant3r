use std::collections::HashMap;
mod requests;
mod args;

fn main() {
    let arg = args::args();
    match arg.subcommand_name() {
         Some("scan") => {
             let _msg = requests::Msg::new("GET",arg.subcommand_matches("scan").unwrap().value_of("url").unwrap(),HashMap::new(),None,None,None);
             #[path = "scan/xss.rs"]
             mod xss;
             xss::scan(_msg);
        },
        _ => println!("No subcommand was used"),
    };
}
