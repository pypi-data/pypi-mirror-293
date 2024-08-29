# -*- coding: UTF-8 -*-

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse


class AppDB(SyncAPIResource):

    def __init__(self, _client) -> None:
        super().__init__(_client)

    def create(self, data):
        response = self._client.post(
            "/openapi/v1/db/app/data/insert", json=data
        )
        return APIResponse(response).json

    def delete(self, data):
        response = self._client.delete(
            "/openapi/v1/db/app/data", json=data
        )
        return APIResponse(response).json

    def update(self, data):
        response = self._client.post(
            "/openapi/v1/db/app/data/update", json=data
        )
        return APIResponse(response).json

    def query(self, data):
        response = self._client.post(
            "/openapi/v1/db/app/data/list", json=data
        )
        return APIResponse(response).json

    def count(self, data):
        response = self._client.post(
            "/openapi/v1/db/app/data/count", json=data
        )
        return APIResponse(response).json
