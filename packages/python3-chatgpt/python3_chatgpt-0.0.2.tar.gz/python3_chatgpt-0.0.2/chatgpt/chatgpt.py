# -*- coding: utf-8 -*-
from openai import OpenAI
from log import log


class ChatGPT(object):
    def __init__(self,base_url,api_key):
        self.__client=OpenAI(api_key=api_key,base_url=base_url)
        self.__model="gpt-4o"
        self.__system_user={
                    "role": "system",
                    "content": "You are a helpful assistant."
                }

    def ask(self,question):
        log.info(f"begino to ask question:{question}.")
        rs = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                self.__system_user,
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        result=rs.choices[0].message.content.strip()
        log.info(f"the answer is: {result}")
        return result
