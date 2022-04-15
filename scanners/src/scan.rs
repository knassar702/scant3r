extern crate scant3r_utils;
use std::fs::read_to_string;
use futures::{stream, StreamExt};
use indicatif::{ProgressBar, ProgressStyle};
use scant3r_utils::requests::Msg;
use yaml_rust::{YamlLoader,ScanError};

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

#[derive(Debug)]
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

    pub fn load_config(&mut self, config_yaml: &str) {
        match YamlLoader::load_from_str(config_yaml) {
            Ok(config) => {
                match &config[0]["modules"].as_hash() {
                    Some(module) => {
                        module.iter().for_each(|(key,value)|{
                            match key.as_str().unwrap() {
                                "xss" => {
                                    let html_tags: Vec<String>;
                                    let jsfunc: Vec<String>;
                                    let jsvalue: Vec<String>;
                                    let attr: Vec<String>;

                                    if value["tags"].as_vec().is_some() {
                                        html_tags = {
                                            let mut tags = Vec::new();
                                            value["tags"].as_vec().unwrap().iter().map(|x| x.as_str().unwrap().to_string()).collect::<Vec<String>>().iter().for_each(|paylods_file| {
                                                let file = read_to_string(paylods_file).unwrap();
                                                for line in file.lines() {
                                                    tags.push(line.to_string());
                                                }
                                            });
                                            tags
                                        };
                                    } else {
                                        html_tags = vec!["<img src=x onerror=$JS_FUNC$`$JS_CMD$`>".to_string(),"<svg/%JS_FUNC%=%JS_VALUE%>".to_string()];
                                    }
                                    if value["jsfunc"].as_vec().is_some(){
                                        jsfunc = {
                                            let mut func = Vec::new();
                                            value["jsfunc"].as_vec().unwrap().iter().map(|x| x.as_str().unwrap().to_string()).collect::<Vec<String>>().iter().for_each(|paylods_file| {
                                                let file = read_to_string(paylods_file).unwrap();
                                                for line in file.lines() {
                                                    func.push(line.to_string());
                                                }
                                            });
                                            func
                                        };
                                    } else {
                                        jsfunc = vec!["alert".to_string()];
                                    }

                                    if value["jsvalue"].as_vec().is_some() {
                                        jsvalue = {
                                            let mut value_vec = Vec::new();
                                            value["jsvalue"].as_vec().unwrap().iter().map(|x| x.as_str().unwrap().to_string()).collect::<Vec<String>>().iter().for_each(|paylods_file| {
                                                let file = read_to_string(paylods_file).unwrap();
                                                for line in file.lines() {
                                                    value_vec.push(line.to_string());
                                                }
                                            });
                                            value_vec
                                        };
                                    } else {
                                        jsvalue = vec!["134".to_string()];
                                    }

                                    if value["attr"].as_vec().is_some() {
                                        attr = {
                                            let mut attr_vec = Vec::new();
                                            value["attr"].as_vec().unwrap().iter().map(|x| x.as_str().unwrap().to_string()).collect::<Vec<String>>().iter().for_each(|paylods_file| {
                                                let file = read_to_string(paylods_file).unwrap();
                                                for line in file.lines() {
                                                    attr_vec.push(line.to_string());
                                                }
                                            });
                                            attr_vec
                                        };

                                    } else {
                                        attr = vec!["onerror".to_string()];
                                    }
                                    self.payloads.push(Payloads::XSS(XssPayloads {
                                            js_cmd: jsfunc,
                                            js_value: jsvalue,
                                            attr: attr,
                                            html_tags: html_tags
                                    }));

                                },
                                _ => {
                                    println!("244")
                                }
                            }
                        });
                    },
                    None => {
                    },
                };

            },
            Err(e) => {
                println!("{}", e);
            }
        };
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
