extern crate scant3r_utils;

use scant3r_utils::{
    Injector::{
        Urlinjector,
        Injector
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
use console::Emoji;

pub struct Xss {
    request: Msg,
    injector: Injector,
}


#[async_trait]
pub trait XssUrlParamsName {
    async fn name_reflected(&self) -> ();
    async fn name_scan(&self, payloads: Vec<String>,_prog: &ProgressBar) -> ();
}

#[async_trait]
pub trait XssUrlParamsValue {
    // scan url params value
    async fn value_reflected(&self) -> HashMap<String,url::Url>;
    async fn value_scan(&self, payloads: Vec<String>,_prog: &ProgressBar) ->HashMap<url::Url, String>;
}



impl Xss {
    pub fn new(request: Msg) -> Xss {
        Xss {
            request: request.clone(),
            injector: Injector{request: request.url},
        }
    }

}



#[async_trait]
impl XssUrlParamsName for Xss {
    async fn name_reflected(&self) -> () {
    }

    async fn name_scan(&self,_payloads: Vec<String>, _prog: &ProgressBar) -> () {

    }
}

#[async_trait]
impl XssUrlParamsValue for Xss {

    async fn value_reflected(&self) -> HashMap<String,url::Url>  {
        let mut reflected_parameters: HashMap<String,url::Url> = HashMap::new();
        let check_requests = self.injector.url_value("scanttrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                let resp = &req.send().await;
                if resp.body.contains("scanttrr") {
                    reflected_parameters.insert(_param,url.clone());
                }
            }
        }
        reflected_parameters
    }

    async fn value_scan(&self,payloads: Vec<String>,_prog: &ProgressBar) -> HashMap<url::Url, String>{
        let mut _found: HashMap<url::Url,String> = HashMap::new();
        for (param,url) in self.value_reflected().await {

            for payload in &payloads {

                let mut req = self.request.clone();
                req.url = self.injector.set_urlvalue(&param, payload, url.clone());
                let res = req.send().await;
                if res.error.is_some() {
                    println!("\n\n\n\n{}",res.error.unwrap());
                    continue;
                }
                if res.body.contains(payload) {
                    res.body.lines()
                        .enumerate()
                        .for_each(|x|{

                        if x.1.contains(payload) == true {
                            let report = Poc {
                                name: "sg".to_owned(),
                                payload: payload.to_owned(),
                                request: req.clone(),
                            };
                            match "curl" {
                                "curl" => {
                                    // emoji cat
                                    let m = format!("{} {}\nLine: {}",Emoji("🐱", ""),report.curl(),&x.0);
                                    _prog.println(&m);
                                    _found.insert(req.url.clone(),m);
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
        _found
    }
}
