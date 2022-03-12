
#[path = "parser.rs"] mod parser;
use parser::Location;

pub trait Payloads {
    fn generate(&self) -> String;
}

pub struct JSPayload {
    pub reflect: Location
}

impl JSPayload {
    pub fn new(reflect: Location) -> JSPayload {
        JSPayload {
            reflect: reflect
        }
    }
}

impl Payloads for JSPayload {
    fn generate(&self) -> String {
        let mut payload = String::new();
        match self.reflect {
            Location::AttrName(ref attr) => {
                payload.push_str("document.getElementById(\"");
                payload.push_str(attr);
                payload.push_str("\").value");
            },
            Location::AttrValue(ref attr) => {
                payload.push_str("document.getElementById(\"");
                payload.push_str(attr);
                payload.push_str("\").value");
            },
            Location::Comment(ref attr) => {
                payload.push_str("document.body.innerHTML");
            },
            Location::Text(ref attr) => {
                payload.push_str("document.cookie");
            },
            Location::TagName(ref attr) => {
                payload.push_str("document.getElementById(\"");
                payload.push_str(attr);
                payload.push_str("\").value");
            },
            _ => {
                payload.push_str("document.getElementById(\"");
                payload.push_str("\").value");
            }
        }
        payload
    }
}

