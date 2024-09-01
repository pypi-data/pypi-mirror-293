from idingbot.constant import interface
from idingbot.core.core import IDingBotCore


class IDingBot(IDingBotCore):
    def new_method(self):
        print("New method added")

    def send_text_msg(self, conversation_id: str, content: str):
        """
        发送文字消息
        :param conversation_id:
        :param content:
        :return:
        """
        super().__on()
        data = {
            "type": interface.MT_SEND_TEXT_MSG,
            "data": {
                "conversation_id": conversation_id,
                "content": content
            }
        }
        super().dll_request_api(data)

    def send_app_msg(self, conversation_id: str, app_info: dict = {}):
        """
        发送小程序消息
        :param conversation_id:
        :param app_info:
        :return:
        """
        data = {
            "type": 11162,
            "data": {
                "conversation_id": conversation_id,
                "username": 'gh_22f97aca5bd7@app',
                "appid": "wx09969e6ae629c8be",
                "appname": "好愿视",
                "appicon": 'http://wework.qpic.cn/bizmail/6VQcTClPQnpxGh8dribrMBic5xa7J50dNfiasOEoeU45Brqyxibuibef32w/0',
                "title": '愿你不忘初心，砥砺前行',
                "page_path": 'pages/loading/loading.html?strategyId=581173251561099264',
                # // cdn参数为小程序封面，可以从cdn上传图片处获得
                'file_id': '306c0201020465306302010002042b3c105002031e9038020451c4f46d020466c6d09d04353732353335363632345f323134333433393032345f6435356538376439653033363231333630643038323365656566343263333863020310380002030080e004000201010201000400',
                "aes_key": '6470616B6E6F76626B62626F656E6A65',
                "md5": "059b34e084cf19a38a92a677177863d2",
                "size": 32989
            }
        }
        super().dll_request_api(data)
