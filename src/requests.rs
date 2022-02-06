// allow dead code
#![allow(dead_code)]
use isahc::prelude::*;
use isahc::{Body, Request, Response};
use std::collections::HashMap;
use url::Url;

pub struct Msg {
    pub method: String,
    pub url: Url,
    pub headers: HashMap<String, String>,
    pub body: Option<String>,
    pub redirect: Option<u32>,
    pub timeout: Option<u64>,
    pub response: Option<Response<Body>>,
    pub response_body: Option<String>,
    pub error: Option<String>,
    pub proxy: Option<String>,
}

impl Msg {
    pub fn new(
        method: &str,
        url: &str,
        headers: HashMap<String, String>,
        body: Option<String>,
        redirect: Option<u32>,
        timeout: Option<u64>,
        proxy: Option<String>,
    ) -> Msg {
        Msg {
            method: method.to_string(),
            url: Url::parse(url).unwrap(),
            headers,
            body,
            redirect,
            timeout,
            response: None,
            response_body: None,
            error: None,
            proxy,
        }
    }
    pub fn send(&mut self) {
        let mut response = Request::builder()
            .method(self.method.as_str())
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_CERTS)
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_HOSTS)
            .redirect_policy(isahc::config::RedirectPolicy::Limit(
                self.redirect.unwrap_or(5),
            ))
            .proxy(self.proxy.as_ref().map(|proxy| proxy.as_str().parse().unwrap()));
        for (key, value) in &self.headers {
            response = response.header(key.as_str(), value.as_str());
        }
        match response
            .uri(self.url.as_str())
            .body(self.body.clone().unwrap_or_else(|| "".to_string()))
            .unwrap()
            .send()
        {
            Ok(mut res) => {
                self.response_body = Some(res.text().unwrap());
                self.response = Some(res);
            
            }
            Err(e) => {
                self.error = Some(e.to_string());
            }
        };
    }
}


