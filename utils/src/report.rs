extern crate regex;
use regex::Regex;
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

mod requests;
mod poc;
use crate::requests::Msg;


#[derive(Serialize, Deserialize)]
struct Bug {
    name: String,
    request: String,
    response: String,
    payload: String,
    poc: String,
}


pub struct Report {
    pub name: String,
    pub payload: String,
    pub request: Msg,
}

impl Report {
    pub fn new(name: String, payload: String, request: Msg) -> Report {
        Report {
            name,
            payload,
            request,
        }
    }

    pub fn generate_report(&self) -> String {
        let mut report = String::new();
        report.push_str(&self.request);
        report.push_str("\n");
        report.push_str(&self.Type);
        report
    }

    pub fn save_report(&self, path: &str) {
        let mut report = String::new();
        report.push_str(&self.request);
        report.push_str("\n");
        report.push_str(&self.Type);
        let mut file = std::fs::File::create(path).unwrap();
        file.write_all(report.as_bytes()).unwrap();
    }


}
