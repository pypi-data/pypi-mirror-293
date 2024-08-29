# -*- encoding: utf-8 -*-

import os
import time
import logging
import logging.handlers
from enum import Enum
from logging.handlers import RotatingFileHandler

from .TraceLogger import TraceLog
from .common import LOG_DIR


# from concurrent_log_handler import ConcurrentRotatingFileHandler


class TimerUnit(Enum):
    NS = 1
    US = 1000
    MS = 1000000
    S = 10000000000


class StatTimer:
    def __init__(self, start=False, accumulate=False, unit: TimerUnit = TimerUnit.MS):
        if start:
            self.__start_time = time.time_ns()
        else:
            self.__start_time = -1
        self.__accumulate = accumulate
        self.__counter = 0
        self.__unit = unit

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, trace):
        self.stop()

    def start(self):
        if not self.__accumulate and self.__start_time > 0:
            self.reset()
        self.__start_time = time.time_ns()

    def stop(self):
        if self.__start_time > 0:
            self.__counter += (time.time_ns() - self.__start_time) // self.__unit.value
        return self.__counter

    def reset(self):
        self.__start_time = -1
        self.__counter = 0

    def value(self):
        if self.__start_time < 0:
            return 0
        if self.__counter > 0:
            return self.__counter
        return (time.time_ns() - self.__start_time) // self.__unit.value


class StatField:
    def __init__(self, name: str, value='-'):
        self.name = name
        self.__value = value

    def set(self, value):
        self.__value = value

    def value(self):
        return self.__value if self.__value is not None else ''


class TimerField(StatField):
    timer: StatTimer = None

    def __init__(self, name: str, start=False, accumulate=False, unit: TimerUnit = TimerUnit.MS):
        super().__init__(name)
        self.timer = StatTimer(start, accumulate, unit)

    def __enter__(self):
        self.timer.start()

    def __exit__(self, type, value, trace):
        self.timer.stop()

    def value(self):
        return self.timer.value()


class StatLogger:

    def __init__(self, stat_id, schema):
        '''
        logger_name: str, 目前只能填"csp_framework"或"csp_service"
        pattern: tuple of str, 埋点项列表
        '''
        if not isinstance(stat_id, str):
            raise TypeError("stat_id must be type of str")
        if not isinstance(schema, tuple):
            raise TypeError("schema must be type of tuple")
        if len(schema) == 0:
            raise ValueError("schema must have one field at least")

        self.cluster_name = os.getenv("PUBLISH_DOMAIN", '-')
        self.service_name = "-"
        self.service_version = "-"

        # from maya_tools.context import get_request_context
        # request_context = get_request_context()
        # if request_context is not None:
        #     # 需要在处理请求时才能获得真正的服务和版本名，初始化时使用mock的
        #     self.service_name = request_context.scene_name
        #     self.service_version = request_context.chain_name

        self.stat_id = stat_id
        self.schema = schema
        self.fields = {}
        for field in schema:
            # setattr(self, field.name, field)
            self.fields[field.name] = field

        # work_dir = os.path.dirname(os.path.abspath(__file__))
        # work_dir = os.getcwd()
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = f"{LOG_DIR}/{self.stat_id}.log"
        TraceLog.info(f'set stat-log file: {log_file}')

        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(process)d %(thread)d %(message)s')
        formatter = logging.Formatter('%(asctime)s %(process)d %(thread)d %(message)s')
        # handler = ConcurrentRotatingFileHandler(log_file, 'a', 64 * 1024 * 1024, 8, 'utf-8')
        handler = RotatingFileHandler(log_file, 'a', 64 * 1024 * 1024, 8, 'utf-8')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger(self.stat_id)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        # self.logger.propagate = False

    def __getattr__(self, field: str):
        return self.fields[field]

    def print(self):
        message = self.cluster_name + "," + self.service_name + "/" + self.service_version + ","
        for field in self.schema:
            message += f"{field.name}={field.value()}^"
        self.logger.info(message)
        TraceLog.info(f'StatLog[{self.stat_id}]: {message}')
