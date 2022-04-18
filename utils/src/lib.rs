#[allow(non_snake_case)]
#[path = "./injector.rs"]
pub mod Injector;
pub mod poc;
pub mod requests;
use regex::Regex;
use std::collections::HashMap;
use rand::{Rng, thread_rng};
use rand::distributions::Alphanumeric;
use urlencoding::encode as url_encode;

pub fn urlencode(s: &str,many: Option<u8>) -> String {
    let mut after_encode = String::from(s);
    for _ in 0..many.unwrap_or(1) {
        after_encode = url_encode(s).to_string();
    }
    after_encode
}

pub fn random_str(len: usize) -> String {
    let mut rng = thread_rng();
    let chars: Vec<char> = rng.sample_iter(&Alphanumeric).take(len).collect();
    return chars.iter().collect();
}

pub fn extract_headers(header: String) -> HashMap<String, String> {
    // regex to extract headers
    let re = Regex::new(r"(.*):\s(.*)").unwrap();
    let mut headers: HashMap<String, String> = HashMap::new();
    for cap in re.captures_iter(header.as_str()) {
        headers.insert(cap[1].to_string(), cap[2].to_string());
    }
    headers
}

pub fn extract_headers_vec(header: Vec<String>) -> HashMap<String, String> {
    // regex to extract headers
    let re = Regex::new(r"(.*):\s(.*)").unwrap();
    let mut headers: HashMap<String, String> = HashMap::new();
    header.iter().for_each(|x| {
        for cap in re.captures_iter(x.as_str()) {
            headers.insert(cap[1].to_string(), cap[2].to_string());
        }
    });
    headers
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = super::extract_headers("Content-Type: application/json".to_string());
        assert_eq!(result.get("Content-Type").unwrap(), "application/json");
    }
    #[test]
    fn check_urlencode() {
        let result = super::urlencode("http://www.google.com", None);
        assert_eq!(result, "http%3A%2F%2Fwww.google.com");
    }
}
