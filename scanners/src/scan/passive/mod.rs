extern crate scant3r_utils;

use std::collections::HashMap;
use scant3r_utils::requests::Msg;
use indicatif::ProgressBar;

struct Passive<'t> {
    requests: &'t Msg,
    config: HashMap<String,String>
}


impl Passive<'_> {
    pub fn new(requests: &Msg) -> Passive {
        Passive {
            requests,
            injector: Urlinjector::new(),
        }
    }

    pub fn headers(&self) -> Vec<String> {
        let mut headers = Vec::new();
        for header in self.requests.headers.iter() {
            headers.push(header.to_string());
        }
        headers
    }

    pub fn body(&self) -> String {
    }

}
