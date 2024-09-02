import platform
import os
import logging
import logging.handlers
from typing import Sequence, Optional
from .filter import MultiLevelFilter, LevelFilter
from .time_executio import TimeExecutionLogger
from .formatter import  ConsoleFormatter, FileFormatter
from .internal_logger import InternalLogger
from .logger_typing import LogLevel, ColorName
from .errors import LoggerErrors

# Дополнительная проверка для ОС Windows
if platform.system() == "Windows":
    os.system('color')

class LoggerManager:
    LEVEL_MAPPING = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, *, name: str, default_format: str = None, level: LogLevel = "DEBUG", log_to_file: bool = False, file_name: str = 'app.log',
                 log_dir: str = 'logs', max_bytes: int = 1024 * 1024, backup_count: int = 5):
        if not isinstance(name, str) or not name.strip():
            self.internal_logger = InternalLogger(name=f"DefaultLogger_internal")
            self.internal_logger.log_warning(f"Некорректное имя логгера: '{name}'. Устанавливается имя по умолчанию 'DefaultLogger'.")
            name = "DefaultLogger"
        else:
            # Внутренний логгер
            self.internal_logger = InternalLogger(name=f"{name}_internal")

        self.max_bytes: int = max_bytes
        self.backup_count: int = backup_count

        # Основной логгер
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.console_handler: Optional[logging.StreamHandler] = None
        self.file_handler: Optional[logging.FileHandler] = None
        self.log_filter: Optional[logging.Filter] = None

        # Экземпляры форматтеров
        self.console_formatter = ConsoleFormatter(default_format)
        self.file_formatter = FileFormatter(default_format)

        self.setup_console_handler(level)
        if log_to_file:
            self.enable_file_logging(file_name, log_dir)

    def setup_console_handler(self, level: LogLevel):
        """Настройка консольного обработчика и форматтера"""
        log_level = self.LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(log_level)
            self.console_handler.setFormatter(self.console_formatter)
            self.logger.addHandler(self.console_handler)
        else:
            self.internal_logger.log_error(
                f"Некорректный уровень логирования: {level}. Используйте один из: {list(self.LEVEL_MAPPING.keys())}"
            )

    def enable_console_logging(self):
        """Включение логирования в консоль"""
        if self.console_handler:
            self.console_handler.setLevel(self.logger.level)
            self.internal_logger.log_info("Логирование в консоль включено")

    def disable_console_logging(self):
        """Отключение логирования в консоль"""
        if self.console_handler:
            self.console_handler.setLevel(logging.CRITICAL + 1)
            self.internal_logger.log_info("Логирование в консоль отключено")
        else:
            self.internal_logger.log_warning("Обработчик консольного логирования уже отключен или не был инициализирован")

    def enable_logging(self):
        """Включение логирования"""
        self.logger.disabled = False
        self.internal_logger.log_info("Логирование включено")

    def disable_logging(self):
        """Отключение логирования"""
        self.logger.disabled = True
        self.internal_logger.log_info("Логирование отключено")

    def enable_file_logging(self, file_name: str = 'app.log', log_dir: str = 'logs'):
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        except Exception as e:
            self.internal_logger.log_error(f"Ошибка при создании директории для логов: {e}")
            raise LoggerErrors(f"Ошибка при создании директории для логов: {e}")

        log_path = os.path.join(log_dir, file_name)

        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()

        try:
            self.file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count
            )
            self.file_handler.setLevel(self.logger.level)
            self.file_handler.setFormatter(self.file_formatter)
            self.logger.addHandler(self.file_handler)
            self.internal_logger.log_info(f"Логирование в файл '{log_path}' включено")
        except Exception as e:
            self.internal_logger.log_error(f"Ошибка при настройке файлового логгера с ротацией: {e}")
            raise LoggerErrors(f"Ошибка при настройке файлового логгера с ротацией: {e}")

    def disable_file_logging(self):
        """Отключение логирования в файл"""
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()
            self.file_handler = None
            self.internal_logger.log_info("Логирование в файл отключено")
        else:
            self.internal_logger.log_warning(
                "Обработчик файла логирования уже отключен или не был инициализирован"
            )

    def set_file_handler_params(self, max_bytes: int, backup_count: int):
        """Установка параметров для RotatingFileHandler."""
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        if self.file_handler:
            self.file_handler.maxBytes = max_bytes
            self.file_handler.backupCount = backup_count
            self.internal_logger.log_info(
                f"Изменены параметры RotatingFileHandler: maxBytes={max_bytes}, backupCount={backup_count}"
            )
        else:
            self.internal_logger.log_warning(
                "Файловый обработчик не инициализирован. Новые параметры будут применены при следующем включении логирования в файл."
            )

    def set_name(self, name: str):
        """Установка нового имени логгера"""
        if not isinstance(name, str) or not name.strip():
            self.internal_logger.log_error(f"Некорректное новое имя логгера: '{name}'. Имя остается без изменений.")
            return

        self.logger.name = name
        self.internal_logger.name = f"{name}_internal"
        self.internal_logger.log_info(f"Имя логгера изменено на '{name}'")

    def set_level(self, level: LogLevel):
        """Установка уровня логирования"""
        log_level = self.LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.logger.setLevel(log_level)
            if self.console_handler:
                self.console_handler.setLevel(log_level)
            if self.file_handler:
                self.file_handler.setLevel(log_level)
            self.internal_logger.log_info(f"Уровень логирования установлен на {level}")
        else:
            self.internal_logger.log_error(
                f"Некорректный уровень логирования: {level}. Используйте один из: {list(self.LEVEL_MAPPING.keys())}"
            )

    def set_filter(self, level: LogLevel):
        """Установка фильтра для логирования"""
        log_level = self.LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.clear_filter()
            self.log_filter = LevelFilter(log_level)
            self.logger.addFilter(self.log_filter)
            self.internal_logger.log_info(f"Фильтр уровня логирования установлен на {level}")
        else:
            self.internal_logger.log_error(
                f"Некорректный уровень фильтра: {level}. Используйте один из: {list(self.LEVEL_MAPPING.keys())}"
            )

    def set_filter_list(self, levels: Sequence[LogLevel]):
        """Установка списка фильтров для логирования"""
        if not levels:
            self.internal_logger.log_error("Список уровней фильтра не должен быть пустым.")
            return

        valid_levels = [self.LEVEL_MAPPING[level] for level in levels if level in self.LEVEL_MAPPING]

        if not valid_levels:
            self.internal_logger.log_error(
                f"Некорректные уровни фильтра: {levels}. Используйте один из: {list(self.LEVEL_MAPPING.keys())}"
            )
            return

        self.clear_filter()
        self.log_filter = MultiLevelFilter(valid_levels)
        self.logger.addFilter(self.log_filter)
        self.internal_logger.log_info(f"Фильтр уровней логирования установлен на {levels}")

    def reset_level(self):
        """Сброс уровня логирования до уровня DEBUG"""
        self.set_level('DEBUG')

    def clear_filter(self):
        """Очистка установленного фильтра"""
        if self.log_filter:
            self.logger.removeFilter(self.log_filter)
            self.log_filter = None
            self.internal_logger.log_info("Фильтр логирования очищен")

    def time_execution(self):
        """Контекстный менеджер для логирования времени выполнения блока кода"""
        return TimeExecutionLogger(self.internal_logger.logger)

    # Методы для работы с форматтерами
    def set_console_format(self, format_string: str):
        """Устанавливает формат для консольного логирования."""
        self.console_formatter.set_format(format_string)
        self.internal_logger.log_info(
            f"Установлен формат для консольного логирования: {format_string}"
        )

    def set_file_format(self, format_string: str):
        """Устанавливает формат для файлового логирования."""
        self.file_formatter.set_format(format_string)
        self.internal_logger.log_info(
            f"Установлен формат для файлового логирования: {format_string }"
        )

    def set_console_level_format(self, level: LogLevel, format_string: str):
        """Устанавливает формат для консольного логирования."""
        self.console_formatter.set_level_format(level, format_string)
        self.internal_logger.log_info(
            f"Установлен формат для консольного логирования: {level+' '+format_string}"
        )

    def set_file_level_format(self, level: LogLevel, format_string: str):
        """Устанавливает формат для файлового логирования."""
        self.file_formatter.set_level_format(level, format_string)
        self.internal_logger.log_info(
            f"Установлен формат для файлового логирования: {level + ' - ' + format_string}"
        )

    def set_console_color(self, level: LogLevel, color: ColorName):
        """Устанавливает цвет для консольного логирования."""
        self.console_formatter.set_color(level, color)
        self.internal_logger.log_info(
            f"Установлен цвет - {color}; для консольного логирования - {level}"
        )

    # Управление внутренним логгером
    def enable_internal_logging(self):
        self.internal_logger.enable_logging()

    def disable_internal_logging(self):
        self.internal_logger.disable_logging()