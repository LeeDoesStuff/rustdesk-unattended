use crate::ui_interface::{self, UiStatus};
use hbb_common::config::Config;
use std::{
    sync::mpsc,
    time::{Duration, Instant},
};

const STATUS_WAIT: Duration = Duration::from_secs(3);

pub fn run() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if matches!(args.first().map(String::as_str), Some("-h" | "--help")) {
        print_help();
        return;
    }
    if matches!(args.first().map(String::as_str), Some("--status")) {
        print_status();
        return;
    }

    let serve = args.is_empty();
    if crate::core_main::core_main().is_none() {
        crate::common::global_clean();
        return;
    }
    if !serve {
        eprintln!(
            "This CLI does not provide graphical outgoing connections. Run with --help for usage."
        );
        crate::common::global_clean();
        std::process::exit(2);
    }

    ui_interface::start_option_status_sync();
    println!("BurgerTop is starting in the background. Press Ctrl+C to stop.");

    let (stop_tx, stop_rx) = mpsc::channel();
    if let Err(error) = ctrlc::set_handler(move || {
        let _ = stop_tx.send(());
    }) {
        eprintln!("Unable to register the shutdown handler: {error}");
    }

    let mut last_status = None;
    loop {
        let status = ui_interface::get_connect_status();
        let current = status_text(&status);
        if last_status.as_deref() != Some(current) {
            if current == "Ready" {
                println!("Ready: {} can accept incoming connections.", status.id);
            } else {
                println!("{current}");
            }
            last_status = Some(current.to_owned());
        }
        if stop_rx.recv_timeout(Duration::from_secs(1)).is_ok() {
            break;
        }
    }

    crate::common::global_clean();
}

pub(crate) fn enable_incoming_service() {
    Config::set_option("stop-service".to_owned(), String::new());
}

fn print_status() {
    if !crate::common::global_init() {
        eprintln!("Global initialization failed.");
        std::process::exit(1);
    }
    crate::load_custom_client();
    hbb_common::init_log(false, "status");
    ui_interface::start_option_status_sync();

    let deadline = Instant::now() + STATUS_WAIT;
    let mut status = ui_interface::get_connect_status();
    while status_text(&status) == "Connecting" && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(100));
        status = ui_interface::get_connect_status();
    }

    println!("{}", status_text(&status));
    if !status.id.is_empty() {
        println!("ID: {}", status.id);
    }
    crate::common::global_clean();
}

fn status_text(status: &UiStatus) -> &'static str {
    if status.status_num > 0 && status.key_confirmed && !status.id.is_empty() {
        "Ready"
    } else if status.status_num < 0 {
        "Offline"
    } else {
        "Connecting"
    }
}

fn print_help() {
    println!(
        "BurgerTop command-line service\n\n\
         Usage:\n  burgertop              Start the incoming-connection service\n  \
         burgertop --status     Show service readiness\n  \
         burgertop --get-id     Print this device's ID\n  \
         burgertop --version    Print the version\n  \
         burgertop --help       Show this help"
    );
}
