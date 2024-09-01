#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : listener
# Author        : Sun YiFan-Movoid
# Time          : 2024/8/3 15:09
# Description   : 
"""
import threading
import time
from typing import Dict

import websocket


class OneListener:
    def __init__(self, url: str):
        self._url = url
        self._ws = websocket.WebSocket()
        self._thread = threading.Thread()
        self._history = []
        self._stop = False
        self._sign = {}
        self.start()

    def _thread_listen(self):
        if not self._ws.connected:
            self._ws.connect(self._url)
        while self._ws.connected and not self._stop:
            try:
                receive_text = self._ws.recv()
                time_now = time.time()
                self._history.append([time_now, receive_text])
            except Exception:
                if self._ws.connected:
                    self._ws.close()
                self._ws.connect(self._url)

    def sign(self, sign_name="__default__"):
        sign_name = str(sign_name)
        self._sign[sign_name] = time.time()
        self.start()

    def start(self):
        if not self._thread.is_alive():
            self._thread = threading.Thread(target=self._thread_listen)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        self._stop = False

    def _find_history_text_after_sign(self, sign=None):
        """
        获取从sign之后的所有获得信息
        :param sign: 不填就全部返回
        :return:
        """
        if sign is None or sign not in self._sign:
            re_list = [_ for _ in self._history]
        else:
            re_list = [_ for _ in self._history if _[0] >= self._sign[sign]]
        return re_list

    def wait_until_check_pass(self, check_function, sign=None, refresh_sign=False, return_time=False, check_interval=0.1, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param return_time: 返回时是否返回时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: 时间+文本，如果没有就返回None。
        """
        if callable(check_function):
            real_check_function = check_function
        else:
            def real_check_function(check_text: object) -> bool:
                return str(check_text) == str(check_function)
        if sign is not None and refresh_sign:
            self.sign(sign)
        text_list = self._find_history_text_after_sign(sign)
        for text_one in text_list[::-1]:
            if real_check_function(text_one[1]):
                pass_text = text_one
                break
        else:
            start_time = time.time()
            last_time = 0
            text_check = len(text_list)
            while last_time < timeout:
                loop_start_time = time.time()
                now_text_list = self._find_history_text_after_sign(sign)
                while text_check < len(now_text_list):
                    text_one = now_text_list[text_check]
                    if real_check_function(text_one[1]):
                        pass_text = text_one
                        break
                    text_check += 1
                else:
                    loop_last_time = time.time() - loop_start_time
                    time.sleep(max(check_interval - loop_last_time, 0))
                    last_time = time.time() - start_time
                    continue
                break
            else:
                pass_text = [0, None]
        if return_time:
            return pass_text
        else:
            return pass_text[1]

    def wait_until_check_multi_pass(self, check_function, pass_count=1, sign=None, refresh_sign=False, return_time=False, check_interval=0.1, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param pass_count: 检查通过的数量，默认1个，如果输入其他数值，那么就会检查更多通过的情况，最小为1
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param return_time: 返回时是否返回时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: 查询到的[[时间,文本]]，即使不够数量，也会把已有的返回，如果没有就返回空列表
        """
        if callable(check_function):
            real_check_function = check_function
        else:
            def real_check_function(check_text: object) -> bool:
                return str(check_text) == str(check_function)
        pass_count = max(1, int(pass_count))
        if sign is not None and refresh_sign:
            self.sign(sign)
        re_pass_text_list = []
        text_list = self._find_history_text_after_sign(sign)
        for text_one in text_list[::-1]:
            if real_check_function(text_one[1]):
                re_pass_text_list.insert(0, text_one if return_time else text_one[1])
                if len(re_pass_text_list) >= pass_count:
                    break
        else:
            start_time = time.time()
            last_time = 0
            text_check = len(text_list)
            while last_time < timeout:
                loop_start_time = time.time()
                now_text_list = self._find_history_text_after_sign(sign)
                while text_check < len(now_text_list):
                    text_one = now_text_list[text_check]
                    if real_check_function(text_one[1]):
                        re_pass_text_list.append(text_one if return_time else text_one[1])
                        if len(re_pass_text_list) >= pass_count:
                            break
                    text_check += 1
                else:
                    loop_last_time = time.time() - loop_start_time
                    time.sleep(max(check_interval - loop_last_time, 0))
                    last_time = time.time() - start_time
                    continue
                break
        return re_pass_text_list

    def wait_until_no_pass_text_new(self, check_function, sign=None, refresh_sign=False, no_new_time=3, check_interval=0.1, timeout=15):
        """
        检查是否能保持一段时间没有找到新可以满足要求的信息传入
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param no_new_time: 没有新信息的维持时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: bool,List[List[float,str]]，是否通过，接收到的全部的信息
        """
        if callable(check_function):
            real_check_function = check_function
        else:
            def real_check_function(check_text: object) -> bool:
                return str(check_text) == str(check_function)
        if sign is not None and refresh_sign:
            self.sign(sign)
        re_pass_text_list = []
        pass_time = 0
        text_list = self._find_history_text_after_sign(sign)
        for text_one in text_list[::-1]:
            if real_check_function(text_one[1]):
                re_pass_text_list.insert(0, text_one)
                pass_time = text_one[0]
                break
        else:
            if sign is None:
                pass_time = time.time()
            else:
                pass_time = self._sign[sign]
        start_time = time.time()
        last_time = 0
        no_new_last_time = start_time - pass_time
        if no_new_last_time >= no_new_time:
            return True, re_pass_text_list
        else:
            text_check = len(text_list)
            while last_time < timeout:
                loop_start_time = time.time()
                now_text_list = self._find_history_text_after_sign(sign)
                while text_check < len(now_text_list):
                    text_one = now_text_list[text_check]
                    if real_check_function(text_one[1]):
                        re_pass_text_list.append(text_one)
                        pass_time = text_one[0]
                    text_check += 1
                no_new_last_time = time.time() - pass_time
                if no_new_last_time >= no_new_time:
                    return True, re_pass_text_list
                else:
                    loop_last_time = time.time() - loop_start_time
                    time.sleep(max(check_interval - loop_last_time, 0))
                    last_time = time.time() - start_time
                    continue
            else:
                return False, re_pass_text_list


class WebSocketListener:
    def __init__(self):
        self._ws: Dict[str, OneListener] = {}

    @property
    def ws(self):
        return self._ws

    def start(self, url, name=None):
        name = str(url) if name is None else str(name)
        self._ws[name] = OneListener(url)

    def sign(self, name, sign):
        self._ws[name].sign(sign)

    def wait_until_check_pass(self, name, check_function, sign=None, refresh_sign=False, return_time=False, check_interval=0.1, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param name: 标签名，一定要输入
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param return_time: 返回时是否返回时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: 时间+文本，如果没有就返回None
        """
        return self._ws[name].wait_until_check_pass(check_function=check_function, sign=sign, refresh_sign=refresh_sign, return_time=return_time, check_interval=check_interval, timeout=timeout)

    def stop(self, name):
        self._ws[name].stop()

    def delete(self, name):
        if name in self._ws:
            self.stop(name)
            self._ws.pop(name)

    def wait_until_check_multi_pass(self, name, check_function, pass_count=1, sign=None, refresh_sign=False, return_time=False, check_interval=0.1, timeout=5):
        """
        最多等待一定时间后，检查是否存在某段文本满足要求，总是会寻找最新的文本
        :param name: 标签名，一定要输入
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param pass_count: 检查通过的数量，默认1个，如果输入其他数值，那么就会检查更多通过的情况，最小为1
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param return_time: 返回时是否返回时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: 查询到的[[时间,文本]]，即使不够数量，也会把已有的返回，如果没有就返回空列表
        """
        return self._ws[name].wait_until_check_multi_pass(check_function=check_function, pass_count=pass_count, sign=sign, refresh_sign=refresh_sign, return_time=return_time, check_interval=check_interval, timeout=timeout)

    def wait_until_no_pass_text_new(self, name, check_function, sign=None, refresh_sign=False, no_new_time=3, check_interval=0.1, timeout=15):
        """
        检查是否能保持一段时间没有新的满足要求的信息传入
        :param name: 标签名，一定要输入
        :param check_function: 检查函数，如果输入的变量没有__call__，那么就认定为全匹配文本
        :param sign: 标记，标记后的文本才会检查，输入None时会检查全文本
        :param refresh_sign: 是否立刻刷新一次sign，默认不刷新，可以保证排除sign过早标记产生的影响
        :param no_new_time: 没有新信息的维持时间
        :param check_interval: 每次检查的最小间隔
        :param timeout: 最大的等待时间
        :return: bool,List[List[float,str]]，是否通过，接收到的全部的信息
        """
        return self._ws[name].wait_until_no_pass_text_new(check_function=check_function, sign=sign, refresh_sign=refresh_sign, no_new_time=no_new_time, check_interval=check_interval, timeout=timeout)
