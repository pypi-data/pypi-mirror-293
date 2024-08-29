#!/usr/bin/env python
# coding: utf-8

import logging
import threading


class TraceLog:
    logger = logging.getLogger()
    local = threading.local()
    local.traceid = '?'

    def __new__(cls, *args, **kwargs):
        raise TypeError("TraceLogger can not be instantiated")

    @classmethod
    def initContext(cls, traceid: str):
        class _Context:
            def __enter__(self):
                self.begin()
                return self

            def __exit__(self, type, value, trace):
                self.end()
                return False

            @staticmethod
            def begin():
                if traceid is not None and traceid != '':
                    cls.local.traceid = traceid
                TraceLog.info(f"======TraceLog.BEGIN======")

            @staticmethod
            def end():
                TraceLog.info(f"======TraceLog.END======")
                cls.local.traceid = '?'

        return _Context()

    @classmethod
    def traceId(cls):
        return cls.local.traceid

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        #cls.logger.info(msg, *args, **kwargs)
        print(msg, *args, **kwargs)

    @classmethod
    def warn(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.warning(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.critical(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, exc_info=True, **kwargs):
        msg = f"<{cls.local.traceid}> {msg}"
        cls.logger.exception(msg, *args, exc_info=exc_info, **kwargs)
