extern crate scant3r_utils;
use clap::{Arg, ArgMatches, Command};

pub fn args() -> ArgMatches {
    Command::new("scant3r")
        .version("0.9.0")
        .author("Khaled Nassar <knassar702@gmail.com>")
        .about("A Web Application Scanner")
        .subcommands(vec![
            Command::new("scan")
                .about("Scan a website")
                .arg(
                    Arg::new("modules")
                        .help("The modules to use")
                        .long("modules")
                        .validator(|module| {
                            if module.contains(" ") {
                                Err("Modules must be separated by a space")
                            } else {
                                Ok(())
                            }
                        })
                        .possible_values(&["xss"])
                        .takes_value(true),
                )
                .arg(
                    Arg::new("delay")
                        .help("The delay between requests")
                        .long("delay")
                        .validator(|delay| {
                            if delay.parse::<u64>().is_err() {
                                Err("Delay must be a number")
                            } else {
                                Ok(())
                            }
                        })
                        .takes_value(true),
                )
                // arg for data option
                .arg(
                    Arg::new("data")
                        .help("The data to send")
                        .long("data")
                        .short('d')
                        .default_value("")
                        .takes_value(true),
                )
                // arg for headers option
                .arg(
                    Arg::new("headers")
                        .help("The headers to send")
                        .long("headers")
                        .short('R')
                        .default_value("")
                        .multiple_occurrences(true)
                        .takes_value(true),
                )
                .arg(
                    Arg::new("content-type")
                        .help("The content type of the data")
                        .long("content-type")
                        .default_value("application/x-www-form-urlencoded")
                        .possible_values(&["application/x-www-form-urlencoded", "application/json"])
                        .takes_value(true),
                )
                // arg for http method options
                // HEADERS AND COOKIES AND METHOD
                .arg(
                    Arg::new("method")
                        .help("The HTTP method to use")
                        .long("method")
                        .takes_value(true)
                        .default_value("GET"),
                )
                // arg for concurrency option
                .arg(
                    Arg::new("concurrency")
                        .help("The number of concurrent requests to make (default: 10)")
                        .long("concurrency")
                        .short('c')
                        .default_value("10")
                        .validator(|s| {
                            if s.parse::<usize>().is_ok() {
                                Ok(s.parse::<usize>().unwrap())
                            } else {
                                Err("Concurrency must be a number".to_string())
                            }
                        })
                        .takes_value(true),
                )
                .arg(
                    Arg::new("urls")
                        .help("The file containing the URLs to scan")
                        .long("urls")
                        .validator(|s| {
                            if std::path::Path::new(s).exists() {
                                Ok(())
                            } else {
                                Err("File does not exist".to_string())
                            }
                        })
                        .required(true)
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
                        .default_value("")
                        .takes_value(true),
                )
                .arg(
                    Arg::new("location")
                        .help("The location to inject the payload (headers or urls or body)")
                        .long("location")
                        .default_value("url")
                        .possible_values(&["headers", "url", "body"])
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
                                Ok(10)
                            } else {
                                Err("Timeout must be a number".to_string())
                            }
                        })
                        .default_value("20"),
                )
                .arg(
                    // -m xss,headers
                    Arg::new("mode")
                        .help("The mode to use")
                        .long("mode")
                        .short('m')
                        .takes_value(true)
                        .multiple_values(true)
                        .possible_values(&["xss", "headers", "cookies"])
                        .default_value("xss"),
                ),
            Command::new("api")
                .about("Scan a website using the API")
                .arg(
                    Arg::new("host")
                        .help("The host to bind")
                        .long("host")
                        .takes_value(true)
                        .default_value("localhost"),
                )
                .arg(
                    Arg::new("port")
                        .help("The port to bind")
                        .long("port")
                        .takes_value(true)
                        .default_value("1338"),
                ),
            Command::new("pipe")
                .about("Scan a website passively")
                .arg(
                    Arg::new("timeout")
                        .help("The timeout in seconds")
                        .long("timeout")
                        .short('t')
                        .takes_value(true)
                        .validator(|s| {
                            if s.parse::<u64>().is_ok() {
                                Ok(10)
                            } else {
                                Err("Timeout must be a number".to_string())
                            }
                        })
                        .default_value("20"),
                )
                .arg(
                    Arg::new("redirect")
                        .help("The Number of redirects to follow")
                        .long("redirect")
                        .short('r')
                        .validator(|s| {
                            if s.parse::<u8>().is_ok() {
                                Ok(0)
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
                        .validator(|s| {
                            if s.parse::<url::Url>().is_ok() {
                                Ok(())
                            } else {
                                Err("Proxy must be in the format host:port".to_string())
                            }
                        })
                        .takes_value(true),
                )
                .arg(
                    Arg::new("modules")
                        .help("The modules to use")
                        .long("modules")
                        .takes_value(true)
                        .multiple_values(true)
                        .possible_values(&[
                            "headers", "links", "forms", "cookies", "sitemap", "xss",
                        ]),
                ),
        ])
        .get_matches()
}
