import requests
from imgurpython import ImgurClient
from flask import Flask, request, abort
import random
from bs4 import BeautifulSoup

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Ei/WOOrisR5p5uAT/BLGqJNGIxuOD9Yi1+Yno4RlCMnc0uq0Jgfq6N87ogRFooq+sJ98jZrhs1x9wQsuxxtosKDjg87iTgOVopcGIZkx/ey9GKocn4/wdAdS3Bh0Hd0OlcJiqGzbmfJtCNlIrpoN4gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('37253c41163b45d32286ad1ebe8b8893')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    client_id = 'de5ecd12cacaf0a'
    client_secret = '3556bb208ceda936f8c53033b861041cb878d878	'
    client = ImgurClient(client_id, client_secret)
    a = client.get_account_albums("kevin86117")
    images = client.get_album_images(a[0].id)
    index = random.randint(0, len(images) - 1)
    url = images[index].link
    if event.message.text == "corgi" or event.message.text == "柯基":
        message = ImageSendMessage(
            original_content_url= url,
            preview_image_url=  url
        )
    elif event.message.text == "news":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
