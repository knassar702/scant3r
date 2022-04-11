use std::collections::HashMap;
use toml::from_str as parse_toml;
use serde_derive::Deserialize;
use std::fs::read_to_string;

#[derive(Deserialize)]
pub struct Xss {
    pub js_cmd: String
}

#[derive(Deserialize, Debug)]
pub struct Opts {
    wordlist: HashMap<String, String>,
}

impl Default for Opts {
    fn default() -> Self {
        Opts {
            wordlist: HashMap::new(),
        }
    }
}

impl Opts {
    pub fn parse(&self, file: &str) {
        let read_file = read_to_string(file).expect("Unable to read file");
        let conf: Opts = match parse_toml(read_file.as_str()) {
            Ok(conf) => conf,
            Err(e) => {
                println!("KOSDKGOSKdg {}", e);
                std::process::exit(1);
            }
        };
        println!("{:?}", conf);
    std::process::exit(1);
    }
}
