# -*- coding: utf-8 -*-

'''
Copyright (C) 2020 antfin.com. All rights reserved.

@file: afts.py
@author: 轩勇
@date: 20200603
'''
import time
import logging
import requests
import hashlib
import threading
import traceback
from urllib.parse import urlparse

###### uncomment the following lines to enable debug information to display on console ######
#import httplib
#import logging
#httplib.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True
#############################################################################################

logger = logging.getLogger()

class Afts:
    '''
    This class is used to upload and/or download file data to/from afts.
    The public api is "download_file" and "upload_file", these two function will not throw exception.
    '''

    # cached the mass token to improve performance
    TOKEN_EXPIRE_INTERVAL = 10 * 3600 # default to 10 hours
    __biz_key_dict = {} # format {"biz_key1":{"token":xxx,"last_update_timestamp":xxx},...}
    __biz_key_dict_lock = threading.Lock()

    def __init__(self, biz_key, biz_secret, appid, endpoint_config={}):

        self.__biz_key = biz_key
        # __biz_secret 区分环境，请填写对应的环境秘钥
        self.__biz_secret = biz_secret
        self.__appid = appid
        self.thread_local = threading.local()
        self.thread_local.err_msg = ""
        self.__err_msg = self.thread_local.err_msg

        # 上传/下载/令牌权限域名同样也区区分环境，哪个环境资源就填写哪个环境的配置，和__biz_secret一样
	    # 不同环境域名配置参考 https://yuque.antfin-inc.com/afts/document/tfklky
        # 上传域名
        self.__upload_endpoint_source = endpoint_config.get("upload_endpoint_source", "mass.alipay.com")
        # 下载域名 
        self.__download_endpoint_source = endpoint_config.get("download_endpoint_source", "mass.alipay.com")
        # 令牌权限域名
        self.__authority_endpoint = endpoint_config.get("authority_endpoint", "mmtcapi-pool.global.alipay.com")

        if self.__authority_endpoint.find('mmtcapi.alipay.com') != -1:
            self.__http_schema = 'https'
        else:
            # 线下或非公网是http
            self.__http_schema = 'http'

    def err_msg(self):
        '''
        This function return error message.
        '''
        return self.__err_msg

    '''
    获取op token
    '''
    def get_op_token(self, timeout_sec):

        time_stamp = str(int(time.time() * 1000))
        authority_url = self.__http_schema + "://" + self.__authority_endpoint + "/token/1.0/op"
        url_params = {}
        url_params["timestamp"] = time_stamp
        url_params["bizKey"] = self.__biz_key
        url_params["appId"] = self.__appid

        md5_handle = hashlib.md5()
        md5_handle.update((self.__appid + self.__biz_key + time_stamp + self.__biz_secret).encode('utf-8'))
        sign = md5_handle.hexdigest()
        url_params["sign"] = sign

        response = requests.get(authority_url, params=url_params, timeout = timeout_sec)
        if response.status_code != 200:
            self.__err_msg = "Error:get_op_token:http status code: " + str(response.status_code) + ", headers: " + str(response.headers)
            logger.error(f"{self.__err_msg}")
            return None
        else:
            res_json = response.json()
            if res_json["code"] != 0:
                self.__err_msg = "Error:get_op_token:server response code:" + str(res_json["code"])
                logger.error(f"{self.__err_msg}: {res_json}")
                return None
            else:
                return res_json["data"]["token"]

    '''
    获取 acktoken
    '''
    def get_acl_token(self, file_id, timeout_sec):
        authority_url = self.__http_schema + "://" + self.__authority_endpoint + "/token/1.0/acl"
        time_stamp = str(int(time.time() * 1000))
        url_params = {}
        url_params["timestamp"] = time_stamp
        url_params["bizKey"] = self.__biz_key
        url_params["fileId"] = file_id
        url_params["appId"] = self.__appid

        md5_handle = hashlib.md5()
        md5_handle.update((self.__appid + self.__biz_key + time_stamp + file_id + self.__biz_secret).encode('utf-8'))
        sign = md5_handle.hexdigest()
        url_params["sign"] = sign

        response = requests.get(authority_url, params=url_params, timeout = timeout_sec)
        if response.status_code != 200:
            self.__err_msg = "Error:get_acl_token:http status code: " + str(response.status_code) + ", headers: " + str(response.headers)
            logger.error(f"{self.__err_msg}")
            return None
        else:
            res_json = response.json()
            if res_json["code"] != 0:
                self.__err_msg = "Error:get_acl_token:server response code:" + str(res_json["code"])
                logger.error(f"{self.__err_msg}: {res_json}")
                return None
            else:
                return res_json["data"]
    
    '''
    判断缓存token是否过期
    '''
    def is_token_expire(self):
        if self.__biz_key not in Afts.__biz_key_dict:
            return True

        current_ts = time.time()
        elapsed_time  = abs(Afts.__biz_key_dict[self.__biz_key]["last_update_timestamp"] - current_ts)
        if elapsed_time >= Afts.TOKEN_EXPIRE_INTERVAL:
            return True
        return False

    '''
    获取 mass token
    '''
    def get_mass_token(self, timeout_sec):

        if self.__biz_key in Afts.__biz_key_dict and not self.is_token_expire():
            token = Afts.__biz_key_dict[self.__biz_key]["token"]
            logging.info(f"using cacehed mass token: {token}")
            return token

        authority_url = self.__http_schema + "://" + self.__authority_endpoint + "/token/1.0/mass"
        time_stamp = str(int(time.time() * 1000))
        url_params = {}
        url_params["appId"] = self.__appid
        url_params["bizKey"] = self.__biz_key
        url_params["opToken"] = self.get_op_token(timeout_sec)
        url_params["massType"] = '1'
        url_params["timestamp"] = time_stamp
        url_params["value"] = self.__biz_key
        url_params["expireTime"] = Afts.TOKEN_EXPIRE_INTERVAL + 1000 # 多留1000秒余量

        md5_handle = hashlib.md5()
        md5_handle.update((self.__appid + self.__biz_key +  url_params["value"]  + time_stamp).encode('utf-8'))
        sign = md5_handle.hexdigest()
        url_params["sign"] = sign

        response = requests.get(authority_url, params=url_params, timeout = timeout_sec)
        if response.status_code != 200:
            self.__err_msg = "Error:get_mass_token:http status code: " + str(response.status_code) + ", headers: " + str(response.headers)
            logger.error(f"{self.__err_msg}")
            return None
        else:
            res_json = response.json()
            if res_json["code"] != 0:
                self.__err_msg = "Error:get_mass_token:server response code:" + str(res_json["code"])
                logger.error(f"{self.__err_msg}: {res_json}")
                return None
            else:
                if self.__biz_key not in Afts.__biz_key_dict or self.is_token_expire():
                    Afts.__biz_key_dict_lock.acquire()
                    # test one more time
                    if self.__biz_key not in Afts.__biz_key_dict or self.is_token_expire():
                        Afts.__biz_key_dict[self.__biz_key] = {"token":res_json["data"], "last_update_timestamp": float(time_stamp) / 1000}
                        logging.info(f"updating cached mass token: {Afts.__biz_key_dict[self.__biz_key]}")
                    Afts.__biz_key_dict_lock.release()
                return res_json["data"]


    '''
    下载文件
    注意：file_id参入可以是afts fileid或url
    '''
    def __download_file(self, file_id, timeout_sec):
        if "http://" in file_id or "https://" in file_id:
            # 替换协议和域名
            parsedUrl = urlparse(file_id)
            parsedUrl = parsedUrl._replace(scheme='http')
            parsedUrl = parsedUrl._replace(netloc=self.__download_endpoint_source)
            logger.info(f"__download_file: replaced url: {parsedUrl.geturl()}")
            response = requests.get(parsedUrl.geturl(), allow_redirects=True, timeout = timeout_sec)
        else:
            acl_token = self.get_acl_token(file_id, timeout_sec)
            download_url = "https://" + self.__download_endpoint_source + "/afts/file/" + file_id 
            url_params = {}
            url_params["bizType"] = self.__biz_key
            url_params["token"] = acl_token
            response = requests.get(download_url, params=url_params, allow_redirects=True, timeout = timeout_sec)

        if response.status_code != 200:
            # print("download file failed." + "fileid=" + file_id + " url=" + download_url , "params=" , url_params)
            self.__err_msg = "Error:__download_file:http status code: " + str(response.status_code) + ", headers: " + str(response.headers)
            logger.error(f"{self.__err_msg}")
            return None
        else:
            # succeeded!
            # print("download file success." + "fileid=" + file_id + " url=" + download_url , "params=" , url_params)
            return response.content


    def __upload_file(self, file_data, file_name, setpublic, timeout_sec, biz_key):
        mass_token = self.get_mass_token(timeout_sec)

        upload_url = "https://" + self.__upload_endpoint_source + "/file/auth/upload"

        url_params = {}
        url_params["bz"] = self.__biz_key
        if biz_key is not None and biz_key != "":
            url_params["bz"] = biz_key
        url_params["public"] = str(setpublic).lower()
        url_params["mt"] = mass_token

        # compute file data md5
        #md5_handle = hashlib.md5()
        #md5_handle.update((file_data).encode('utf-8'))
        #file_data_md5 = md5_handle.hexdigest()
        #form_param = {"md5":file_data_md5}

        # file data to be uploaded, we use the md5 as the file name
        #form_file = {"file":(file_data_md5, file_data, "application/octet-stream")}
        form_file = {"file":(file_name, file_data, "application/octet-stream")}

        #response = requests.post(upload_url, params=url_params, data=form_param, files=form_file)
        response = requests.post(upload_url, params=url_params, files=form_file, timeout = timeout_sec)
        if response.status_code != 200:
            self.__err_msg = "Error:__upload_file:http status code: " + str(response.status_code) + ", headers: " + str(response.headers)
            logger.error(f"{self.__err_msg}")
            return None
        else:
            res_json = response.json()
            if res_json["code"] != 0:
                self.__err_msg = "Error:__upload_file:server response code:" + str(res_json["code"])
                logger.error(f"{self.__err_msg}: {res_json}")
                return None
            else:
                return res_json["data"]["id"]

    def download_file(self, file_id, timeout_sec = 3):
        '''
        Wrapper function that will not throw exception
        '''
        try:
            file_data = self.__download_file(file_id, timeout_sec)
            return file_data
        except Exception as e:
            logger.error(f"afts download file exception: {traceback.format_exc()}")
            self.__err_msg = "afts download file exception" + repr(e)
            return None

    def upload_file(self, file_data, setpublic=False, timeout_sec = 3, biz_key=""):
        '''
        Wrapper function that will not throw exception
        '''
        try:
            file_id = self.__upload_file(file_data, "", setpublic, timeout_sec, biz_key)
            return file_id
        except Exception as e:
            logger.error(f"afts upload file exception: {traceback.format_exc()}")
            self.__err_msg = "afts upload file exception: " + repr(e)
            return None

    '''
    上传文件
    param: file_data: 文件流
    file_name: 设置文件名，与下载的content-type 关联
    setpublic: 设置文件公私有
    '''
    def upload_file(self, file_data, file_name, setpublic=False, timeout_sec = 3, biz_key=""):
        '''
        Wrapper function that will not throw exception
        '''
        try:
            file_id = self.__upload_file(file_data, file_name, setpublic, timeout_sec, biz_key)
            return file_id
        except Exception as e:
            logger.error(f"afts upload file exception: {traceback.format_exc()}")
            self.__err_msg = "afts upload file exception: " + repr(e)
            return None

    '''
    获取url
    '''
    def get_url(self, file_id, timeout_sec = 3):
        try:
            acl_token = self.get_acl_token(file_id, timeout_sec)
            if acl_token is None:
                return None
            download_url = "https://" + self.__download_endpoint_source + "/afts/file/" + file_id + "?" + "bizType=" + self.__biz_key + "&token=" + acl_token
            return download_url
        except Exception as e:
            logger.error(f"afts get_url exception: {traceback.format_exc()}")
            self.__err_msg = "afts get_url exception: " + repr(e)
            return None

def afts_test():
    '''
    This function shows example usage and can be used for test purpose
    '''

    # dev end points for download, upload and authentication
    endpoint_config = {"download_endpoint_source":"mass.alipay.com",
                       "upload_endpoint_source":"mass.alipay.com",
                       "authority_endpoint":"mmtcapi.alipay.com"}

    afts = Afts("your_biz_key", "your_biz_secret", "your_appid", endpoint_config=endpoint_config)
    #with open("./_antvip_client.so", "rb") as f:
    #    file_data = f.read()
    file_data = "this is my test file data"

    # perform the upload
    for i in range(1):
        file_id = afts.upload_file(file_data)
        if file_id is None:
            print(afts.err_msg())
        else:
            print("upload ok, file_id: %s" % file_id)
            # perform the download
            file_data = afts.download_file(file_id)
            if file_data is None:
                print("download error: %s" % afts.err_msg())
            else:
                md5_handle = hashlib.md5()
                md5_handle.update(file_data)
                file_data_md5 = md5_handle.hexdigest()
                print("download ok, file md5: %s" % file_data_md5)
