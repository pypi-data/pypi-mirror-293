import ctypes
import json
import os
import subprocess
import time
from functools import wraps

import psutil
import pyee

from idingbot.constant import interface

# # 定义方法参数类型
# clientAcceptCallFun = ctypes.WINFUNCTYPE(None, ctypes.c_int32)
# # 定义方法参数类型
# callRecvHandlerCallFun = ctypes.WINFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32)
# # 定义方法参数类型
# clientCloseCallFun = ctypes.WINFUNCTYPE(None, ctypes.c_int32)

add_client_accept_callfunc = ctypes.WINFUNCTYPE(None, ctypes.c_int32)
add_recv_handler_callfunc = ctypes.WINFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32)
add_client_close_callfunc = ctypes.WINFUNCTYPE(None, ctypes.c_int32)

dll_lib = os.path.dirname(os.path.abspath(__file__))

"""
path = ctypes.c_char_p(os.path.join(dll_lib.replace("core", ""), 'dll', 'WxWork.dll'))
TypeError: bytes or integer address expected instead of str instance
"""

CALLBACK_FUNC = ctypes.WINFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32)


class IDingBotCore:
    _instance = None

    @staticmethod
    def get_instance():
        if IDingBotCore._instance is None:
            IDingBotCore._instance = IDingBotCore()
        return IDingBotCore._instance

    def __init__(self):
        """
        初始化
        """
        self.transfer = ctypes.windll.LoadLibrary(self.path_transfer(os.path.join(dll_lib.replace("core", ""), 'dll', 'transfer.dll')))
        self.path = self.path_transfer(os.path.join(dll_lib.replace("core", ""), 'dll', 'WxWork.dll')).encode()

        self.event_emitter = pyee.EventEmitter()


    def _on(self, msg_type, f):
        """
        消息事件绑定
        :param msg_type:
        :param f:
        :return:
        """
        self.event_emitter.on(msg_type, f)

    def msg_register(self, msg_type: str):
        """
        消息事件注册装饰器
        :param msg_type:
        :return:
        """

        def wrapper(f):
            wraps(f)
            self._on(msg_type, f)
            return f

        return wrapper

    def kill_wework(self):
        """
        关闭企业微信应用
        :return:
        """
        subprocess.run("taskkill /IM WXWork.exe /F", capture_output=True, text=True)

    def get_processes(self, process_name: str):
        """
        读取运行进程
        :param process_name:
        :return:
        """
        processes = []
        for process in psutil.process_iter():
            if process.name().lower() == process_name.lower():
                processes.append(process)
        return processes

    def client_accept_callfunc(self, clientId):
        """
        客户端连接成功事件监听回调
        :param clientId:
        :return:
        """
        print("客户端连接成功")

    def recv_handler_callfunc(self, cid, add_msg, length):
        """
        消息事件监听回调
        :param add_msg:
        :return:
        """
        msg = json.loads(add_msg.decode('utf-8'))
        msg_type = msg['type']
        self.event_emitter.emit(msg_type, msg['data'])
        self.event_emitter.emit(interface.MT_ALL_MSG, msg['data'])

    def client_close_callfunc(self, clientId):
        """
        客户端断开连接事件监听回调
        :param clientId:
        :return:
        """
        print("客户端断开连接")

    def path_transfer(self, abs_path, base_dir=None):
        """
        绝对路径转换相对路径（解决 WxWork.dll 路径问题）
        :param abs_path:
        :param base_dir:
        :return:
        """
        if base_dir is None:
            base_dir = os.getcwd()
        if not abs_path.endswith(os.sep):
            abs_path += os.sep
        if not base_dir.endswith(os.sep):
            base_dir += os.sep

        rel_path = os.path.relpath(abs_path, base_dir)
        if rel_path.endswith(os.sep) and not abs_path.endswith(os.sep * 2):
            rel_path = rel_path[:-1]
        return os.path.join(".", rel_path)

    def dll_request_api(self, data: dict):
        """
        发送消息接口
        :param msg_data:
        :return:
        """
        from_json = json.dumps(data)
        self.transfer.SendWxWorkData(1, ctypes.c_char_p(from_json.encode()))

    def start(self, WxWork_dll=None):
        """
        启动微信机器人服务
        :return:
        """
        processes = self.get_processes("WXWork.exe")
        if processes:
            self.kill_wework()

        if WxWork_dll is not None:
            self.transfer.InjectWxWork(WxWork_dll.encode(), "")
        else:
            self.transfer.InjectWxWork(self.path, "")

        while not processes:
            time.sleep(5)
            processes = self.get_processes("WXWork.exe")
        self.transfer.UseRecvJsUnicode()

        p_client_accept_callfunc = add_client_accept_callfunc(self.client_accept_callfunc)
        p_call_recv_handler_callfunc = add_recv_handler_callfunc(self.recv_handler_callfunc)
        p_client_close_callfunc = add_client_close_callfunc(self.client_close_callfunc)

        self.transfer.InitWxWorkSocket(
            p_client_accept_callfunc,
            p_call_recv_handler_callfunc,
            p_client_close_callfunc
        )

        while True:
            pass