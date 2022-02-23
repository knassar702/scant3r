extern crate scant3r_utils;
use scant3r_utils::{
    payloads::{
        Injector,
        url_injector
    },
    poc::{
        Poc,
        Curl
    },
    requests::Msg
};
use async_trait::async_trait;
use std::collections::HashMap;
use indicatif::ProgressBar;

pub struct Xss {
    request: Msg,
    blind: bool,
    injector: Injector,
    poc_type: String,
}

pub trait XssHeaders {
    fn find_reflected(&self) -> HashMap<String, String>;
    fn scan(&self, payloads: &Vec<String>) -> bool;
}

pub trait XssUrlParamsName {
    // scan url params name
    fn find_reflected(&self) -> HashMap<String, String>;
    fn scan(&self, payloads: &Vec<String>) -> bool;
}

#[async_trait]
pub trait XssUrlParamsValue {
    // scan url params value
    fn new(request: Msg, blind: bool, poc_type: String) -> Self;
    async fn find_reflected(&self) -> HashMap<String,url::Url>;
    async fn scan(&self, payloads: Vec<String>,prog: &ProgressBar) -> bool;
}

#[async_trait]
impl XssUrlParamsValue for Xss {
    fn new(request: Msg,blind: bool, poc_type: String) -> Xss {
        Xss {
            request: request.clone(),
            blind: blind,
            injector: Injector{request: request.url},
            poc_type: poc_type
        }
    }

    async fn find_reflected(&self) -> HashMap<String,url::Url> {
        let mut reflected_parameters: HashMap<String,url::Url> = HashMap::new();
        let check_requests = self.injector.url_parameters("scantrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                req.send().await;
                if req.response_body.unwrap().contains("scantrr") {
                    reflected_parameters.insert(_param,url.clone());
                }
            }
        }
        reflected_parameters
    }

    async fn scan(&self,payloads: Vec<String>,prog: &ProgressBar) -> bool {
        for (param,url) in self.find_reflected().await {
            for payload in &payloads {
                let mut req = self.request.clone();
                req.url = url.clone();
                let new_params = {
                        let params = req.url.query_pairs().into_iter().collect::<HashMap<_, _>>();
                        let mut params2 = HashMap::new();
                        for (key,value) in params.clone() {
                            params2.insert(key.to_string(),value.clone().to_string());
                        }
                        *params2.get_mut(&param).unwrap() = payload.to_string();
                        params2
                };
                req.url = {
                    req.url.query_pairs_mut().clear();
                    for (key,value) in new_params {
                        req.url.query_pairs_mut().append_pair(&key,&value);
                    }
                    req.url
                };
                req.send().await;
                let body = req.response_body.as_ref().unwrap();
                if body.contains(payload) {
                    body.lines().enumerate().for_each(|x|{
                        if x.1.contains(payload) == true {
                            let report = Poc {
                                name: "sg".to_owned(),
                                payload: payload.to_owned(),
                                request: req.clone(),
                            };
                            match &self.poc_type as &str {
                                "curl" => {
                                    let curl = report.curl();
                                    prog.println(format!("TEST {}",curl));
                                },
                                _ => {
                                    println!("BRUH");
                                }
                            }
                        }
                    });
                    break;
                } else {
                    continue;
                }
            }
        }
        false
    }
}
