extern crate scant3r_utils;
use clap::{Arg, ArgMatches, Command};

pub fn args() -> ArgMatches {
    Command::new("scant3r")
        .version("0.9.0")
        .author("Khaled Nassar <knassar702@gmail.com>")
        .about("A Web Application Scanner")
        .subcommands(vec![
            Command::new("urls")
                .about("Scan a website")
                .arg(
                    Arg::new("config")
                        .help("Path to the configuration file")
                    )

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
                    Arg::new("keep-value")
                        .help("Keep the value of the parameter")
                        .long("keep-value")
                        .takes_value(false),
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
                .arg(
                    Arg::new("data")
                        .help("The data to send")
                        .long("data")
                        .short('d')
                        .default_value("")
                        .takes_value(true),
                )
                .arg(
                    Arg::new("headers")
                        .help("The headers to send")
                        .long("headers")
                        .short('H')
                        .default_value("")
                        .multiple_occurrences(true)
                        .takes_value(true),
                )

                .arg(
                    Arg::new("method")
                        .help("The HTTP method to use")
                        .long("method")
                        .takes_value(true)
                        .default_value("GET"),
                )
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
                    Arg::new("file")
                        .help("The file containing the URLs to scan")
                        .long("file")
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
        ])
        .get_matches()
}
