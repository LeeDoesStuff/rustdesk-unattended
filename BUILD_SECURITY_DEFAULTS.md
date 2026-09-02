# Build-time security defaults

## Initialize `hbb_common`

```powershell
cd D:\burger\BurgerTop
git submodule update --init libs/hbb_common
cd libs\hbb_common
git switch -c codex/security-defaults
```

## Configure authentication and access

In `D:\burger\BurgerTop\libs\hbb_common\src\config.rs`, replace the declarations of `DEFAULT_SETTINGS`, `OVERWRITE_SETTINGS`, `HARD_SETTINGS`, and `BUILTIN_SETTINGS` with the following code:

```rust
pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> =
    RwLock::new(HashMap::from([
        (
            "approve-mode".to_owned(),
            "password".to_owned(),
        ),
        (
            "verification-method".to_owned(),
            "use-permanent-password".to_owned(),
        ),
        (
            "temporary-password-length".to_owned(),
            "8".to_owned(),
        ),
        (
            "access-mode".to_owned(),
            "full".to_owned(),
        ),
    ]));

pub static ref OVERWRITE_SETTINGS: RwLock<HashMap<String, String>> =
    RwLock::new(HashMap::from([
        (
            "approve-mode".to_owned(),
            "password".to_owned(),
        ),
        (
            "verification-method".to_owned(),
            "use-permanent-password".to_owned(),
        ),
        (
            "access-mode".to_owned(),
            "full".to_owned(),
        ),
    ]));

pub static ref HARD_SETTINGS: RwLock<HashMap<String, String>> =
    RwLock::new(HashMap::from([
        (
            "password".to_owned(),
            "REPLACE_WITH_GENERATED_PASSWORD_STORAGE".to_owned(),
        ),
        (
            "salt".to_owned(),
            "REPLACE_WITH_GENERATED_SALT".to_owned(),
        ),
    ]));

pub static ref BUILTIN_SETTINGS: RwLock<HashMap<String, String>> =
    RwLock::new(HashMap::from([
        (
            "disable-change-permanent-password".to_owned(),
            "Y".to_owned(),
        ),
    ]));
```

## Generate the permanent-password storage and salt

Set `$password` to the permanent password that will ship with the build, then run:

```powershell
$password = "REPLACE_WITH_THE_PERMANENT_PASSWORD"

$saltBytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($saltBytes)
$rng.Dispose()
$salt = [Convert]::ToBase64String($saltBytes)

$inputBytes = [Text.Encoding]::UTF8.GetBytes($password + $salt)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$hashBytes = $sha256.ComputeHash($inputBytes)
$sha256.Dispose()
$storage = "00" + [Convert]::ToBase64String($hashBytes)

Write-Output "password storage: $storage"
Write-Output "salt: $salt"
```

Replace `REPLACE_WITH_GENERATED_PASSWORD_STORAGE` and `REPLACE_WITH_GENERATED_SALT` in `config.rs` with the two generated values. Do not put the plaintext password in the Rust source.

## Commit the submodule change

```powershell
cd D:\burger\BurgerTop\libs\hbb_common
git add src\config.rs
git commit -m "Set compiled security defaults"

cd D:\burger\BurgerTop
git add libs\hbb_common
git commit -m "Use customized hbb_common security defaults"
```

Build RustDesk through the repository's normal build process and validate the result with a clean RustDesk configuration directory.
