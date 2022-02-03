use std::collections::HashMap;
use url::Url;
use isahc::prelude::*;
use isahc::{Response,Request,Body};

pub struct Msg {
    pub method: String,
    pub url: Url,
    pub headers: HashMap<String, String>,
    pub body: Option<String>,
    pub redirect: Option<u32>,
    pub response: Option<Response<Body>>,
    pub error: Option<String>,
    pub proxy: Option<String>,
}

impl Msg {
    pub fn new(method: &str, url: &str, headers: HashMap<String, String>, body: Option<String>,redirect: Option<u32>,proxy: Option<String>) -> Msg {
        Msg {
            method: method.to_string(),
            url: Url::parse(url).unwrap(),
            headers,
            body,
            redirect: redirect,
            response: None,
            error: None,
            proxy: proxy,
        }
    }
    pub fn send(&mut self) -> () {
        let mut response = Request::builder()
            .method(self.method.as_str())
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_CERTS)
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_HOSTS)
            .redirect_policy(isahc::config::RedirectPolicy::Limit(self.redirect.unwrap_or(5)))
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
            Ok(mut res) => {
                self.response = Some(res);
            }
            Err(e) => {
                self.error = Some(e.to_string());
            }
        };

    }
    pub fn set_body(&mut self, body: &str) {
        self.body = Some(body.to_string());
    }



}

