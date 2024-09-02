from typing import Literal

from ucaptcha.nopecha import solve_nopecha

from .anticaptcha import solve_anticaptcha
from .capmonster import solve_capmonster
from .nocaptchaai import solve_nocaptchaai

CaptchaService = Literal[
    "anti-captcha",
    "capmonster",
    "nocaptchaai",
    "nopecha",
]


def solve_captcha(
    service: CaptchaService,
    api_key: str,
    site_key: str,
    url: str,
    user_agent: str,
    rqdata: str,
    proxy: str | None = None,
    proxy_ip: str | None = None,
    cookies: dict[str, str] | None = None,
    extra_data: dict[str, str] | None = None,
):
    if service == "anti-captcha":
        return solve_anticaptcha(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
        )
    if service == "capmonster":
        return solve_capmonster(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            cookies,
            extra_data,
        )
    if service == "nocaptchaai":
        return solve_nocaptchaai(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
        )
    if service == "nopecha":
        return solve_nopecha(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
        )
    raise NotImplementedError(f"{service} captcha service is not implemented.")
