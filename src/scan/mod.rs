#[path = "../payloads.rs"]
mod requests;
use std::collections::HashMap;
use std::io::prelude::*;
use std::path::Path;
use crate::{
    requests::Msg,
    xss
};

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

    pub fn load_payloads(&mut self) -> Vec<String> {
        for module in self.modules.clone() {
            match module {
             "xss" => {

                    if Path::new("/home/knassar702/.scant3r/xss.txt").exists() {
                            let mut payload_file = std::fs::File::open("/home/knassar702/.scant3r/xss.txt").unwrap();
                            let mut payload_string = String::new();
                            payload_file.read_to_string(&mut payload_string).unwrap();
                            let payloads: Vec<&str> = payload_string.split("\n").collect();
                            self.payloads.insert(String::from("xss"), payloads.iter().map(|x| x.to_string()).collect());
                            info!("Loaded payloads from file");
                    } else {
                        error!("No payloads found for xss module");
                        let module_location = self.modules.iter().position(|x| *x == module).unwrap();
                        self.modules.remove(module_location);
                        }
                },
                _ => {
                    error!("{}",format!("Module {} is not found", module));
                    let module_location = self.modules.iter().position(|x| *x == module).unwrap();
                    self.modules.remove(module_location);
                }
            }
        }
        vec![]
    }
    pub fn scan(&self,request: Msg){
        for module in self.modules.clone() {
            match module {
                "xss" => {
                      println!("{}",format!("{}",module));
//                    xss::scan(request, self.payloads.get("xss").unwrap());
                },
                _ => {
                    println!("Module not found");
                }
            }
        }
    }
}
