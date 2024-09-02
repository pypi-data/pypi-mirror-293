import json
import time
from typing import Any

import requests

from ucaptcha import logger
from ucaptcha.exceptions import CaptchaException
from ucaptcha.proxies import get_proxy_parts


def solve_nopecha(
    api_key: str,
    site_key: str,
    url: str,
    user_agent: str,
    rqdata: str,
    proxy: str | None = None,
    proxy_ip: str | None = None,
    extra_data: dict[str, Any] | None = None,
):
    logger.info("Initiating captcha task...")
    parts = get_proxy_parts(proxy)

    data: dict[str, Any] = {
        "key": api_key,
        "type": "hcaptcha",
        "url": url,
        "sitekey": site_key,
        "data": {"rqdata": rqdata},
        "useragent": user_agent,
    }

    if proxy is not None and proxy_ip is not None and parts is not None:
        data["proxy"] = {
            "host": proxy_ip,
            "port": parts["port"],
            "scheme": parts["type"],
        }

        if "username" in parts:
            data["proxy"]["username"] = parts["username"]
        if "password" in parts:
            data["proxy"]["password"] = parts["password"]

    if extra_data is not None:
        data.update(extra_data)

    request_url = "https://api.nopecha.com/token/"
    try:
        res = requests.post(request_url, json=data, timeout=300)
        logger.debug(f"{res.status_code}, {res.text}")
        if not res.ok:
            raise CaptchaException(f"{res.status_code}, {res.text}")
        data = res.json()
        logger.debug(data)
        if "data" in data:
            task_id = data["data"]
        else:
            raise CaptchaException(f"{res.status_code}, {res.text}")

        time.sleep(7)

    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return None

    task_url = f"https://api.nopecha.com/token/?key={api_key}&id={task_id}"

    while True:
        try:
            res = requests.get(task_url, timeout=300)
            logger.debug(f"{res.status_code}, {res.text}")
            if res.status_code == 409:
                if "Incomplete job" in res.text:
                    logger.info("Captcha not ready...")
                    time.sleep(10)
                    continue
            if not res.ok:
                raise CaptchaException(f"{res.status_code}, {res.text}")
            data = res.json()

            if "data" in data:
                logger.info("Captcha ready.")
                return data["data"]

            raise CaptchaException(f"{res.status_code}, {res.text}")

        except (requests.exceptions.RequestException, json.JSONDecodeError):
            logger.exception("Failed to solve catpcha.")
            time.sleep(10)
            continue
