extern crate regex;
use regex::Regex;
mod requests;
use std::collections::HashMap;
use crate::requests::Msg;


pub struct Report {
    pub request: String,
    pub Type: String,
}

pub trait ReportType {
    fn json(&self,msg: &str) -> bool;
    fn html(&self,msg: &str) -> bool;
    fn csv(&self,msg: &str) -> bool;
    fn xml(&self,msg: &str) -> bool;
    fn find(&self,txt: &[u8]) -> HashMap<u64,String>;
}


impl ReportType for Report {
    fn json(&self,msg: &str) -> bool {
        true
    }

    fn html(&self,msg: &str) -> bool {
        true
    }

    fn csv(&self,msg: &str) -> bool {
        true
    }

    fn xml(&self,msg:&str) -> bool {
        true
    }

    fn find(&self,msg: &[u8]) -> HashMap<u64,String> {
        let mut found = HashMap::new();
        let reg = Regex::new("<body>").unwrap();
        reg.find_iter("<body> html").for_each(|m| {
            println!("{:?}",m);
        });
        found
    }

    fn poc(&self,msg: &str,pocType: &str) -> bool {
        // create
        true
    }
}
