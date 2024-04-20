import re


def is_valid_ip(ip: str):
    match = re.match(
        r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):\d{4,5}$", ip)
    return match is not None and all(map(lambda subnet: 0 <= int(subnet) <= 255, match.groups()))
