use scraper::Html;
use scraper::Selector;

#[derive(Debug, Clone)]
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
    println!("{:?}", pattern);
    let select = Selector::parse(pattern).unwrap();
    for node in document.select(&select) {
        found.push_str(&node.html());
    }
    found
}

pub fn css_selector(html: &str) -> String {
    let mut found = String::new();
    let document = Html::parse_document(html);
    document.tree.values().for_each(|node| {
        if node.as_element().is_some() {
            let element = node.as_element().unwrap();
            let mut search = format!("{}", element.name());
            element.attrs.iter().for_each(|attr| {
                search.push_str(&format!(
                    "[{}='{}']",
                    attr.0.local.to_string(),
                    attr.1.to_string().replace("'", "\\'").replace("\"", "\\\"")
                ));
            });
            if search.contains("[") {
                found.push_str(&search);
            }
        }
    });
    found
}

pub fn html_parse(html: &str, payload: &str) -> Vec<Location> {
    let mut found: Vec<Location> = Vec::new();
    if payload.len() == 0 {
        return found;
    }
    let document = Html::parse_document(html);
    document.tree.values().for_each(|node| {
        if node.is_text() {
            let text = node.as_text().unwrap();
            if text.contains(payload) {
                found.push(Location::Text(text.to_string()));
            }
        } else if node.is_element() {
            let element = node.as_element().unwrap();
            if element.name().contains(payload) {
                found.push(Location::TagName(element.name().to_string()));
            }
            element.attrs().for_each(|attr| {
                if attr.1.contains(payload) {
                    found.push(Location::AttrValue(attr.1.to_string()));
                }
                if attr.0.contains(payload) {
                    found.push(Location::AttrName(attr.0.to_string()));
                }
            });
        } else if node.is_comment() {
            let comment = node.as_comment().unwrap();
            if comment.contains(payload) {
                found.push(Location::Comment(comment.to_string()));
            }
        }
    });
    found
}
