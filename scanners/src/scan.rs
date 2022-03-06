extern crate scant3r_utils;
use indicatif::{ProgressStyle,ProgressBar};
use scant3r_utils::requests::Msg;
use futures::{stream, StreamExt};
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use home::home_dir;

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
		"application/rss+xml"];

#[derive(Debug, Clone)]
pub struct Scanner {
    pub modules: Vec<&'static str>,
    pub payloads: HashMap<String,Vec<String>>,
    pub requests: Vec<Msg>,
}



impl Scanner {
    pub fn new(modules: Vec<&'static str>,requests: Vec<Msg>) -> Scanner {
        Scanner {
            modules,
            payloads: HashMap::new(),
            requests,
        }
    }

    pub fn load_payloads(&mut self) {
        let scant3r_dir = home_dir().unwrap().join(".scant3r/");
        for module in self.modules.clone() {
                let dir = scant3r_dir.join(&format!("{}.txt",&module))
                    .to_str()
                    .unwrap()
                    .to_string();

                if Path::new(&dir).exists() {

                        let mut payload_file = std::fs::File::open(&dir).unwrap();
                        let mut payload_string = String::new();
                        payload_file.read_to_string(&mut payload_string).unwrap();
                        let payloads: Vec<&str> = payload_string
                            .split("\n")
                            .collect();

                        self.payloads.insert(String::from("xss"), payloads.iter()
                                             .map(|x| x.to_string())
                                             .collect());

                } else {

                    let module_location = self.modules
                        .iter()
                        .position(|x| *x == module)
                        .unwrap();
                    self.modules.remove(module_location);
                    }
            }
    }
    pub async fn scan(&self,concurrency: usize) {
        if self.payloads.len() == 0 {
            panic!("No payloads loaded");
        }
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
                                let resp = request.send().await.unwrap();
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
                                    let xss_scan = xss::Xss::new(request);
                                    let _value = xss_scan.value_scan(self.payloads.get("xss").unwrap().clone(),pb).await;
                                }
                                pb.inc(1);
                            },
                           _ => {
                                panic!("Module not found");
                            }
                        }
                    }
                }
            }).await;
    }
}

