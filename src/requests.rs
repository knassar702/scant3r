use std::collections::HashMap;
use url::Url;
use isahc::prelude::*;
use isahc::Request;

pub struct Msg {
    pub method: String,
    pub url: Url,
    pub headers: HashMap<String, String>,
    pub body: Option<String>,
    pub response: Option<String>,
    pub error: Option<String>,
    pub status: Option<u16>,
    pub proxy: Option<String>,
}

impl Msg {
    pub fn new(method: &str, url: &str, headers: HashMap<String, String>, body: Option<String>,proxy: Option<String>) -> Msg {
        Msg {
            method: method.to_string(),
            url: Url::parse(url).unwrap(),
            headers,
            body,
            response: None,
            error: None,
            status: None,
            proxy: proxy,
        }
    }
    pub fn scan(&mut self) -> () {
        let mut response = Request::builder()
            .method(self.method.as_str())
            .proxy({
                if let Some(proxy) = &self.proxy {
                    Some(proxy.as_str().parse().unwrap())
                } else {
                    None
                }
            });
        for (key, value) in &self.headers {
            response = response.header(key.as_str(), value.as_str());
        }
        match response.uri(self.url.as_str()).body(self.body.clone().unwrap_or("".to_string())).unwrap().send() {
            Ok(res) => {
                self.status = Some(u16::from(res.status()));
            }
            Err(e) => {
                self.error = Some(e.to_string());
            }
        };

    }
    pub fn set_body(&mut self, body: &str) {
        self.body = Some(body.to_string());
    }

    pub fn set_header(&mut self, key: &str, value: &str) {
        self.headers.insert(key.to_string(), value.to_string());
    }

}

