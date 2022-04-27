#![allow(dead_code)]
use reqwest::blocking::ClientBuilder;
use reqwest::header::{
    HeaderMap,
    HeaderName,
    HeaderValue};
use reqwest::redirect::Policy;
use reqwest::Proxy;
use reqwest::StatusCode;
use std::collections::HashMap;
use url::Url;

pub struct Resp {
    pub url: Url,
    pub status: StatusCode,
    pub headers: HeaderMap,
    pub body: String,
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
        if _proxy.is_empty() {
            self.proxy = None;
        } else {
            self.proxy = Some(_proxy);
        }
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
    pub fn send(&self) -> Result<Resp, reqwest::Error> {
        // sleep with tokio

        if let Some(delay) = self.delay {
            std::thread::sleep(std::time::Duration::from_secs(delay));
        }

        let mut resp = ClientBuilder::new()
            .danger_accept_invalid_certs(true)
            .timeout(std::time::Duration::from_secs(self.timeout.unwrap_or(30)))
            .user_agent("Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
            .redirect(Policy::limited((self.redirect.unwrap_or(10) as u16).into()));

        let mut headers = HeaderMap::new();
        if self.proxy.is_some() {
            resp = resp.proxy(Proxy::all(self.proxy.as_ref().unwrap()).unwrap());
        }
        self.headers.iter().for_each(|(k, v)| {
            headers.append(
                HeaderName::from_bytes(k.as_bytes()).unwrap(),
                HeaderValue::from_str(v.as_str()).unwrap(),
            );
        });
        if headers.len() > 0 {
            resp = resp.default_headers(headers);
        }

        match resp
            .build()
            .unwrap()
            .request(
                reqwest::Method::from_bytes(self.method.as_bytes()).unwrap(),
                self.url.as_str(),
            )
            .send()
        {
            Ok(res) => Ok(Resp {
                url: res.url().clone(),
                status: res.status(),
                headers: res.headers().clone(),
                body: match res.text() {
                    Ok(body) => body,
                    Err(_) => "".to_string(),
                },
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
            curl.push_str(&format!("-d \"{:?}\" ", self.body.as_ref().unwrap()));
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
