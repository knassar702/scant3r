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
                    Arg::new("url")
                        .help("The URL to scan")
                        .required(true)
                        .long("url")
                        .short('u')
                        .takes_value(true)
                )
                .arg(
                    Arg::new("redirect")
                        .help("The Number of redirects to follow")
                        .long("redirect")
                        .short('r')
                        .takes_value(true)
                )

                .arg(
                    Arg::new("threads")
                        .help("The Number of threads to use")
                        .long("threads")
                        .short('t')
                        .takes_value(true)
                )


                .arg(
                    Arg::new("verbose")
                        .help("Verbose output")
                        .long("verbose")
                        .short('v')
                )

        ])

        .get_matches()
}
