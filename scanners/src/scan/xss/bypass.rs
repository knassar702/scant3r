#[path = "parser.rs"] mod parser;
use crate::scan::xss::parser::Location;
use std::collections::HashMap;

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
