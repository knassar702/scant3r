use clap::{App, Arg, ArgMatches};

pub fn args() -> ArgMatches {
    App::new("scant3r")
        .version("0.9.0")
        .author("Khaled Nassar <knassar702@gmail.com>")
        .about("A Web Application Scanner")
        .subcommands(vec![
            App::new("scan")
                .about("Scan a website")
                .arg(
                    Arg::with_name("url")
                        .help("The URL to scan")
                        .required(true)
                        .long("url")
                        .short('u')
                        .takes_value(true)
                )
                .arg( 
                    Arg::with_name("urls")
                        .help("The URLs to scan")
                        .required(false)
                        .long("urls")
                        .short('U')
                        .takes_value(true)
                    )
                .arg(
                    Arg::with_name("threads")
                        .help("The number of threads to use")
                        .required(false)
                        .long("threads")
                        .short('t')
                        .default_value("10")
                        .takes_value(true)
                )

                .arg(
                    Arg::with_name("timeout")
                        .help("The timeout in seconds")
                        .required(false)
                        .long("timeout")
                        .short('o')
                        .default_value("10")
                        .takes_value(true)
                )

                .arg(
                    Arg::with_name("output")
                        .help("The output file")
                        .required(false)
                        .long("output")
                        .short('o')
                        .default_value("output.json")
                        .takes_value(true)
                )

                .arg(
                    Arg::with_name("verbose")
                        .help("Verbose output")
                        .required(false)
                        .long("verbose")
                        .short('v')
                )

                .arg(
                    Arg::with_name("debug")
                        .help("Debug output")
                        .required(false)
                        .long("debug")
                        .short('d')
                ),
            App::new("list")
                .about("List all the scanned websites")
                .arg(
                    Arg::with_name("url")
                        .help("The URL to scan")
                        .required(false)
                        .index(1),
                ),

            App::new("report")
                .about("Generate a report")
                .arg(
                    Arg::with_name("url")
                        .help("The URL to scan")
                        .required(true)
                        .index(1),
                )
        ])

        .get_matches()
}
