import os
import sys
from importlib import resources
from io import StringIO

import oss2
from dotenv import load_dotenv


def resource_path(relative_path: str):
    """Get absolute path to resource (works for dev & PyInstaller exe)"""
    base_path = getattr(sys, "_MEIPASS", None)
    if not base_path:
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)


def _load_env_file() -> bool:
    """Attempt to load the packaged .env first, then fallback to defaults."""
    env_path = resource_path(".env")
    loaded = False

    if os.path.exists(env_path):
        loaded = load_dotenv(env_path)

    if not loaded:
        exe_env = None
        if getattr(sys, "frozen", False):
            exe_env = os.path.join(os.path.dirname(sys.executable), ".env")
        else:
            exe_env = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".env")
        if exe_env and os.path.exists(exe_env):
            loaded = load_dotenv(exe_env, override=False)

    if not loaded:
        try:
            with resources.files("desktop").joinpath(".env").open("r", encoding="utf-8") as handle:
                loaded = load_dotenv(stream=StringIO(handle.read()), override=False)
        except (FileNotFoundError, ModuleNotFoundError, AttributeError):
            loaded = False

    if not loaded:
        import pkgutil

        try:
            data = pkgutil.get_data("desktop", ".env")
        except Exception:
            data = None
        if data:
            loaded = load_dotenv(stream=StringIO(data.decode("utf-8")), override=False)

    if not loaded:
        # Fallback to the usual resolution (current dir, parent dirs, etc.)
        loaded = load_dotenv()

    return loaded

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(
            f"Missing required environment variable '{name}'. Ensure your credentials are set "
            "in the environment or packaged .env file."
        )
    return value.strip()


_load_env_file()

ACCESS_KEY_ID = _require_env('OSS_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = _require_env('OSS_ACCESS_KEY_SECRET')
ENDPOINT = _require_env('OSS_ENDPOINT')
BUCKET_NAME = _require_env('OSS_BUCKET')


# Auth & Bucket instance
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def upload_file(local_path, oss_key) -> bool:
    """
    Upload a file to OSS with AES256 encryption
    :param local_path: Local file path (e.g. ./images/tool123.png)
    :param oss_key: OSS path (e.g. uploads/tool123.png)
    :return: True if success, False if failed
    """

    if not os.path.exists(local_path):
        print(f"[ERROR] File not found: {local_path}")
        return False

    try:
        result = bucket.put_object_from_file(
            oss_key,
            local_path,
            headers={"x-oss-server-side-encryption": "AES256"},
        )

        if result.status in (200, 204, 201):
            print(f"[OK] Uploaded: {oss_key}")
            return True
        else:
            print(f"[FAIL] Upload failed: {result.status}")
            return False

    except Exception as e:
        print(f"[EXCEPTION] Upload error: {e}")
        return False


def generate_signed_url(oss_key, expires_in_seconds=600) -> str:
    """
    Generate a signed download URL (expires in X seconds)
    :param oss_key: File path in OSS
    :param expires_in_seconds: Validity duration (default 10 mins)
    :return: URL string
    """
    try:
        url = bucket.sign_url('GET', oss_key, expires_in_seconds)
        print(f"[URL] Signed URL: {url}")
        return url
    except Exception as e:
        print(f"[EXCEPTION] Signed URL error: {e}")
        return None
