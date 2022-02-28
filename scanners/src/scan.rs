extern crate scant3r_utils;
use indicatif::ProgressBar;
use scant3r_utils::requests::Msg;
#[ path = "./xss.rs"] mod xss;
use xss::{
    XssUrlParamsValue,
    XssUrlParamsName
};
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use home::home_dir;


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
pub struct Scanner{
    pub modules: Vec<&'static str>,
    pub payloads: HashMap<String,Vec<String>>,
    pub inject_body: bool,
    pub inject_query: bool,
}


impl Scanner {
    pub fn new(modules: Vec<&'static str>,inject_query: bool, inject_body: bool) -> Scanner {
        Scanner {
            modules,
            payloads: HashMap::new(),
            inject_body,
            inject_query,
        }
    }

    pub fn load_payloads(&mut self) {
        let scant3r_dir = home_dir().unwrap().join(".scant3r/");
        for module in self.modules.clone() {
                let dir = scant3r_dir.join(&format!("{}.txt",&module)).to_str().unwrap().to_string();
                if Path::new(&dir).exists() {

                        let mut payload_file = std::fs::File::open(&dir).unwrap();
                        let mut payload_string = String::new();
                        payload_file.read_to_string(&mut payload_string).unwrap();
                        let payloads: Vec<&str> = payload_string.split("\n").collect();
                        self.payloads.insert(String::from("xss"), payloads.iter().map(|x| x.to_string()).collect());

                } else {

                    let module_location = self.modules
                        .iter()
                        .position(|x| *x == module)
                        .unwrap();
                    self.modules.remove(module_location);
                    }
            }
    }
    pub async fn scan(&self,request: Msg,_prog: &ProgressBar){
        if self.payloads.len() == 0 {
            panic!("No payloads loaded");
        }

        for module in self.modules.clone() {

            match module {

                "xss" => {

                    let mut blocking_headers = false;
                    for header in BLOCKING_HEADERS.iter() {
                        if request.response_headers.as_ref().unwrap().contains_key("Content-Type") {
                            if request.response_headers.as_ref().unwrap().get("Content-Type").unwrap() == header {
                                blocking_headers = true;
                            }
                        } else {
                            blocking_headers = true;
                        }
                    }

                    if !blocking_headers {
                        let xss_scan = xss::Xss::new(request.clone());
                        xss_scan.value_scan(self.payloads.get("xss").unwrap().clone(),&_prog).await;
                        xss_scan.name_scan(self.payloads.get("xss").unwrap().clone(),&_prog).await;
                    }
                }
                _ => {
                    println!("Module {} not found",module);
                }
            }
        }
    }
}
