import os
import logging
from datetime import datetime

def dir_test(): #检测日志文件夹是否存在。
    folder_path = "logs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"folder {folder_path} created.") #如果不存在，则新建。
    else:
        print(f"folder {folder_path} already exists.")

def setup_flask_logging(app):
    # 规定了log文件名格式，生成。
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"flask_app_{timestamp}.log"
    log_filepath = os.path.join('logs', log_filename)

    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 创建文件处理器
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 移除 Flask 默认的处理器（避免重复输出）
    app.logger.handlers.clear()

    # 将处理器添加到 Flask 的 logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.info(f'Flask application logging started. Log file: {log_filename}')
    app.logger.info('Flask application logging setup complete.')

    return log_filepath