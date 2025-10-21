import logging
import logging.handlers
import re
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List


class ProjectLogger:
    def __init__(self, name="app", log_dir="logs", max_bytes=10 * 1024 * 1024, backup_count=5):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

        self._setup_file_handler('debug', logging.DEBUG, formatter, max_bytes, backup_count)
        self._setup_file_handler('info', logging.INFO, formatter, max_bytes, backup_count)
        self._setup_file_handler('warning', logging.WARNING, formatter, max_bytes, backup_count)
        self._setup_file_handler('error', logging.ERROR, formatter, max_bytes, backup_count)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self, level_name, level, formatter, max_bytes, backup_count):
        log_file = self.log_dir / f"{level_name}.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)

        def level_filter(record):
            return record.levelno >= level

        handler.addFilter(level_filter)

        self.logger.addHandler(handler)

    def debug(self, message, **kwargs):
        self.logger.debug(self._format_message(message, kwargs))

    def info(self, message, **kwargs):
        self.logger.info(self._format_message(message, kwargs))

    def warning(self, message, **kwargs):
        self.logger.warning(self._format_message(message, kwargs))

    def error(self, message, **kwargs):
        self.logger.error(self._format_message(message, kwargs))

    def exception(self, message, **kwargs):
        self.logger.exception(self._format_message(message, kwargs))

    @staticmethod
    def _format_message(message, extra_data):
        if extra_data:
            return f"{message} | {json.dumps(extra_data, ensure_ascii=False, default=str)}"
        return message


logger = ProjectLogger()


class LogParser:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - '
            r'(?P<name>.*?) - '
            r'(?P<level>\w+) - '
            r'(?P<file>.*?):(?P<line>\d+) - '
            r'(?P<message>.*)'
        )

    def parse_log_file(self, level: str) -> List[Dict]:
        log_file = self.log_dir / f"{level}.log"
        if not log_file.exists():
            return []

        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                match = self.log_pattern.match(line)
                if match:
                    log_data = match.groupdict()
                    message_parts = log_data['message'].split(' | ', 1)
                    log_data['message'] = message_parts[0]

                    if len(message_parts) > 1:
                        try:
                            log_data['extra'] = json.loads(message_parts[1])
                        except json.JSONDecodeError:
                            log_data['extra'] = message_parts[1]
                    else:
                        log_data['extra'] = None

                    logs.append(log_data)
                else:
                    logs.append({
                        'raw': line,
                        'timestamp': datetime.now().isoformat(),
                        'level': level.upper()
                    })

        return logs


log_parser = LogParser()
