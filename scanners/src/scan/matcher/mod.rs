use fancy_regex::Regex;
use std::collections::HashMap;

pub struct Matcher {
    pub response: String,
}

impl Matcher {
    pub fn new(response: String) -> Matcher {
        Matcher { response }
    }

    pub fn match_regex(&self, regex: &str) -> bool {
        let re = Regex::new(regex).unwrap();
        re.is_match(&self.response)
    }

    pub fn match_hashmap(&self, hashmap: &HashMap<String, String>) -> bool {
        for (key, value) in hashmap {
            if !self.match_regex(&value) {
                return false;
            }
        }
        true
    }
}
