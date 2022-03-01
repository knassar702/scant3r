pub mod requests;
pub mod poc;
#[allow(non_snake_case)]
#[path = "./injector.rs"] pub mod Injector;
use std::collections::HashMap;
use regex::Regex;

pub fn extract_headers(header: String) -> HashMap<String, String> {
    // regex to extract headers
    let re = Regex::new(r"(.*):\s(.*)").unwrap();
    let mut headers: HashMap<String, String> = HashMap::new();
    for cap in re.captures_iter(header.as_str()) {
        headers.insert(cap[1].to_string(), cap[2].to_string());
    }
    headers
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = super::extract_headers("Content-Type: application/json");
        assert_eq!(result.get("Content-Type").unwrap(), "application/json");
    }
}
