use std::collections::HashMap;

pub struct Injector {
    pub request: url::Url,
}


impl Injector {
    pub fn url_parameters(&self,_payload: &str) -> HashMap<String,Vec<url::Url>> {
        let url = self.request.clone();
        let params: HashMap<_,_> = url.query_pairs().collect::<HashMap<_, _>>();
        let mut scan_params = HashMap::new();
        let mut bruh: HashMap<String,Vec<url::Url>> = HashMap::new();
        let mut param_list = Vec::new();
        for (key, value) in params.iter() {
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

}
