use scraper::Html;
use scraper::Selector;

#[derive(Debug)]
pub enum Location {
    AttrValue(String),
    AttrName(String),
    TagName(String),
    Text(String),
    Comment(String),
}

pub fn html_search(html: &str, pattern: &str) -> String {
    let mut found = String::new();
    let document = Html::parse_document(html);
    let Select = Selector::parse(r#"img[onerror="alert()"]"#).unwrap();
    for node in document.select(&Select){
        found.push_str(&node.html());
    }
    found
}

pub fn parse(html: &str,payload: String) -> Vec<Location> {
    let mut Found: Vec<Location> = Vec::new();
    if payload.len() == 0 {
        println!("BRUH");
        return Found;
    }
    let document = Html::parse_document(html);
    document.tree.values().for_each(|node| {
        // find_payloadword in the html without the tag name
        if node.is_text() {
            let text = node.as_text().unwrap();
            if text.contains(payload.as_str()) {
                Found.push(Location::Text(text.to_string()));
            }
        } else if node.is_element() {
            let element = node.as_element().unwrap();
            element.attrs().for_each(|attr| {
                if attr.1.contains(payload.as_str()) {
                    
                    Found.push(Location::AttrValue(attr.1.to_string()));
                }
                if attr.0.contains(payload.as_str()) {
                    Found.push(Location::AttrName(attr.0.to_string()));
                }
            });

        } else if node.is_comment() {
            let comment = node.as_comment().unwrap();
            if comment.contains(payload.as_str()) {
                Found.push(Location::Comment(comment.to_string()));
                
            }
        }
    });
    Found

}
