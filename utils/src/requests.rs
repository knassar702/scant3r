#![allow(dead_code)]
use isahc::http::{HeaderMap, StatusCode};
use isahc::prelude::*;
use isahc::Request;
use std::collections::HashMap;
use url::Url;

pub struct Resp {
    pub url: Url,
    pub status: StatusCode,
    pub headers: HeaderMap,
    pub body: String,
    pub error: Option<String>,
}

#[derive(Debug, Clone)]
pub struct Msg {
    pub method: String,
    pub url: Url,
    pub headers: HashMap<String, String>,
    pub body: Option<String>,
    pub redirect: Option<u32>,
    pub timeout: Option<u64>,
    pub proxy: Option<String>,
    pub delay: Option<u64>,
}

pub trait Settings {
    fn method(&mut self, _method: String) -> Self;
    fn url(&mut self, _url: String) -> Self;
    fn headers(&mut self, _headers: HashMap<String, String>) -> Self;
    fn body(&mut self, _body: String) -> Self;
    fn redirect(&mut self, _many: u32) -> Self;
    fn timeout(&mut self, _sec: u64) -> Self;
    fn proxy(&mut self, _proxy: String) -> Self;
    fn delay(&mut self, _sec: u64) -> Self;
}

impl Settings for Msg {
    fn method(&mut self, _method: String) -> Self {
        self.method = _method;
        self.clone()
    }
    fn url(&mut self, _url: String) -> Self {
        self.url = url::Url::parse(_url.as_str()).unwrap();
        self.clone()
    }
    fn headers(&mut self, _headers: HashMap<String, String>) -> Self {
        self.headers = _headers;
        self.clone()
    }
    fn body(&mut self, _body: String) -> Self {
        self.body = Some(_body);
        self.clone()
    }
    fn redirect(&mut self, _many: u32) -> Self {
        self.redirect = Some(_many);
        self.clone()
    }
    fn timeout(&mut self, _sec: u64) -> Self {
        self.timeout = Some(_sec);
        self.clone()
    }
    fn proxy(&mut self, _proxy: String) -> Self {
        self.proxy = Some(_proxy);
        self.clone()
    }
    fn delay(&mut self, _sec: u64) -> Self {
        self.delay = Some(_sec);
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
            proxy: None,
            delay: None,
        }
    }
    pub fn send(&self) -> Result<Resp, isahc::Error> {
        // sleep with tokio

        if let Some(delay) = self.delay {
            std::thread::sleep(std::time::Duration::from_secs(delay));
        }

        let mut response = Request::builder()
            .method(self.method.as_str())
            .ssl_options(isahc::config::SslOption::DANGER_ACCEPT_INVALID_CERTS)
            .timeout(std::time::Duration::from_secs(self.timeout.unwrap_or(30)))
            .redirect_policy(isahc::config::RedirectPolicy::Limit(
                self.redirect.unwrap_or(5),
            ));
        if self.proxy.as_ref().unwrap_or(&"".to_string()).len() > 0 {
            response = response.proxy(
                self.proxy
                    .as_ref()
                    .map(|proxy| proxy.as_str().parse().unwrap()),
            );
        }

        for (key, value) in &self.headers {
            response = response.header(key.as_str(), value.as_str());
        }
        match response
            .uri(self.url.as_str())
            .body(self.body.clone().unwrap_or_else(|| "".to_string()))
            .unwrap()
            .send()
        {
            Ok(mut res) => Ok(Resp {
                        url: self.url.clone(),
                        status: res.status(),
                        headers: res.headers().clone(),
                        body: res.text().unwrap(),
                        error: None,
                    }),

            Err(e) => Err(e),
        }
    }
}

pub trait Curl {
    fn curl(&self) -> String;
}

impl Curl for Msg {
    fn curl(&self) -> String {
        // convert isahc request to curl
        let mut curl = String::from("curl ");
        // extract headers
        self.headers.iter().for_each(|(key, value)| {
            curl.push_str(&format!("-H \"{}: {}\" ", key, value.replace("\"", "\\\"")));
        });
        // extract body
        if self.body.as_ref().unwrap().len() > 0 {
            curl.push_str(&format!(
                "-d \"{:?}\" ",
                self.body.as_ref().unwrap()
            ));
        }
        // extract url
        curl.push_str(&format!("\"{}\"", self.url));
        // extract method
        curl.push_str(&format!(" -X {}", self.method));
        // proxy
        if self.proxy.as_ref().unwrap_or(&"".to_string()).len() > 0 {
            curl.push_str(&format!(" -x {}", self.proxy.as_ref().unwrap()));
        }
        curl
    }
}

