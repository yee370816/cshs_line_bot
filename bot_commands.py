from student_manager import StudentManager

SYSTEM_COMMANDS = {
    "/register",
    "/help",
    "/id",
    "/token",
}

class BotCommand:
    def __init__(self, user_id: str, message: str) -> None:
        if not user_id:
            raise ValueError("必須有開發者 ID")
        if not message:
            raise ValueError("必須有指令內容")
        if message[0] != '/':
            raise ValueError("指令文字必須以 / 開頭")

        message_values = message.split(' ')
        self.user_id: str = user_id
        self.command: str = message_values[0]
        self.arguments: list = message_values[1:]
        self.is_system_command = self.command in SYSTEM_COMMANDS

stu_manager = StudentManager()

def process_register(command_obj: BotCommand) -> str:
    try:
        stu_manager.register_student(command_obj)
    except Exception as ex:
        return str(ex)

def process_help(command_obj: dict) -> str:
    pass

def process_show_id(command_obj: dict) -> str:
    pass

def process_show_token(command_obj: dict) -> str:
    pass

command_processors = {
    "/register": process_register,
    "/help": process_help,
    "/id": process_show_id,
    "/token": process_show_token,
}

def is_system_message(message: str) -> bool:
    if message[0] != '/':
        return False
    message_values = message.split(' ')
    

def is_system_command(command_obj: dict) -> bool:
    if command_obj["command"] in SYSTEM_COMMANDS:
        return True
    return False

def get_command_object(message: str, user_id: str) -> dict:
    if not message or message[0] != '/':
        return None
    obj = {}
    message_values = message.split(' ')
    obj["command"] = message_values[0]
    obj["user_id"] = user_id
    obj["arguments"] = message_values[1:]


def process_system_command(command_obj: dict) -> str:
    message:str = command_obj["message"]
    if not is_system_command(message):
        return "錯誤: 此訊息非系統指令"
    arguments = message.split(' ')
    command = arguments[0]
    action = command_processors[command]
    result = action(arguments)
    return result
