import requests
from typing import (AnyStr, Optional)


class VkBot:
    def __init__(self, key: AnyStr, ver: AnyStr):
        self.key = key
        self.url = 'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={V}'
        self.v = ver

    def call_api_method(self, method_name, **params: dict) -> requests.Response:
        url = self.url
        params_lst = [f'{name}={value}' for name, value in params.items()]
        params = '&'.join(params_lst)
        request = url.format(
            method_name=method_name,
            parameters=params,
            token=self.key,
            V=self.v
        )
        request = requests.utils.requote_uri(request)
        resp = requests.post(request)
        return resp

    def send_message(self, user_id, message: AnyStr, keyboard: Optional[dict] = None, random_id: str = "0") \
            -> requests.Response:
        kwargs = dict()
        kwargs['user_id'] = user_id
        kwargs['message'] = message
        kwargs['random_id'] = random_id
        if keyboard:
            kwargs['keyboard'] = keyboard
        return self.call_api_method('messages.send', **kwargs)
