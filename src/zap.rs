use std::collections::HashMap;
use url::Url;
use serde_json::{from_str,Value};
#[path = "requests.rs"]
mod requests;

pub struct Zaproxy {
    pub client: requests::Msg
}

impl Zaproxy {
    pub fn new(host: String, key: Option<String>) -> Zaproxy {
        let mut c = HashMap::new();
        c.insert(String::from("hostvv"),String::from("rr") );
        Zaproxy {
            client: requests::Msg::new("POST",host.as_str(),c,None,None)}
    }

    pub fn get_urls(&mut self) -> Vec<String> {
        let mut urls = Vec::new();
        self.client.url = self.client.url.join("/JSON/spider/view/allUrls/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("allUrls").unwrap().as_array().unwrap().iter().for_each(|x| {
            urls.push(x.as_str().unwrap().to_string());
        });
        urls
    }

    pub fn get_context(&mut self) -> Vec<String> {
        let mut contexts = Vec::new();
        self.client.url = self.client.url.join("/JSON/context/view/contextList/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("contextList").unwrap().as_array().unwrap().iter().for_each(|x| {
            contexts.push(x.as_str().unwrap().to_string());
        });
        contexts
    }

    pub fn new_context(&mut self,name: String) -> String {
        self.client.url = self.client.url.join("/JSON/context/action/newContext/").unwrap();
        self.client.body = Some(format!("contextName={}",name));
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("contextId").unwrap().as_str().unwrap().to_string()
    }


    pub fn delete_context(&mut self,id: String) {
        self.client.url = self.client.url.join("/JSON/context/action/deleteContext/").unwrap();
        self.client.body = Some(format!("contextId={}",id));
        self.client.send();
    }

    pub fn context_include(&mut self,contextName: String,regex: String) -> String {
        self.client.url = self.client.url.join("/JSON/context/action/include/").unwrap();
        self.client.body = Some(format!("contextName={}&regex={}",contextName,regex));
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("contextId").unwrap().as_str().unwrap().to_string()
    }

    pub fn context_exclude(&mut self,contextName: String,regex: String) -> String {
        self.client.url = self.client.url.join("/JSON/context/action/exclude/").unwrap();
        self.client.body = Some(format!("contextName={}&regex={}",contextName,regex));
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("contextId").unwrap().as_str().unwrap().to_string()
    }

    pub fn spider(&mut self,url: String,contextId: String) {
        self.client.url = self.client.url.join("/JSON/spider/action/scan/").unwrap();
        self.client.body = Some(format!("url={}&contextId={}",url,contextId));
        self.client.send();
    }


    pub fn spider_status(&mut self) -> String {
        self.client.url = self.client.url.join("/JSON/spider/view/status/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("status").unwrap().as_str().unwrap().to_string()
    }

    pub fn spider_results(&mut self) -> Vec<String> {
        self.client.url = self.client.url.join("/JSON/spider/view/results/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        let mut urls = Vec::new();
        results.as_object().unwrap().get("results").unwrap().as_array().unwrap().iter().for_each(|x| {
            urls.push(x.as_str().unwrap().to_string());
        });
        urls
    }

    pub fn ajax_spider(&mut self,url: String,contextId: String) {
        self.client.url = self.client.url.join("/JSON/ajaxSpider/action/scan/").unwrap();
        self.client.body = Some(format!("url={}&contextId={}",url,contextId));
        self.client.send();
    }

    pub fn ajax_spider_status(&mut self) -> String {
        self.client.url = self.client.url.join("/JSON/ajaxSpider/view/status/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("status").unwrap().as_str().unwrap().to_string()
    }

    pub fn ajax_spider_time(&mut self) -> String {
        self.client.url = self.client.url.join("/JSON/ajaxSpider/view/time/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("time").unwrap().as_str().unwrap().to_string()
    }


    pub fn hosts(&mut self) -> Vec<String> {
        self.client.url = self.client.url.join("/JSON/host/view/list/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        let mut hosts = Vec::new();
        results.as_object().unwrap().get("list").unwrap().as_array().unwrap().iter().for_each(|x| {
            hosts.push(x.as_str().unwrap().to_string());
        });
        hosts
    }

    pub fn host_tree(&mut self) -> Vec<String> {
        self.client.url = self.client.url.join("/JSON/host/view/tree/").unwrap();
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        let mut hosts = Vec::new();
        results.as_object().unwrap().get("tree").unwrap().as_array().unwrap().iter().for_each(|x| {
            hosts.push(x.as_str().unwrap().to_string());
        });
        hosts
    }

    pub fn child_id(&mut self,id: String) -> String {
        self.client.url = self.client.url.join("/JSON/request/view/id/").unwrap();
        self.client.body = Some(format!("id={}",id));
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("id").unwrap().as_str().unwrap().to_string()
    }

    pub fn request_id(&mut self,id: String) -> String {
        self.client.url = self.client.url.join("/JSON/request/view/id/").unwrap();
        self.client.body = Some(format!("id={}",id));
        self.client.send();
        let results: Value = from_str(self.client.response.as_ref().unwrap().as_str()).unwrap();
        results.as_object().unwrap().get("id").unwrap().as_str().unwrap().to_string()
    }


}

pub fn zap_proxy(reqs: Vec<String>) -> Vec<String> {
    let mut zap_proxy_reqs = Vec::new();
    for req in reqs {
        if req.contains("zap_proxy") {
            zap_proxy_reqs.push(req);
        }
    }
    zap_proxy_reqs
}


