extern crate scant3r_utils;
extern crate yaml_rust;
use futures::{stream, StreamExt};
use home::home_dir;
use indicatif::{ProgressBar, ProgressStyle};
use scant3r_utils::requests::Msg;
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use yaml_rust::{Yaml, YamlLoader};

mod xss;
use xss::XssUrlParamsValue;

// create a Const with a list of blocking headers
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

#[derive(Debug, Clone)]
pub struct Scanner {
    pub modules: Vec<&'static str>,
    pub payloads: HashMap<String, Vec<String>>,
    pub requests: Vec<Msg>,
    pub keep_value: bool,
}

impl Scanner {
    pub fn new(modules: Vec<&'static str>, requests: Vec<Msg>,keep_value: bool) -> Scanner {
        Scanner {
            modules,
            payloads: HashMap::new(),
            requests,
            keep_value,
        }
    }

    pub fn loader(&self) -> HashMap<String, String> {
        let mut payloads = HashMap::new();
        // load ~/.scant3r/config.yaml file
        let config_file = home_dir().unwrap().join(".scant3r").join("config.yaml");
        if config_file.exists() {
            let mut file = std::fs::File::open(config_file).unwrap();
            let mut contents = String::new();
            file.read_to_string(&mut contents).unwrap();
            let docs = YamlLoader::load_from_str(&contents).unwrap();
            // extract files value
            // modules:
            //   xss:
            //     files:
            //        html_tags: ~/scant3r/txt
            let x = &docs[0]["modules"]["xss"]["files"];
            let v = x.as_hash().unwrap();
            v.iter().for_each(|(k, v)| {
                // read v file content
                let mut fiile = std::fs::File::open(v.as_str().unwrap()).unwrap();
            });
        }
        payloads
    }
    pub fn load_payloads(&mut self) {
        let scant3r_dir = home_dir().unwrap().join(".scant3r/");
        for module in self.modules.clone() {
            let dir = scant3r_dir
                .join(&format!("{}.txt", &module))
                .to_str()
                .unwrap()
                .to_string();

            if Path::new(&dir).exists() {
                let mut payload_file = std::fs::File::open(&dir).unwrap();
                let mut payload_string = String::new();
                payload_file.read_to_string(&mut payload_string).unwrap();
                let payloads: Vec<&str> = payload_string.split("\n").collect();

                self.payloads.insert(
                    String::from("xss"),
                    payloads.iter().map(|x| x.to_string()).collect(),
                );
            } else {
                let module_location = self.modules.iter().position(|x| *x == module).unwrap();
                self.modules.remove(module_location);
            }
        }
    }

    pub async fn scan(&self, concurrency: usize) {
        if self.payloads.len() == 0 {
            panic!("No payloads loaded");
        }
        //self.loader();
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
                                    let xss_scan = xss::Xss::new(request,self.keep_value);
                                    let _value = xss_scan
                                        .value_scan(pb)
                                        .await;
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
