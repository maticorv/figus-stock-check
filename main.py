import requests
import logging
import os
from lxml import html
from lxml.html import HtmlElement
from dotenv import load_dotenv

load_dotenv()
URL = os.environ["URL"]
DOCUMENT_ID = os.environ["DOCUMENT_ID"]
# TELEGRAM
bot_token = os.environ["bot_token"]
chat_id = os.environ["chat_id"]


def get_stock() -> None:
    try:
        res = requests.get(URL)
        data: HtmlElement = html.fromstring(res.content)
        value = data.xpath("//form[@id='product_form']//input[@type='submit']/@value")[0]
        if isinstance(value, str):
            if value != "SIN STOCK":
                # post_telegram(post_status(value))
                # post_telegram(post_status(value))
                print('No hay stock')
            else:
                post_telegram(post_status(value))
        else:
            post_telegram(f"🔴 Cannot read value")

    except Exception as e:
        post_telegram(f"🔴 Cannot read value")


def post_status(value: str) -> str:
    try:
        if value.upper() == "SIN STOCK":
            telegram_text = "🔴 STOCK AGOTADO 🔴\nEl pack x25 sobres de figuritas del mundial se encuentra agotado."
        else:
            telegram_text = f"🟢 HAY STOCK 🟢\nEl pack x25 sobres de figuritas del mundial se encuentra con stock disponible.\n Conseguilo en {URL}"
        return post_telegram(telegram_text)
    
    except Exception as e:
        logging.error({'level': 'ERROR', 'message': 'Error telegraming.', 'exception': str(e), 'name': 'check_stock_function'})
        return None


def post_telegram(telegram_text: str) -> str:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={telegram_text}"
    payload = {}
    headers = {}
    request = requests.request("GET", url, headers=headers, data=payload)
    return request.text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_stock()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
