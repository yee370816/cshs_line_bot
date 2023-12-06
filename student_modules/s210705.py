def process(message: str) -> str:
    if message == "debug":
        return message
    
    # 新增一個 if 規則
    if message.startswith("計算"):
        # 判斷訊息的前兩個字是不是 "計算"
        # 如果是，進行數學運算
        expression = message[2:].strip()  # 取得 "計算" 之後的部分，並移除空白
        try:
            # 計算數學運算
            result = eval(expression)
            # 回傳數學運算的結果
            return str(result)
        except Exception as e:
            # 如果計算出現錯誤，回傳錯誤訊息
            return f"計算錯誤: {str(e)}"
    
    if message == "資訊社":
        return "讚"
    if message == "資訊老師":
        return "帥"
    if message == "資訊社的同學":
        return "棒"
    if message == "資訊社的電腦":
        return "不好說"
