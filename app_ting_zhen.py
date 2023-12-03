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

from student_manager import StudentManager
from bot_command.command_base import BotCommand
from bot_command.command_processors import BotCommandProcessor
from caesar_cipher.caesar_cipher import CaesarCipher
import utilities
from datetime import datetime
import random
app = Flask(__name__)
line_credential = utilities.read_config('./line-api-credential.json')
students = utilities.read_students('./students.json')
student_modules = utilities.get_student_modules(students)
stu_manager = StudentManager()
configuration = Configuration(access_token = line_credential['accessToken'])
handler = WebhookHandler(line_credential['channelSecret'])
command_processor = BotCommandProcessor(stu_manager)
cipher = CaesarCipher()

d = {}
@app.route("/inservice/caesar-cipher", methods=['GET'])
def inservice_handler():
    cmd = request.args.get('cmd').lower()
    if cmd == "answer":
        ans = request.args.get("ans")
        if ans == cipher.get_plaintext():
            time_string = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
            return f"Correct!,{time_string}"
        else:
            return "try again"
    elif cmd == "query":
        return cipher.get_question()
    elif cmd == "system-next":
        mode = request.args.get('mode').lower()
        cipher.next_question(mode == "advanced")
        cipher.encrypt()
        return "ok"
    elif cmd == "system-reload":
        cipher.reload_words()
    else:
        abort(400)

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

def is_group_event(event: dict) -> bool:
    return hasattr(event.source, "group_id")

def get_command_obj(user_id: str, message: str) -> BotCommand:
    if message[0] != '/':
        return None
    return BotCommand(user_id, message)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):  #這裡可以改
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client) #主要運作實體
        user_id = event.source.user_id          #專屬ip
        message = event.message.text            #傳過來的訊息文字
        reply_message = message                 #回復訊息


        if message == "開始":
            d[user_id]={
            "count": 0,
            "min_num" : 0, 
            "max_num" : 100, 
            "answer" : random.randint(0, 100)
        } 
            reply_message = "請敲出0到100的數字:" 
        elif user_id in d:
            if d[user_id] is None:
                print("若要重新開始再輸入\"開始\"")
            elif d[user_id] is not None:
                
                d[user_id]["count"] = d[user_id]["count"] + 1
                count = d[user_id]["count"]
                min_num = d[user_id]["min_num"]
                max_num = d[user_id]["max_num"]
                answer = d[user_id]["answer"]
                d[user_id]["num"] = int(message)
                num = d[user_id]["num"]

                if num > max_num or num < min_num:
                    reply_message = "不在範圍內，再輸一次 ε٩(๑> ₃ <)۶з"
                else:
                    if num > answer:
                        d[user_id]["max_num"] = num
                        reply_message = "請敲出 %d 到 %d 的數字:" % (d[user_id]["min_num"], d[user_id]["max_num"])
                    elif num < answer:
                        d[user_id]["min_num"] = num
                        reply_message = "請敲出 %d 到 %d 的數字:" % (d[user_id]["min_num"], d[user_id]["max_num"])
                    elif num == answer:
                        reply_message = "答案是%d你猜對了~~真蚌 你用了 %d 次" %(answer, count)
                        d[user_id] = None


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
                messages=[TextMessage(text="""遊戲剛法如下：
當輸入"開始"，即可開始猜數字到猜對。
猜對使用次數越少越好!!
看懂的話就開始遊戲八!""")]
            )
        )

if __name__ == "__main__":
    app.run(port=9001)
