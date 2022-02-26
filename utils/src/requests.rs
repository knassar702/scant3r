#![allow(dead_code)]
use async_trait::async_trait;
use isahc::prelude::*;
use isahc::Request;
use isahc::http::{
    HeaderValue,
    HeaderMap,
    StatusCode
};
use std::collections::HashMap;
use tokio::time::Duration;
use url::Url;

#[derive(Debug, Clone)]
pub struct Msg {
    pub method: String,
    pub url: Url,
    pub headers: HashMap<String, String>,
    pub body: Option<String>,
    pub redirect: Option<u32>,
    pub timeout: Option<u64>,
    pub response_body: Option<String>,
    pub response_status: Option<StatusCode>,
    pub response_headers: Option<HeaderMap<HeaderValue>>,
    pub error: Option<String>,
    pub proxy: Option<String>,
}

pub trait Settings {
    fn method(&mut self,_method: String) -> Self;
    fn url(&mut self,_url: String) -> Self;
    fn headers(&mut self,_headers: HashMap<String,String>) -> Self;
    fn body(&mut self,_body: String) -> Self;
    fn redirect(&mut self,_many: u32) -> Self;
    fn timeout(&mut self,_sec: u64) -> Self;
    fn proxy(&mut self,_proxy: String) -> Self;
}


impl Settings for Msg {
    fn method(&mut self,_method: String) -> Self {
        self.method = _method;
        self.clone()
    }
    fn url(&mut self,_url: String) -> Self {
        self.url = url::Url::parse(_url.as_str()).unwrap();
        self.clone()
    }
    fn headers(&mut self,_headers: HashMap<String,String>) -> Self {
        self.headers = _headers;
        self.clone()
    }
    fn body(&mut self,_body: String) -> Self {
        self.body = Some(_body);
        self.clone()
    }
    fn redirect(&mut self,_many: u32) -> Self {
        self.redirect = Some(_many);
        self.clone()
    }
    fn timeout(&mut self,_sec: u64) -> Self {
        self.timeout = Some(_sec);
        self.clone()
    }
    fn proxy(&mut self,_proxy: String) -> Self {
        self.proxy = Some(_proxy);
        self.clone()
    }
}

impl Msg {
    pub fn new() -> Msg {
        Msg {
            method: "GET".to_string(),
            url: Url::parse("http://localhost").unwrap(),
            headers: HashMap::new(),
            body: None,
            redirect: None,
            timeout: None,
            response_body: None,
            response_status: None,
            response_headers: None,
            error: None,
            proxy: None,
        }
    }
    pub async fn send(&mut self) {
        let mut response = Request::builder()
            .method(self.method.as_str())
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_CERTS)
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
            .send_async().await
        {
            Ok(mut res) => {
                self.response_status = Some(res.status());
                self.response_body = Some(res.text().await.unwrap());
                self.response_headers = Some(res.headers().clone());
                self.error = None;
            }
            Err(e) => {
                self.response_body = None;
                self.error = Some(e.to_string());
            }
        };
    }
}
