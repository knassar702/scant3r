extern crate scant3r_utils;

use async_trait::async_trait;
use indicatif::ProgressBar;
use log::error;
use scant3r_utils::{
    requests::Msg,
    Injector::{Injector, Urlinjector},
};
use std::collections::HashMap;

mod parser;
use parser::{html_search, parse};

mod bypass;
use bypass::{PayloadGen, XssPayloads};
// create a struct with refrence Vec

pub struct Xss<'t> {
    request: &'t Msg,
    injector: Injector,
}

#[async_trait]
pub trait XssUrlParamsValue {
    // scan url params value
    async fn value_reflected(&self) -> Vec<String>;
    async fn value_scan(
        &self,
        payloads: Vec<String>,
        _prog: &ProgressBar,
    ) -> HashMap<url::Url, String>;
}

impl Xss<'_> {
    pub fn new(request: &Msg, keep_value: bool) -> Xss<'_> {
        Xss {
            request,
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
        let check_requests = self.injector.url_value("scanttrr");
        for (_param, urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                match req.send().await {
                    Ok(resp) => {
                        if resp.body.contains("scanttrr") {
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

    async fn value_scan(
        &self,
        payloads: Vec<String>,
        _prog: &ProgressBar,
    ) -> HashMap<url::Url, String> {
        let mut _found: HashMap<url::Url, String> = HashMap::new();
        for param in self.value_reflected().await {
            for payload in &payloads {
                if payload.len() == 0 {
                    continue;
                }
                let payload = payload
                    .replace("JS_FUNC", "alert")
                    .replace("JS_VALUE", "scanttrr");
                let mut req = self.request.clone();
                req.url = self.injector.set_urlvalue(&param, "hackerman");
                let res = match req.send().await {
                    Ok(resp) => resp,
                    Err(e) => {
                        error!("{}", e);
                        continue;
                    }
                };
                for x in parse(&res.body.as_str(), "hackerman".to_string()).iter() {
                    /*
                     * Check if the payload is in the html and analyze it for chosen tags
                     * */
                    req.url = self.injector.set_urlvalue(&param, &payload);
                    let Payloads = XssPayloads {
                        js_cmd: vec!["pp".to_string()],
                        js_value: vec!["1".to_string()],
                        html_tags: vec!["<img src=x JS_FUNC(JS_VALUE)>".to_string()],
                    };
                    let PayloadGenerator =
                        PayloadGen::new(&res.body.as_str(), x, "hackerman", &Payloads);
                    for pay in PayloadGenerator.analyze().iter() {
                        req.url = self.injector.set_urlvalue(&param, &pay.payload);
                        match req.send().await {
                            Ok(resp) => {
                                let d = html_search(resp.body.as_str(), &pay.search);
                                if d.len() > 0 {
                                    _prog.println(format!(
                                        "FOUND DOM XSS {:?} | {:?} | {:?}",
                                        x, pay.payload, d
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
        }
        _found
    }
}
