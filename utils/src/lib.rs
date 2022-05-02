pub mod injector;
pub mod requests;
use rand::distributions::Alphanumeric;
use rand::{thread_rng, Rng};
use regex::Regex;
use std::collections::HashMap;
use urlencoding::encode as url_encode;

pub fn valid_url(url: &str) -> bool {
    reqwest::Url::parse(url).is_ok()
}

pub fn urlencode(s: &str, many: Option<u8>) -> String {
    let mut after_encode = String::from(s);
    for _ in 0..many.unwrap_or(1) {
        after_encode = url_encode(&after_encode).to_string();
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
    use reqwest::Url;
    use std::collections::HashMap;
    use crate::injector::{self, Urlinjector};

    #[test]
    fn check_headers() {
        let result = super::extract_headers("Content-Type: application/json".to_string());
        assert_eq!(result.get("Content-Type").unwrap(), "application/json");
    }
    #[test]
    fn check_urlencode() {
        let result = super::urlencode("http://www.google.com", Some(2));
        assert_eq!(result, "http%3A%2F%2Fwww.google.com");
    }
    #[test]
    fn check_header_vec() {
        let mut test_result = HashMap::new();
        test_result.insert("Server".to_string(), "Nginx".to_string());
        let result = super::extract_headers_vec(vec!["Server: Nginx".to_string()]);
        assert_eq!(test_result,result);
    }
    #[test]
    fn check_url_injector_keepvalue() {
        let mut test_params = HashMap::new();
        test_params.insert("test".to_string(), vec![Url::parse("http://google.com/?test=1hello").unwrap()]);
        let inj = injector::Injector{
            request: Url::parse("http://google.com/?test=1").unwrap(),
            keep_value: true
        };
        let newparam_value = inj.set_urlvalue("test", "hello");
        let inject_payload = inj.url_value("hello");
        assert_eq!(newparam_value.as_str(),"http://google.com/?test=1hello");
        assert_eq!(inject_payload, test_params);
    }
}
