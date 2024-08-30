# -*- coding: UTF-8 -*-

from bohrium_open_sdk import OpenSDK
from bohrium_open_sdk.db.tiefblue import Tiefblue
import os


class App:
    def __init__(self, base_url="https://openapi.test.dp.tech", access_key="", tiefblue_url=None, timeout=60):
        # timeout 默认 1min
        self.client = OpenSDK(base_url=base_url, access_key=access_key)
        self.tiefblue = Tiefblue(tiefblue_url=tiefblue_url)

    def get_user_info(self):
        resp = self.client.user.get_info()
        data = resp.get("data")
        return data.get("user_id"), data.get("org_id")

    def get_app_id(self, app_key):
        resp = self.client.app.get_app_info(app_key)
        return resp.get("data").get("id")

    def create(self, data):
        return self.client.app_db.create(data)

    def delete(self, data):
        return self.client.app_db.delete(data)

    def count(self, data):
        return self.client.app_db.count(data)

    def update(self, data):
        return self.client.app_db.update(data)

    def query(self, data):
        return self.client.app_db.query(data)

    def create_table(self, data):
        return self.client.app_db.create_table(data)

    def delete_table(self, data):
        return self.client.app_db.delete_table(data)

    def get_upload_token(self, app_key: str = "", file_name: str = ""):
        return self.client.app_db.get_upload_token(app_key, file_name)

    def upload_file(
            self,
            app_key: str = "",
            file_name: str = "",
            file_path: str = "",
            overwrite: bool = False,
    ):
        """
        app_key: str, required 当前 App 的 app_key
        file_name: str, required 存储的文件名
        file_path: str, required 要上传文件的本地路径
        overwrite: bool, optional 是否覆盖同名文件，默认为 False

        请捕获异常并处理
        """
        if not app_key:
            raise Exception("app_key is required")
        if not file_name:
            raise Exception("file_name is required")
        if not file_path:
            raise Exception("file_path is required")
        # file_path是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file_path {file_path} not exists")
        if os.path.isdir(file_path):
            raise IsADirectoryError(f"file_path {file_path} is a directory")

        token = self.get_upload_token(app_key, file_name)

        if token.get("code") != 0:
            raise Exception(f"get upload token failed: {token}")

        self.tiefblue.upload_file(token.get("data"), file_path, overwrite)
