pub mod scan;
pub use urlencoding::encode as url_encode;

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }

    #[test]
    fn test_urlencode() {
        let url = "http://www.google.com/search?q=rust+language";
        let encoded = super::url_encode(url);
        assert_eq!(
            encoded,
            "http%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Drust%2Blanguage"
        );
    }
}
