#[path = "../requests.rs"]
mod requests;
use crate::requests::Msg;

pub fn scan(mut request: Msg ) {
    let url = request.url.clone();
    // get url query from url query hashmap Url
    request.url.query_pairs_mut().clear();
    url.query_pairs().for_each(|(key, value)| {
        request.url.query_pairs_mut().append_pair(&key, format!("{}<script>alert()</script>", value).as_str());
    });
    request.send();
}
