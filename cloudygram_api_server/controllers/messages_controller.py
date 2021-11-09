from cloudygram_api_server.models import UserModels, TtModels
from cloudygram_api_server.telethon.telethon_wrapper import *
from cloudygram_api_server.scripts import jres
from pyramid_handlers import action
from pyramid.request import Request
import asyncio, concurrent.futures
from typing import List


class MessagesController(object):
    __autoexpose__ = None

    def __init__(self, request: Request):
        self.request = request
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @action(name="getMessages", renderer="json", request_method="GET")
    def get_messages_req(self):
        phone_number: str = self.request.matchdict["phoneNumber"][1:]
        result = self.pool.submit(
                asyncio.run,
                get_messages(phone_number)
                ).result()
        return jres(TtModels.message_list(result), status=200)

    @action(name="deleteMessages", renderer="json", request_method="POST")
    def delete_messages_req(self):
        phone_number: str = self.request.matchdict["phoneNumber"][1:]
        message_ids: List[str] = self.request.json_body["ids"]
        self.pool.submit(
            asyncio.run,
            delete_messages(phone_number, message_ids)
        ).result()
        return jres(UserModels.success(), status=200)

