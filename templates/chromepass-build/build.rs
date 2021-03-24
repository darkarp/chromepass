extern crate winres;

fn main() {
    if cfg!(target_os = "windows") {
        let mut res = winres::WindowsResource::new();
        res.set_icon("client.ico");
        match res.compile() {
            Ok(_) => println!("Build Successfull"),
            Err(err) => println!("Error: {}", err),
        }
    }
}
