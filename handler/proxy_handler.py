import os
import re
import typing
from handler.print_handler import print_main_text, print_sub_text
import simplejson as json
import requests
from model.proxy import Proxy


def get_json_proxies(output_file: str) -> typing.Dict[str, typing.List[dict]]:
    print_sub_text("Reading proxy list from " + output_file)
    with open(output_file) as json_file:
        proxy_list = json.load(json_file)

    # sorting
    proxy_obj_list = {}
    for proxy_obj in proxy_list:
        proxy_type = proxy_obj["type"].lower()
        if proxy_type not in proxy_obj_list:
            proxy_obj_list[proxy_type] = []
        proxy_obj_list[proxy_type].append(proxy_obj)

    return proxy_obj_list


def _save_proxies(proxy_obj_list: typing.Dict[str, Proxy], output_file: str):
    print_main_text("Saving proxies to " + output_file)
    proxy_json_list = []
    for ip_port, proxy_obj in proxy_obj_list.items():
        proxy_json_list.append(proxy_obj.to_json())
    with open(output_file, "w+") as outfile:
        json.dump(proxy_json_list, outfile)


def _get_shifity_proxies(url: str, proxy_type: str) -> typing.Dict[str, Proxy]:
    print_sub_text("Getting proxy list from " + url)
    proxies = requests.get(url).text
    proxy_obj_list = {}

    proxy_lines = iter(proxies.splitlines())
    for line in proxy_lines:
        ip = re.search(_pattern_ip, line).group()
        port = re.search(_pattern_port, line).group()[1:]
        proxy_obj = Proxy(ip, port)
        proxy_obj.type = proxy_type
        ip_port = str(ip) + ":" + str(port)

        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    return proxy_obj_list


def _get_shifity_list() -> typing.Dict[str, Proxy]:
    proxy_obj_list = {}
    http_url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    https_url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt"
    socks4_url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt"
    socks5_url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt"

    for ip_port, proxy_obj in _get_shifity_proxies(http_url, "HTTP").items():
        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    for ip_port, proxy_obj in _get_shifity_proxies(https_url, "HTTPS").items():
        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    for ip_port, proxy_obj in _get_shifity_proxies(socks4_url, "SOCKS4").items():
        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    for ip_port, proxy_obj in _get_shifity_proxies(socks5_url, "SOCKS5").items():
        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    return proxy_obj_list


def _get_proxyscan_list() -> typing.Dict[str, Proxy]:
    url = "https://www.proxyscan.io/api/proxy?format=json"
    print_sub_text("Getting proxy list from " + url)
    proxies = requests.get(url).json()
    proxy_obj_list = {}

    for proxy_item in proxies:
        ip = proxy_item["Ip"]
        port = proxy_item["Port"]
        country = proxy_item["Location"]["countryCode"]
        proxy_type_list = proxy_item["Type"]

        proxy_type = ""
        for proxy_type_item in proxy_type_list:
            if proxy_type == "":
                proxy_type = proxy_type_item
            else:
                proxy_type = proxy_type + " | " + proxy_type_item

        proxy_obj = Proxy(ip, port)
        proxy_obj.country = country
        proxy_obj.type = proxy_type
        ip_port = str(ip) + ":" + str(port)

        if ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    return proxy_obj_list


def _get_clarketm_list() -> typing.Dict[str, Proxy]:
    url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"
    print_sub_text("Getting proxy list from " + url)
    pattern_indicators = "(([A-Z]+)(!*)-*)+"
    pattern_google_able = "\+"

    proxies = requests.get(url)
    proxies = proxies.text[385:]  # removing header
    proxies = proxies[:-69]  # removing footer
    proxy_lines = iter(proxies.splitlines())

    proxy_obj_list = {}
    for line in proxy_lines:
        ip = re.search(_pattern_ip, line).group()
        port = re.search(_pattern_port, line).group()[1:]
        indicators = re.search(pattern_indicators, line).group().split("-")
        country = indicators[0]
        is_google_able = re.search(pattern_google_able, line)
        is_google_able = False if is_google_able is None else True
        proxy_type = indicators[2] if len(indicators) == 3 else "H"

        if "S" in proxy_type:
            proxy_type = "HTTPS"
        if "H" in [proxy_type] or ("!" in proxy_type and "S" not in proxy_type):
            proxy_type = "HTTP"

        proxy_obj = Proxy(ip, port)
        proxy_obj.country = country
        proxy_obj.type = proxy_type
        proxy_obj.google_able = is_google_able
        ip_port = str(ip) + ":" + str(port)

        if ip + ip_port not in proxy_obj_list:
            proxy_obj_list[ip_port] = proxy_obj

    return proxy_obj_list


def prepare_directory(output_file: str):
    file_name = output_file.split("/")[-1]
    dir_path = output_file.replace(file_name, "")
    os.makedirs(dir_path, exist_ok=True)


def renew_proxy_list(output_file: str):
    prepare_directory(output_file)

    _json_file_name = output_file
    print_main_text("Retrieving updated proxy list")

    proxy_list = {}

    for ip_port, proxy_obj in _get_shifity_list().items():
        if ip_port not in proxy_list:
            proxy_list[ip_port] = proxy_obj

    for ip_port, proxy_obj in _get_clarketm_list().items():
        if ip_port not in proxy_list:
            proxy_list[ip_port] = proxy_obj

    for ip_port, proxy_obj in _get_proxyscan_list().items():
        if ip_port not in proxy_list:
            proxy_list[ip_port] = proxy_obj

    print_main_text("Retrieved " + str(len(proxy_list.keys())) + " proxies")
    _save_proxies(proxy_list, output_file)


_pattern_ip = "(([0-9]+)\.)+([0-9]+)"
_pattern_port = "\:([0-9]+)"