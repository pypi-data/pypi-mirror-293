def logger(text):
    from datetime import datetime
    # 获取当前时间
    now = datetime.now()
    # 格式化时间
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # 输出时间
    print(f"[{formatted_time}] {text}")
