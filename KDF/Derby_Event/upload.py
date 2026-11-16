"""Optional EasyAPI.io upload adapter for the archived upload prototype.

The SDK is not part of the active web runtime. Import it lazily only when this
adapter is explicitly called, and keep credentials in the environment.
"""
import os
from pathlib import Path


def upload_file(file_path):
    api_key = os.environ.get("EASYAPI_API_KEY")
    app_id = os.environ.get("EASYAPI_APP_ID")
    if not api_key or not app_id:
        raise RuntimeError("Set EASYAPI_API_KEY and EASYAPI_APP_ID to enable this optional adapter.")

    try:
        import easyapiio
    except ImportError as exc:
        raise RuntimeError(
            "The optional easyapiio package is not installed. It is not part of the web runtime."
        ) from exc

    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(str(path))

    client = easyapiio.File(api_key, app_id)
    with path.open("rb") as source:
        result = client.upload(source)

    if not result.get("success"):
        raise RuntimeError(result.get("message", "The upload provider rejected the file."))
    return result["file"]["id"]


def delete_file(file_id):
    api_key = os.environ.get("EASYAPI_API_KEY")
    app_id = os.environ.get("EASYAPI_APP_ID")
    if not api_key or not app_id:
        raise RuntimeError("Set EASYAPI_API_KEY and EASYAPI_APP_ID to enable this optional adapter.")

    try:
        import easyapiio
    except ImportError as exc:
        raise RuntimeError(
            "The optional easyapiio package is not installed. It is not part of the web runtime."
        ) from exc

    result = easyapiio.File(api_key, app_id).delete(file_id)
    if not result.get("success"):
        raise RuntimeError(result.get("message", "The upload provider rejected the delete request."))
    return result
