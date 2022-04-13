extern crate scant3r_utils;

use async_trait::async_trait;
use indicatif::ProgressBar;
use log::error;
use scant3r_utils::{
    random_str,
    requests::{Msg,Curl},
    Injector::{Injector, Urlinjector},
};
use std::collections::HashMap;

mod parser;
use parser::{html_parse, html_search};

mod bypass;
pub use bypass::{PayloadGen, XssPayloads};

pub struct Xss<'t> {
    request: &'t Msg,
    injector: Injector,
    payloads: &'t XssPayloads,
}

#[async_trait]
pub trait XssUrlParamsValue {
    // scan url params value
    async fn value_reflected(&self) -> Vec<String>;
    async fn value_scan(&self, _prog: &ProgressBar) -> HashMap<url::Url, String>;
}

impl Xss<'_> {
    pub fn new<'a>(request: &'a Msg, payloads: &'a XssPayloads, keep_value: bool) -> Xss<'a> {
        Xss {
            request,
            payloads,
            injector: Injector {
                request: request.url.clone(),
                keep_value,
            },
        }
    }
}

#[async_trait]
impl XssUrlParamsValue for Xss<'_> {
    async fn value_reflected(&self) -> Vec<String> {
        let mut reflected_parameters: Vec<String> = Vec::new();
        let payload = random_str(5);
        let check_requests = self.injector.url_value(&payload);
        for (_param, urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                match req.send().await {
                    Ok(resp) => {
                        let found = resp.body.contains(&payload);
                        if found {
                            reflected_parameters.push(_param);
                        }
                    }
                    Err(e) => {
                        error!("{}", e);
                        continue;
                    }
                };
            }
        }
        reflected_parameters
    }

    async fn value_scan(&self, _prog: &ProgressBar) -> HashMap<url::Url, String> {
        let mut _found: HashMap<url::Url, String> = HashMap::new();
        for param in self.value_reflected().await {
            let mut req = self.request.clone();
            let payload = random_str(5).to_lowercase();
            req.url = self.injector.set_urlvalue(&param,&payload);
            let res = match req.send().await {
                Ok(resp) => resp,
                Err(e) => {
                    _prog.set_message(format!("CONNECTION ERROR: {}", e));
                    continue;
                }
            };
            for reflect in html_parse(&res.body.as_str(), &payload).iter() {
                let payload_generator =
                    PayloadGen::new(&res.body.as_str(), reflect, &payload, &self.payloads);
                for pay in payload_generator.analyze().iter() {
                    let count = html_search(&res.body.as_str(), &pay.search);
                    req.url = self.injector.set_urlvalue(&param, &pay.payload);
                    match req.send().await {
                        Ok(resp) => {
                            let d = html_search(resp.body.as_str(), &pay.search);
                            if d.len() > count.len() {
                                _prog.println(format!(
                                    "FOUND XSS \nReflect: {:?}\nPayload: {:?}\nMatch: {:?}\nCURL: {:?}",
                                    reflect, pay.payload, d,req.curl()
                                ));
                                break;
                            }
                        }
                        Err(_e) => {
                            continue;
                        }
                    };
                }
            }
        }
        _found
    }
}
