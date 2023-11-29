def process(message: str) -> None:
    if message == "debug":
        return message
    if message == "資訊社":
        return "讚"
    if message == "資訊老師":
        return "帥"
    if message == "資訊社的同學":
        return "棒"
    if message == "資訊社的電腦":
        return "不好說"
    else:
        return "抱歉，我不知道您在公沙小"
