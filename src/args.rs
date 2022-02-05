use clap::{App, Arg, ArgMatches};

pub fn args() -> ArgMatches {
    App::new("scant3r")
        .version("0.9.0")
        .author("Khaled Nassar <knassar702@gmail.com>")
        .about("A Web Application Scanner")
        .arg(
            // arg for upload option
            Arg::new("upload")
                .long("upload")
                .value_name("FILE")
                .help("Upload a file to the server")
                .takes_value(true),
            )
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
                // validate is it a number  or not
                Arg::new("redirect")
                    .help("The Number of redirects to follow")
                    .long("redirect")
                    .short('r')
                    .validator(|s| {
                        if s.parse::<u8>().is_ok() {
                            Ok(())
                        } else {
                            Err("Redirects must be a number".to_string())
                        }
                    })
                    .takes_value(true),
            )
            .arg(
                Arg::new("proxy")
                    .help("The proxy to use")
                    .long("proxy")
                    .short('p')
                    .takes_value(true))

            .arg(
                Arg::new("timeout")
                    .help("The timeout in seconds")
                    .long("timeout")
                    .short('t')
                    .takes_value(true)
                    .validator(|s| {
                        if s.parse::<u64>().is_ok() {
                            Ok(())
                        } else {
                            Err("Timeout must be a number".to_string())
                        }
                    })
                    .default_value("20"),
            )
            .arg(
                Arg::new("modules")
                    .help("The modules to use")
                    .long("modules")
                    .short('m')
                    .takes_value(true)
                    .possible_values(&["headers", "links", "forms", "cookies", "sitemap", "xss"]),
            ),
            App::new("passive")
                .about("Scan a website passively")
                .arg(
                    Arg::new("url")
                        .help("The URL to scan")
                        .required(true)
                        .long("url")
                        .short('u')
                        .takes_value(true),
                )

                .arg(
                    Arg::new("timeout")
                        .help("The timeout in seconds")
                        .long("timeout")
                        .short('t')
                        .takes_value(true)
                        .validator(|s| {
                            if s.parse::<u64>().is_ok() {
                                Ok(())
                            } else {
                                Err("Timeout must be a number".to_string())
                            }
                        })
                        .default_value("20"),
                )

                .arg(Arg::new("redirect")
                    .help("The Number of redirects to follow")
                    .long("redirect")
                    .short('r')
                    .default_value("0")
                    .validator(|s| {
                        if s.parse::<u8>().is_ok() {
                            Ok(())
                        } else {
                            Err("Redirects must be a number".to_string())
                        }
                    })
                    .takes_value(true),
                )
                .arg(
                    Arg::new("proxy")
                        .help("The proxy to use")
                        .long("proxy")
                        .short('p')
                        .takes_value(true))
                .arg(
                    Arg::new("modules")
                        .help("The modules to use")
                        .long("modules")
                        .short('m')
                        .takes_value(true)
                        .default_value("xss")
                        .possible_values(&["headers", "links", "forms", "cookies", "sitemap", "xss"]),
                )
    ])
        .get_matches()
}
