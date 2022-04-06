#[path = "parser.rs"]
mod parser;
use crate::scan::xss::parser::{
    Location,
    css_selector
};
use fancy_regex::Regex;


pub struct XssPayloads {
    pub js_cmd: Vec<String>,
    pub js_value: Vec<String>,
    pub attr: Vec<String>,
    pub html_tags: Vec<String>,
}

pub struct OrderPayload {
    pub search: String,
    pub payload: String,
}

pub fn match_qoutes(d: &str, s: &str) -> bool {
    let re = Regex::new(&format!(r#"=\'.*{}*.\'"#, s)).unwrap();
    re.is_match(d).unwrap_or(false)
}

pub fn match_double_qoutes(d: &str, s: &str) -> bool {
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

    pub fn txt_payloads(&self) -> Vec<OrderPayload> {
        let mut payloads = vec![];
        self.payloads.html_tags.iter().for_each(|tag| {
            self.payloads.js_cmd.iter().for_each(|cmd| {
                    self.payloads.js_value.iter().for_each(|value| {
                        let payload = tag.replace("$JS_FUNC$", cmd).replace("$JS_CMD$", value);
                        let search = css_selector(&payload);
                        payloads.push(OrderPayload {
                            payload,
                            search,
                        });
                    });
                });
        });
        payloads
    }

    pub fn tagname_payloads(&self) -> Vec<OrderPayload> {
        let mut payloads = vec![];
        self.payloads.js_cmd.iter().for_each(|cmd| {
            self.payloads.js_value.iter().for_each(|value| {
            });
        });
        payloads
    }
    pub fn analyze(&self) -> Vec<OrderPayload> {
        match *self.location {
            Location::Text(ref _txt) => {
                self.txt_payloads()
            },
            Location::TagName(ref _txt) => {vec![]},
            Location::AttrName(ref _txt) => {vec![]},
            Location::AttrValue(ref _txt) => {vec![]},
            Location::Comment(ref _txt) => {vec![]},
        }
    }
}
