#[path = "../payloads.rs"]
mod requests;

use serde_json::to_string;
use crate::requests::Msg;

pub struct Scanner{
    pub request: Msg,
    pub modules: Vec<&'static str>,
}

impl Scanner {
    pub fn new(request: Msg,modules: Vec<&'static str>) -> Scanner {
        Scanner {
            request,
            modules,
        }
    }

    pub fn load_payloads(&self) -> Vec<String> {
        for module in self.modules.clone() {
            println!("Loading payloads frfffom {}", module);
            match module {
             "xss" => {
                    println!("[+] Loading payloads from {}", module);
                },
                _ => {
                    println!("Module not found");
                }
            }
        }
        vec![]
    }
    pub fn scan(&self) -> Vec<String> {
        vec![]
    }
}
