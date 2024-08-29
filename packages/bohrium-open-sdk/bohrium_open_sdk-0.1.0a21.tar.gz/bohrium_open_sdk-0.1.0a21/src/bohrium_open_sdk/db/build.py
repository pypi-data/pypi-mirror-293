# -*- coding: UTF-8 -*-

from bohrium_open_sdk.db.node import Op, OperatorNode, Condition
from bohrium_open_sdk.db.app import App
import json


def Where(key: str, op: Op, value) -> OperatorNode:
    return OperatorNode(None, Condition.AND).And(key, op, value)


class SQL:
    def __init__(self, table, ak="", app_key="", openapi_addr=""):
        self.table = table
        self.ak = ak
        self.app_key = app_key
        self.root = None
        self._page = 1
        self._page_size = 10
        self._select = []
        self._data = []
        self._order = []
        self._app = App(base_url=openapi_addr, access_key=ak)
        self._app_id = self._app.get_app_id(app_key)

    def Select(self, *args):
        for key in args:
            self._select.append(key)
        return self

    def Where(self, key: str, op: Op, value):
        if self.root is None:
            self.root = Where(key, op, value)
        else:
            self.root.And(key, op, value)
        return self

    def Or(self, *args):
        self.root.Or(*args)
        return self

    def And(self, *args):
        self.root.And(*args)
        return self

    def page(self, count):
        self._page = count
        return self

    def page_size(self, count):
        self._page_size = count
        return self

    def order(self, key, is_asc: bool):
        o = -1
        if is_asc:
            o = 1
        order = {
            "filed": key,
            "type": o,
        }

        self._order.append(order)
        return self

    def Create(self, obj):
        if type(obj) is dict:
            self._data.append(obj)
        elif type(obj) is list:
            self._data.extend(obj)
        else:
            raise ValueError("not supprot this type")

        json_data = {
            "appId": str(self._app_id),
            "tableName": self.table,
            "data": self._data,
        }
        return self._app.create(json_data)

    def Delete(self):
        filters = self._dict()
        json_data = {
            "appId": str(self._app_id),
            "tableName": self.table,
            "filters": filters
        }
        return self._app.delete(json_data)

    def Count(self):
        filters = self._dict()
        json_data = {
            "appId": str(self._app_id),
            "tableName": self.table,
            "filters": filters
        }
        return self._app.count(json_data)


    def Update(self, obj):
        filters = self._dict()
        json_data = {
            "appId": str(self._app_id),
            "tableName": self.table,
            "filters": filters,
            "values": obj,
        }
        return self._app.update(json_data)

    def Find(self):
        filters = self._dict()
        json_data = {
            "appId": str(self._app_id),
            "tableName": self.table,
            "filters": filters,
            "selectedFields": [],
            "orderBy": [],
            "page": self._page,
            "pageSize": self._page_size,
        }
        if len(self._select) > 0:
            json_data["selectedFields"] = self._select

        if len(self._order) > 0:
            json_data["orderBy"] = self._order
        j = json.dumps(filters)
        print(j)
        return self._app.query(json_data)

    def _dict(self):
        return self.root.dict()

    def _build(self):
        return json.dumps(self.root.dict(), indent=4)