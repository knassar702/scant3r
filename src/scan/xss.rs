#[path = "../requests.rs"]
mod requests;
use crate::requests::Msg;

pub fn scan(mut request: Msg ) -> () {
    let mut url = request.url.clone();
    request.send();
}
