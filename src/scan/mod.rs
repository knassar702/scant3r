pub mod xss;
#[path = "../payloads.rs"]
mod requests;
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use home::home_dir;

use crate::requests::Msg;


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
                        info!("Loaded payloads from file");
                } else {
                    error!("No payloads found for xss module");
                    let module_location = self.modules.iter().position(|x| *x == module).unwrap();
                    self.modules.remove(module_location);
                    warn!("Module {} was removed from the modules list", module);
                    }
            }
    }
    pub async fn scan(&self,request: Msg) -> u32 {
        let mut score = 0;
        if self.payloads.len() == 0 {
            panic!("No payloads loaded");
        }
        for module in self.modules.clone() {
            match module {
                "xss" => {
                    let xss_scan = xss::Xss::new(request.clone(), self.inject_query, self.inject_body);
                    xss_scan.scan(&self.payloads.get("xss").unwrap()).await;
                },
                _ => {
                    println!("Module not found");
                }
            }
        }
        score
    }
}