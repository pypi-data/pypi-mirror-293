import logging
import os
import time
from datetime import datetime, timedelta

class CustomTimedRotatingFileHandler(logging.Handler):
    def __init__(self, filename, days=7, when='H', interval=1, backupCount=0, encoding=None):
        super().__init__()
        self.baseFilename = filename
        self.when = when.upper()
        self.interval = interval
        self.backupCount = backupCount
        self.encoding = encoding
        self.current_filename = self._get_current_filename()
        self.days = days
        
        # 确保日志目录存在
        log_dir = os.path.dirname(self.current_filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.stream = open(self.current_filename, 'a', encoding=encoding)
        self.rollover_at = self.compute_next_rollover()

    def _get_current_filename(self):
        """
        获取当前日志文件名，带有时间戳。
        """
        date_str = datetime.now().strftime("%Y-%m-%d_%H")
        return f"{self.baseFilename}.{date_str}.log"

    def compute_next_rollover(self):
        """
        计算下一个日志切割的时间点。
        """
        current_time = time.time()
        if self.when == 'S':
            interval = 1  # 秒
        elif self.when == 'M':
            interval = 60  # 分钟
        elif self.when == 'H':
            interval = 3600  # 小时
        else:
            raise ValueError(f"Unsupported interval: {self.when}")

        return current_time + interval

    def doRollover(self):
        """
        执行日志文件切割。
        """
        if self.stream:
            self.stream.close()

        # 生成新的日志文件名
        self.current_filename = self._get_current_filename()
        
        # 确保日志目录存在
        log_dir = os.path.dirname(self.current_filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.stream = open(self.current_filename, 'a', encoding=self.encoding)

        # 清理旧日志文件
        self.cleanup_old_logs()

    def cleanup_old_logs(self):
        """
        删除days天前的日志文件。
        """
        cutoff_time = datetime.now() - timedelta(days=self.days)
        log_dir = os.path.dirname(self.baseFilename)
        if not log_dir:
            log_dir = "."
        base_filename = os.path.basename(self.baseFilename)

        for filename in os.listdir(log_dir):
            if filename.startswith(base_filename) and filename.endswith('.log'):
                try:
                    date_str = filename[len(base_filename) + 1:-4]
                    log_time = datetime.strptime(date_str, "%Y-%m-%d_%H")
                    if log_time < cutoff_time:
                        os.remove(os.path.join(log_dir, filename))
                except ValueError:
                    continue

    def emit(self, record):
        """
        处理日志记录，按需执行日志文件切割。
        """
        if time.time() >= self.rollover_at:
            self.doRollover()
            self.rollover_at = self.compute_next_rollover()

        msg = self.format(record)
        self.stream.write(msg + '\n')
        self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()

# # 设置日志记录器
# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.INFO)

# # 设置自定义处理器，按小时切割日志文件，并仅保留7天的日志
# log_file_handler = CustomTimedRotatingFileHandler('my_log_file', days=7, when='H', interval=1)
# logger.addHandler(log_file_handler)

# # 设置日志格式
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# log_file_handler.setFormatter(formatter)

# # 示例日志输出
# for i in range(100):
#     logger.info(f'This is log message number {i}')
#     time.sleep(0.2)  # 模拟实际运行的时间延迟
