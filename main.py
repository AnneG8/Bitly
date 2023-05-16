from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import os
import argparse


def get_bitlink_path(link):
    parsed = urlparse(link)
    return f"{parsed.netloc}{parsed.path}"


def is_bitlink(token, url):
    bitlink = get_bitlink_path(url)
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def shorten_link(token, url):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "long_url": url
    }
    response = requests.post(bitly_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, link):
    bitlink = get_bitlink_path(link)
    bitly_url = (f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
                 "/clicks/summary?unit=day&units=-1")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    url = parser.parse_args().url
    if(is_bitlink(token, url)):
        clicks_count = count_clicks(token, url)
        print(f"По вашей ссылке прошли {clicks_count} раз(а)")
    else:
        try:
            bitlink = shorten_link(token, url)
            print("Битлинк: ", bitlink)
        except requests.exceptions.HTTPError as err:
            print(f"Невозможно получить ответ, {err}")


if __name__ == "__main__":
    main()
