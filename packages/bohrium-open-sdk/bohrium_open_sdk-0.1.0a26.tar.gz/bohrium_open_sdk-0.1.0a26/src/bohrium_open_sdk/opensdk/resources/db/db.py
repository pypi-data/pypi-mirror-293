# -*- coding: UTF-8 -*-

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse


class AppDB(SyncAPIResource):

    def __init__(self, _client) -> None:
        super().__init__(_client)

    def create(self, data):
        response = self._client.post("/openapi/v1/db/app/data/insert", json=data)
        return APIResponse(response).json

    def delete(self, data):
        response = self._client.delete("/openapi/v1/db/app/data", json=data)
        return APIResponse(response).json

    def update(self, data):
        response = self._client.post("/openapi/v1/db/app/data/update", json=data)
        return APIResponse(response).json

    def query(self, data):
        response = self._client.post("/openapi/v1/db/app/data/list", json=data)
        return APIResponse(response).json

    def count(self, data):
        response = self._client.post("/openapi/v1/db/app/data/count", json=data)
        return APIResponse(response).json

    def get_upload_token(self, app_key: str = "", file_name: str = ""):
        url = f"/openapi/v1/square/app/admin/upload/token?appKey={app_key}&type=other&fileName={file_name}"
        response = self._client.get(url)
        if response.status_code != 200:
            raise Exception(f"get upload token failed: {response.text}")
        return APIResponse(response).json

    def create_table(self, data):
        response = self._client.post(
            "/openapi/v1/db/app/table/create", json=data
        )
        return APIResponse(response).json

    def delete_table(self, data):
        response = self._client.delete(
            "/openapi/v1/db/app/table", json=data
        )
        return APIResponse(response).json

