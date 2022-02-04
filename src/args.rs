use clap::{App, Arg, ArgMatches};

pub fn args() -> ArgMatches {
    App::new("scant3r")
        .version("0.9.0")
        .author("Khaled Nassar <knassar702@gmail.com>")
        .about("A Web Application Scanner")
        .subcommands(vec![App::new("scan")
            .about("Scan a website")
            .arg(
                Arg::new("url")
                    .help("The URL to scan")
                    .required(true)
                    .long("url")
                    .short('u')
                    .takes_value(true),
            )
            .arg(
                Arg::new("redirect")
                    .help("The Number of redirects to follow")
                    .long("redirect")
                    .short('r')
                    .takes_value(true),
            )
            .arg(
                Arg::new("timeout")
                    .help("The timeout in seconds")
                    .long("timeout")
                    .short('t')
                    .takes_value(true)
                    .default_value("20"),
            )
            .arg(
                Arg::new("modules")
                    .help("The modules to use")
                    .long("modules")
                    .short('m')
                    .takes_value(true)
                    .possible_values(&["headers", "links", "forms", "cookies", "sitemap", "xss"]),
            )])
        .get_matches()
}
