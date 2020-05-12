from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('u4rnjIGjTPscuJ7DyrLEwPgHBdZxEsDs2+2Aa/+A2dXexmGpJbb/EUMSrOkp7ZQjCymt7Ri08zUuYsbwryt2HVcDBz7MitxnDlPtkOGvvfvWSS308DTpfk4+RUWWsyvd4UtPKcPqZjLIrGId3/YckQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e0bee310df0e564e2cef25a9d8218246')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎？':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想訂位是嗎？'
    else:
        r = '我看不懂你說什麼!!!'

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
        package_id='1',
        sticker_id='1'
    ))


if __name__ == "__main__":
    app.run()