from curl_cffi import requests

TELEGRAM_UA = "TelegramBot"


def is_url_has_image(url: str) -> None:
    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=5,
            headers={
                "User-Agent": TELEGRAM_UA,
                "Range": "bytes=0-0",
            },
        )
        if response.status_code >= 400:
            raise ValueError("URL недоступний")

        ct = response.headers.get("Content-Type", "")

        if not ct.startswith("image/"):
            raise ValueError("Не зображення")

    except Exception:
        raise ValueError(f"Помилка")
