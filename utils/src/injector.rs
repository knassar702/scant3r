use std::collections::HashMap;
use isahc::http::header::HeaderMap;
use url::Url;

pub struct Injector {
    pub request: Url,

}


pub trait Urlinjector {
    fn url_value(&self,_payload: &str) -> HashMap<String,Vec<Url>>;
    fn set_urlvalue(&self,param: &str,_payload: &str,_url: Url) -> Url;
}



impl Urlinjector for Injector {
    fn set_urlvalue(&self,param: &str,_payload: &str,_url: Url) -> Url {
        let mut url = _url.clone();
        let mut final_params = HashMap::new();

        url.query_pairs()
            .into_iter()
            .collect::<HashMap<_, _>>()
            .iter()
            .for_each(|(k,v)| {
                final_params.insert(k.clone().to_string(),v.clone().to_string());
            });
        url.query_pairs_mut().clear();
        *final_params.get_mut(param).unwrap() = _payload.to_string();


        final_params.iter()
            .for_each(|(k,v)| {
                url.query_pairs_mut().append_pair(k,v);
            });
        url

    }

    fn url_value(&self,_payload: &str) -> HashMap<String,Vec<Url>> {
        let url = self.request.clone();
        let _params: HashMap<_,_> = url.query_pairs()
                                       .collect::<HashMap<_, _>>();
        let mut scan_params = HashMap::new();
        let mut bruh: HashMap<String,Vec<Url>> = HashMap::new();
        let mut param_list = Vec::new();
        _params.iter().for_each(|(key, value)| {
            scan_params.insert(key.to_string(), value.to_string());
            param_list.push(key.to_string());
        });
        drop(_params);

        scan_params.iter().for_each(|(key, value)| {
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
        });
        bruh
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
