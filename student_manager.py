import re
import gspread
from bot_command.command_base import BotCommand

class StudentManager:
    def __init__(self, credential_path: str = 'sheet-api-credential.json') -> None:
        self.worksheet = None
        self.students: dict = {}
        self.stu_no_pattern = r"^[Ss]\d{6,7}$"
        self.init_worksheet(credential_path)
        self.init_students()

    def init_worksheet(self, credential_path: str) -> None:
        service_account = gspread.service_account(filename = credential_path)
        work_book = service_account.open("資訊科技 Sheet 應用") # title: sheet title, NOT tab name
        self.worksheet = work_book.worksheet("LINE bot users") # title: now, it's TAB name

    def init_students(self) -> None:
        sheet_rows = self.worksheet.get_all_records()
        for row in sheet_rows: # skip header
            if len(row) < 5 or not row["開發者ID"]:
                continue
            user_id = row["開發者ID"]
            self.students[user_id] = {
                "class_unit": row["班級"],
                "seat_no": row["座號"],
                "name": row["姓名"],
                "student_no": row["學號"],
            }

    def register_student(self, command_obj: BotCommand) -> str:
        arguments = command_obj.arguments
        if len(arguments) != 4:
            return "註冊指令需要班級、座號、姓名、學號，範例：\n/register 高一0 99 竹山金城武 s0123456"
        if not arguments[0]:
            return "班級不可為空"
        if not arguments[1]:
            return "座號不可為空"
        if not arguments[2]:
            return "姓名不可為空"
        if not arguments[3]:
            return "學號不可為空"
        class_unit = arguments[0]
        seat_no = arguments[1]
        name = arguments[2]
        student_no = arguments[3]
        if not self.is_valide_student_no(student_no):
            return "學號格式有誤"
        if self.is_student_registered(command_obj.user_id):
            return "你已經註冊過"
        row = [
            class_unit,
            seat_no,
            name,
            student_no,
            command_obj.user_id
        ]
        self.worksheet.append_row(row)
        self.reload_student_data()
        return "註冊完成~"

    def is_student_registered(self, user_id: str) -> bool:
        return user_id in self.students

    def is_valide_student_no(self, student_no: str) -> bool:
        return re.match(self.stu_no_pattern, student_no)
    
    def reload_student_data(self) -> None:
        self.init_students()

    def get_student(self, user_id: str) -> dict:
        if not self.is_student_registered(user_id):
            return None
        return self.students[user_id]
