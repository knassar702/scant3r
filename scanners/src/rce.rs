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
use console::{
    Emoji,
    style
};
use async_trait::async_trait;
use std::collections::HashMap;
use indicatif::ProgressBar;

pub struct Rce {
    request: Msg,
    blind: bool,
    injector: Injector,
    poc_type: String,
}


#[async_trait]
pub trait RceUrlParamsValue {
    // scan url params value
    fn new(request: Msg, blind: bool, poc_type: String) -> Self;
    async fn scan(&self, payloads: Vec<String>,prog: &ProgressBar) -> bool;
}

#[async_trait]
impl RceUrlParamsValue for Rce {
    fn new(request: Msg,blind: bool, poc_type: String) -> Rce {
        Rce {
            request: request.clone(),
            blind: blind,
            injector: Injector{request: request.url},
            poc_type: poc_type
        }
    }
    async fn scan(&self,payloads: Vec<String>,prog: &ProgressBar) -> bool {
        for payload in payloads {
            let req = self.request.clone();
            let v = self.injector.url_parameters(payload);
            println!("BRUH {}",v);
        }
    }
}
