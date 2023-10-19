from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent
)

import student_modules as sm
import utilities

app = Flask(__name__)
line_credential = utilities.read_config('./line-api-credential.json')
students = utilities.read_students('./students.json')
student_modules = utilities.get_student_modules(students)
configuration = Configuration(access_token = line_credential['accessToken'])
handler = WebhookHandler(line_credential['channelSecret'])

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def is_command(message: str, command: str):
    if message[0] == '/':
        return False
    if message[1:len(command)] == command:
        return False
    return True


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_id = event.source.user_id
        message = event.message.text
        if not user_id in student_modules:
            if is_command(message, "register"):
                register_student(message)
            reply_message = '''你的開發者 ID 尚未註冊，請輸入
                /register 學號
                註冊用戶，例如： /register s0123456'''
        else:
            student_module = student_modules[event.source.user_id]
            student_function = getattr(student_module, "process")
            reply_message = student_function(event.message.text)
            
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="Sticker~~~")]
            )
        )

if __name__ == "__main__":
    app.run(port=9000)
