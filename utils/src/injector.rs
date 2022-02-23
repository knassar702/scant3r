use std::collections::HashMap;
use isahc::http::header::HeaderMap;
use url::Url;

pub struct Injector {
    pub request: Url,
}


pub trait url_injector {
    fn inject_map(&self, map: &mut HashMap<String, String>) -> HashMap<String,Vec<Url>>;
    fn url_parameters(&self,_payload: &str) -> HashMap<String,Vec<Url>>;
}


impl url_injector for Injector {
    fn url_parameters(&self,_payload: &str) -> HashMap<String,Vec<Url>> {
        let url = self.request.clone();
        let _params: HashMap<_,_> = url.query_pairs().collect::<HashMap<_, _>>();
        let mut scan_params = HashMap::new();
        let mut bruh: HashMap<String,Vec<Url>> = HashMap::new();
        let mut param_list = Vec::new();
        for (key, value) in _params.iter() {
            scan_params.insert(key.to_string(), value.to_string());
            param_list.push(key.to_string());
        }
        for (key, value) in scan_params.iter() {
            let mut p = Vec::new();
            for payload in _payload.split("\n") {
                let mut new_params = scan_params.clone();
                new_params.insert(key.to_string(),value.as_str().to_owned() + payload);
                let mut new_url = url.clone();
                new_url.query_pairs_mut().clear();
                new_url.query_pairs_mut().extend_pairs(&new_params);
                p.push(new_url);
//                urls.push(new_url);
            }
            bruh.insert(key.to_string(), p);
        }
        bruh
    }
    fn inject_map(&self, map: &mut HashMap<String, String>) -> HashMap<String,Vec<Url>> {
        /*
         * map: Hashmap<String,String>
         * let mut map = HashMap::new();
         * map.insert("parameter","payload")
         * */
        let url = self.request.clone();
        // map {"name":"XSS"}
        let _params: HashMap<_,_> = url.query_pairs().collect::<HashMap<_, _>>();
        let mut scan_params = HashMap::new();
        let mut testing: HashMap<String,Vec<Url>> = HashMap::new();

        for (key, value) in _params.iter() {
            scan_params.insert(key.to_string(), value.to_string());
        }
        for (key, value) in map.into_iter() {
            scan_params.insert(key.to_string(), value.to_string());
        }
        for (key, value) in _params.iter() {
            let mut p = Vec::new();
            for payload in value.split("\n") {
                let mut new_params = scan_params.clone();
                new_params.insert(key.to_string(),format!("{}{}",value,payload));
                let mut new_url = url.clone();
                new_url.query_pairs_mut().clear();
                new_url.query_pairs_mut().extend_pairs(&new_params);
                p.push(new_url);
            }
            testing.insert(key.to_string(), p);
        }
        testing
    }
}

pub trait headers_injector {
    fn header(&self,map: &mut HashMap<String,String>) -> HashMap<String,String>;
}

impl headers_injector for Injector {
    fn header(&self,map: &mut HashMap<String,String>) -> HashMap<String,String> {
        let mut testing = HeaderMap::new();
        testing.insert("TEST", isahc::http::header::HeaderValue::from_static("TEST"));
        let url = self.request.clone();
        let mut urls = Vec::new();
        let mut headers = HashMap::new();
        for (key, value) in map.iter() {
            headers.insert(key.to_string(), value.to_string());
        }
        let mut new_url = url.clone();
        new_url.query_pairs_mut().clear();
        new_url.query_pairs_mut().extend_pairs(&headers);
        urls.push(new_url);
        let mut testing = HashMap::new();
        testing
    }
}
