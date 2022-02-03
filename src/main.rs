mod requests;
mod args;
mod zap;

fn main() {
    /*
    let arg = args::args();


    match arg.subcommand_name() {
        Some("scan") => {
            let subcommand = arg.subcommand_matches("scan").unwrap();
            let url = subcommand.value_of("url").unwrap();
            println!("{}", url
            );

        },
        Some("report") => {
            let subcommand = arg.subcommand_matches("report").unwrap();
            let url = subcommand.value_of("url").unwrap();
            println!("{}", url
            );

        },
        _ => println!("No subcommand was used"),

    }*/

    #[cfg(feature = "webapi")]
    {
        #[path = "api.rs"]
        mod api;
        api::main();
    }
}
