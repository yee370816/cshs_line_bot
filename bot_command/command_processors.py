from bot_command.command_base import BotCommand, SYSTEM_COMMANDS
from student_manager import StudentManager

SYSTEM_COMMANDS = {
    "/help",
    "/register",
    "/id",
    "/token",
}


class BotCommandProcessor:
    def __init__(self, stu_manager: StudentManager) -> None:
        self.stu_manager = stu_manager
        self.command_processors = {
            "/register": self.process_register,
            "/help": self.process_help,
            "/id": self.process_show_id,
            "/token": self.process_show_token,
        }
    def process_register(self, command_obj: BotCommand) -> str:
        try:
            result = self.stu_manager.register_student(command_obj)
            return result
        except Exception as ex:
            return str(ex)

    def process_help(self, command_obj: dict) -> str:
        return ''' === 當前版本系統指令 ===
        【顯示說明】 /help
        【註冊用戶】 /register 班級 座號 姓名 學號
        【顯示開發者ID】 /id 
        【顯示 API 金鑰】 /token api名稱
        '''

    def process_show_id(self, command_obj: BotCommand) -> str:
        return f"你的開發者ID是\n{command_obj.user_id}"

    def process_show_token(self, command_obj: BotCommand) -> str:
        pass
        

    def is_system_command(self, command_obj: BotCommand) -> bool:
        if command_obj.command in SYSTEM_COMMANDS:
            return True
        return False

    def get_command_object(self, message: str, user_id: str) -> dict:
        if not message or message[0] != '/':
            return None
        obj = {}
        message_values = message.split(' ')
        obj["command"] = message_values[0]
        obj["user_id"] = user_id
        obj["arguments"] = message_values[1:]


    def process_system_command(self, command_obj: BotCommand) -> str:
        if not self.is_system_command(command_obj):
            return "錯誤: 此訊息非系統指令"
        action = self.command_processors[command_obj.command]
        result = action(command_obj)
        return result
