# -*- coding: utf-8 -*-
import logging
import requests
import threading

from .StatLogger import StatTimer
from .afts import Afts
from itertools import repeat
from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger()

client_download_thread_pool = ThreadPool()
client_upload_thread_pool = ThreadPool()
client_get_url_thread_pool = ThreadPool()

download_thread_pool_lock = threading.Lock()
upload_thread_pool_lock = threading.Lock()
get_url_thread_pool_lock = threading.Lock()


class AftsClient:
    def __init__(self, biz_key, biz_secret, appid, endpoint_config=None, dtimer:StatTimer=None, utimer:StatTimer=None):
        self._afts = Afts(biz_key, biz_secret, appid, {} if endpoint_config is None else endpoint_config)
        self._traceid = ""
        self._dtimer = StatTimer(False, True) if dtimer is None else dtimer
        self._utimer = StatTimer(False, True) if utimer is None else utimer
    
    def set_traceid(self, traceid):
        self._traceid = traceid

    def __download_file_with_retry(self, file_id, timeout_sec, retry=3):
        '''
        内部方法
        '''
        for i in range(retry):
            content = self._afts.download_file(file_id, timeout_sec)
            if content is not None:
                logger.info(f"traceid={self._traceid} download file succeed: {file_id}: file len {len(content)}")
                return content, None
            logger.warning(f"traceid={self._traceid} download file failed: {file_id}: {self._afts.err_msg()}, retry {i}")
        return None, self._afts.err_msg()

    def __upload_file_with_retry(self, file_data, file_name, setpublic=False, timeout_sec=3, biz_key="", retry=3):
        '''
        内部方法
        '''
        for i in range(retry):
            file_id = self._afts.upload_file(file_data, file_name, setpublic = setpublic, timeout_sec = timeout_sec, biz_key=biz_key)
            if file_id is not None:
                logger.info(f"traceid={self._traceid} upload file succeed: file id {file_id}, biz_key is {biz_key}")
                return file_id, None
            logger.warning(f"traceid={self._traceid} upload file failed: {self._afts.err_msg()}, retry {i}")
        return None, self._afts.err_msg()

    def __get_url_with_retry(self, file_id, timeout_sec, retry=3):
        '''
        内部方法
        '''
        for i in range(retry):
            url = self._afts.get_url(file_id, timeout_sec)
            if url is not None:
                logger.info(f"traceid={self._traceid} get url succeed: {file_id}: url: {url}")
                return url, None
            logger.warning(f"traceid={self._traceid} get url failed: {file_id}: {self._afts.err_msg()}, retry {i}")
        return None, self._afts.err_msg()
    
    def err_msg(self):
        return self._afts.err_msg()

    def download_file(self, file_id, timeout_sec = 3):
        '''
        单线程下载单个文件
        成功：返回文件内容
        失败：返回None, 错误信息通过调用err_msg方法获取
        '''
        with self._dtimer:
            return self.__download_file_with_retry(file_id, timeout_sec)[0]
    
    def upload_file(self, file_data, file_name, setpublic=False, timeout_sec = 3, biz_key=""):
        '''
        单线程上传单个文件
        成功：返回file ID
        失败：返回None, 错误信息通过调用err_msg方法获取
        '''
        with self._utimer:
            return self.__upload_file_with_retry(file_data, file_name, setpublic=setpublic, timeout_sec=timeout_sec, biz_key=biz_key)[0]
    
    def get_url(self, file_id, timeout_sec = 3):
        '''
        单线程获取单个file ID对应的URL
        成功：返回URL
        失败：返回None, 错误信息通过调用err_msg方法获取
        '''
        return self.__get_url_with_retry(file_id, timeout_sec)[0]

    def download_file_threaded(self, file_id_list, timeout_sec = 3):
        '''
        多线程下载多个文件
        返回结果是一个列表，每个列表元素是一个tuple(content, err_msg)。content是下载的文件内容，下载失败时为None，err_msg表示失败原因。
        '''
        with self._dtimer:
            try:
                download_thread_pool_lock.acquire()
                return client_download_thread_pool.starmap(self.__download_file_with_retry, zip(file_id_list, repeat(timeout_sec)))
            finally:
                download_thread_pool_lock.release()

    def upload_file_threaded(self, file_data_list, file_name_list, setpublic=False, timeout_sec = 3, biz_key=""):
        '''
        多线程上传多个文件
        返回结果是一个列表，每个列表元素是一个tuple(file_id, err_msg)。file_id表示上传成功时的file ID，失败时为None，err_msg表示失败原因。
        '''
        with self._utimer:
            try:
                upload_thread_pool_lock.acquire()
                return client_upload_thread_pool.starmap(self.__upload_file_with_retry, zip(file_data_list, file_name_list, repeat(setpublic), repeat(timeout_sec), repeat(biz_key)))
            finally:
                upload_thread_pool_lock.release()

    def get_url_threaded(self, file_id_list, timeout_sec = 3):
        '''
        多线程获取多个file ID的对应URL
        返回结果是一个列表，每个列表元素是一个tuple(url, err_msg)。url是生成的url，失败时为None，err_msg表示失败原因。
        '''
        try:
            get_url_thread_pool_lock.acquire()
            return client_get_url_thread_pool.starmap(self.__get_url_with_retry, zip(file_id_list), repeat(timeout_sec))
        finally:
            get_url_thread_pool_lock.release()

    def __download_from_url_with_retry(self, url, timeout_sec, retry=3):
        '''
        内部方法
        '''
        try:
            status_code = 0
            for i in range(retry):
                resp = requests.get(url, allow_redirects = True, timeout=timeout_sec)
                status_code = resp.status_code
                if status_code != requests.codes.ok:
                    logger.warning(f"traceid={self._traceid}: download from url failed: code={status_code}: url={url}, retry {i}")
                    continue
                else:
                    logger.info(f"traceid={self._traceid}: download from url succeed: {url=}, content len {len(resp.content)}")
                    return resp.content, None
            return None, "failed with http code " + str(status_code)
        except Exception as e:
            logger.error(f"traceid={self._traceid}: download from url exception: " + repr(e))
            return None, "exception " + repr(e)

    def download_from_url(self, url, timeout_sec = 3):
        '''
        单线程从url获取内容
        成功：返回一个tuple，第一个元素为内容，第二个元素为None
        失败：返回一个tuple，第一个元素为None，第二个元素为错误信息
        '''
        with self._dtimer:
            return self.__download_from_url_with_retry(url, timeout_sec)

    def download_from_url_threaded(self, url_list, timeout_sec=3):
        '''
        多线程从多个url获取内容
        返回结果是一个列表，每个列表元素是一个tuple(content, err_msg)。content是下载的文件内容，下载失败时为None，err_msg表示失败原因。
        '''
        with self._dtimer:
            try:
                download_thread_pool_lock.acquire()
                return client_download_thread_pool.starmap(self.__download_from_url_with_retry, zip(url_list, repeat(timeout_sec)))
            finally:
                download_thread_pool_lock.release()
