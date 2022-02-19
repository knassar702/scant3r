use url::Url;
use std::collections::HashMap;

pub struct Request {
    pub url: Url,
    pub method: String,
    pub headers: HashMap<String, String>,
    pub body: String,
}

pub struct Site {
    request: Request,
    base: Url,
}
