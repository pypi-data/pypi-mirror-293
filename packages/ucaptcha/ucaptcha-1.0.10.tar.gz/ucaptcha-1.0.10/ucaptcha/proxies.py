import re


def get_proxy_parts(proxy: str | None):
    if proxy is None:
        return None
    match = re.search("(http)://(.+):(.+)@(.+):([0-9]+)", proxy)
    if match is not None:
        return {
            "type": match.group(1),
            "username": match.group(2),
            "password": match.group(3),
            "address": match.group(4),
            "port": int(match.group(5)),
        }
    match = re.search("(http)://(.+):([0-9]+)", proxy)
    if match is not None:
        return {
            "type": match.group(1),
            "address": match.group(2),
            "port": int(match.group(3)),
        }
    return None
