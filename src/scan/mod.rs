pub mod xss;
#[path = "../payloads.rs"]
mod requests;
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use crate::requests::Msg;


#[derive(Debug, Clone)]
pub struct Scanner{
    pub modules: Vec<&'static str>,
    pub payloads: HashMap<String,Vec<String>>,
}

impl Scanner {
    pub fn new(modules: Vec<&'static str>) -> Scanner {
        Scanner {
            modules,
            payloads: HashMap::new(),
        }
    }

    pub fn load_payloads(&mut self) {
        for module in self.modules.clone() {
                    let dir = home::home_dir().unwrap().join(format!(".scant3r/{}.txt",&module)).to_str().unwrap().to_string();
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
                      if xss::scan(request.clone(), self.payloads.get("xss").unwrap()).await {
                          score += 1;
                      }
                },
                _ => {
                    println!("Module not found");
                }
            }
        }
        score
    }
}
