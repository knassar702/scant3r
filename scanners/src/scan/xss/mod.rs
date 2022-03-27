extern crate scant3r_utils;

use futures::TryFutureExt;
use scant3r_utils::{
    Injector::{
        Urlinjector,
        Injector
    },
    requests::Msg
};
use async_trait::async_trait;
use std::collections::HashMap;
use indicatif::ProgressBar;
use log::error;

mod parser;
use parser::{
    parse,
    html_search,
};


mod bypass;
use bypass::{
    generate_xss_payload,
    match_qoutes,
    match_double_qoutes,
    PayloadGen
};
// create a struct with refrence Vec


pub struct Xss<'t> {
    request: &'t Msg,
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
    async fn value_reflected(&self) -> Vec<String>;
    async fn value_scan(&self, payloads: Vec<String>,_prog: &ProgressBar) ->HashMap<url::Url, String>;
}



impl Xss<'_> {
    pub fn new(request: &Msg,keep_value: bool) -> Xss<'_> {
        Xss {
            request,
            injector: Injector{request: request.url.clone(), keep_value},
        }
    }

}



#[async_trait]
impl XssUrlParamsName for Xss<'_> {
    async fn name_reflected(&self) -> () {
    }

    async fn name_scan(&self,_payloads: Vec<String>, _prog: &ProgressBar) -> () {

    }
}

#[async_trait]
impl XssUrlParamsValue for Xss<'_> {

    async fn value_reflected(&self) -> Vec<String>  {
        let mut reflected_parameters: Vec<String> = Vec::new();
        let check_requests = self.injector.url_value("scanttrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                match req.send().await {
                    Ok(resp) => {
                        if resp.body.contains("scanttrr") {
                            reflected_parameters.push(_param);
                        }
                    },
                    Err(e) => {
                        error!("{}",e);
                        continue;
                    }
                };

            }
        }
        reflected_parameters
    }

    async fn value_scan(&self,payloads: Vec<String>,_prog: &ProgressBar) -> HashMap<url::Url, String>{
        let mut _found: HashMap<url::Url,String> = HashMap::new();
        for param in self.value_reflected().await {

            for payload in &payloads {
                if payload.len() == 0 {continue;}
                let payload = payload.replace("JS_FUNC","alert")
                                     .replace("JS_VALUE","scanttrr");
                let mut req = self.request.clone();
                req.url = self.injector.set_urlvalue(&param, "hackerman");
                let res = match req.send().await {
                    Ok(resp) => resp,
                    Err(e) => {
                        error!("{}",e);
                        continue;
                    }
                };
                for x in parse(&res.body.as_str(), "hackerman".to_string()).iter() {
                        /*
                         * Check if the payload is in the html and analyze it for chosen tags
                         * */
                        req.url = self.injector.set_urlvalue(&param, &payload);
                        let vvvv = PayloadGen::new(&res.body.as_str(), x,"hackerman",vec!["bruh"]);
                        for pay in vvvv.analyze().iter() {
                            req.url = self.injector.set_urlvalue(&param, &pay);
                            match req.send().await {
                                Ok(resp) => {
                                    let d = html_search(resp.body.as_str(),"*[onerror='alert()']");
                                },
                                Err(e) => {continue;}
                            };
                            _prog.println(format!("FFFFFFFFFf {:?} | {}",&x,&pay));
                        }
                    }
            }
        }
        _found
    }
}
