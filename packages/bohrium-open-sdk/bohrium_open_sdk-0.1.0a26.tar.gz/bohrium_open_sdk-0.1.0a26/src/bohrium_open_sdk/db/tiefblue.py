from bohrium_open_sdk.opensdk._tiefblue_client import Tiefblue as _Tiefblue
from bohrium_open_sdk.opensdk._base_client import BaseClient
from httpx import URL
from typing import Optional, Union
from bohrium_open_sdk import UploadInputItem


class Tiefblue(BaseClient):

    def __init__(
        self,
        tiefblue_url: Optional[Union[str, URL]] = None,
    ) -> None:
        self.tiefblue = _Tiefblue(base_url=tiefblue_url)

    def upload_file(
        self, token_params: dict = {}, file_path: str = "", overwrite: bool = False
    ):
        # path
        params = self.tiefblue.decode_base64(
            token_params[self.tiefblue.TIEFBLUE_HEADER_KEY]
        )
        path = params["path"]
        orgin_file_name = path.split("/")[-1]

        headers = {
            self.tiefblue.TIEFBLUE_HEADER_KEY: token_params[
                self.tiefblue.TIEFBLUE_HEADER_KEY
            ],
            self.tiefblue.AUTH_HEADER_KEY: token_params[self.tiefblue.AUTH_HEADER_KEY],
        }
        meta_resp = self.tiefblue.meta(path=path, headers=headers)

        if meta_resp.get("code") != 0:
            raise Exception(f"upload failed pre to get meta failed: {meta_resp}")

        if meta_resp.get("data").get("exist") and not overwrite:
            raise Exception(f"file {orgin_file_name} already exists")

        # 上传文件
        file = UploadInputItem(src=file_path)
        self.tiefblue.upload_from_file_multi_part(
            object_key=path,
            custom_headers=headers,
            file_path=str(file.src),
            progress_bar=True,
        )
