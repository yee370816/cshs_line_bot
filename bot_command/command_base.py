SYSTEM_COMMANDS = {
    "/help",
    "/register",
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
