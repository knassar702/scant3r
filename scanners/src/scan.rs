extern crate scant3r_utils;
use futures::{stream, StreamExt};
use home::home_dir;
use indicatif::{ProgressBar, ProgressStyle};
use scant3r_utils::requests::Msg;
use std::io::prelude::*;

mod xss;
use xss::{XssPayloads, XssUrlParamsValue};

const BLOCKING_HEADERS: [&str; 10] = [
    "application/json",
    "application/javascript",
    "text/javascript",
    "text/plain",
    "text/css",
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/gif",
    "application/rss+xml",
];

pub enum Payloads {
    XSS(XssPayloads),
}

pub struct Scanner {
    pub modules: Vec<String>,
    pub payloads: Vec<Payloads>,
    pub requests: Vec<Msg>,
    pub keep_value: bool,
}

impl Scanner {
    pub fn new(modules: Vec<String>, requests: Vec<Msg>, keep_value: bool) -> Scanner {
        Scanner {
            modules,
            payloads: Vec::new(),
            requests,
            keep_value,
        }
    }

    pub fn load_config(&mut self) {
        // load ~/.scant3r/config.yml file and extract payloads from it
        let config_path = home_dir().unwrap().join(".scant3r").join("config.yaml");
        let mut config_file = std::fs::File::open(config_path).unwrap();
        let mut config_yaml = String::new();
        self.modules.iter().for_each(|module| {
            self.payloads.push(Payloads::XSS(XssPayloads {
                    js_cmd: vec!["alert".to_string()],
                    js_value: vec![module.to_string()],
                    attr: vec!["onerror".to_string()],
                    html_tags: vec![
                    "\"><img src=x onerror=$JS_FUNC$`$JS_CMD$`>"
                    .to_string(),
                    ]}));
        });
        config_file.read_to_string(&mut config_yaml).unwrap();
        
    }
    pub async fn scan(&self, concurrency: usize) {
        let bar = ProgressBar::new(self.requests.len() as u64);
        bar.set_style(ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos:>7}/{len:7} {msg}")
            .tick_chars("//—\\\r")
            .progress_chars("#>-"));
        stream::iter(&self.requests)
            .for_each_concurrent(concurrency, |request| {
                let modules = &self.modules;
                let request = request;
                let pb = &bar;
                async move {
                    for module in modules.clone() {
                        let module = module.as_str();
                        match module {
                            "xss" => {
                                let mut blocking_headers = false;
                                let resp = match request.send().await {
                                    Ok(resp) => resp,
                                    Err(_) => {
                                        pb.inc(1);
                                        return;
                                    }
                                };

                                BLOCKING_HEADERS.iter().for_each(|header| {
                                    if resp.headers.contains_key("Content-Type") {
                                        if resp.headers.get("Content-Type").unwrap() == header {
                                            blocking_headers = true;
                                        }
                                    } else {
                                        blocking_headers = true;
                                    }
                                });

                                if !blocking_headers {
                                    for payload in self.payloads.iter(){
                                        match payload {
                                            Payloads::XSS(current_payload) => {

                                                let xss_scan = xss::Xss::new(
                                                    request,
                                                    current_payload,
                                                    self.keep_value,
                                                );
                                                let _value = xss_scan.value_scan(pb).await;
                                            }
                                        }
                                    }
                                }
                                pb.inc(1);
                            }
                            _ => {
                                panic!("Module not found");
                            }
                        }
                    }
                }
            })
            .await;
    }
}
