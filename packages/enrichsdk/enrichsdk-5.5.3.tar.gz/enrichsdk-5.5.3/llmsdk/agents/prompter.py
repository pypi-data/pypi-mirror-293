import os
import json
import time
import string
import hashlib

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks import get_openai_callback

from . import agent_events
from llmsdk.lib import SafeEncoder
from llmsdk.services.log import *

__all__ = ['LLMPromptAgent']

class LLMPromptAgent(object):
    """
    A geenric agent to run a query
    """

    def __init__(self,
                 name,
                 cred={},
                 platform="openai",
                 model="gpt-4o"):
        """
        init the bot
        name: name of the bot
        cred: credentials object
        platform: name of the platform backend to use
                default to openai platform for now
                will be extended in the future to suuport other platforms
        model: model name
        """

        start_time = time.time()

        # logging
        self.logger = get_logger()

        # defaults
        self.metadata = {}
        self.max_llm_tokens = 4000

        # name
        self.agent_name = name
        self.agent_type = "prompter"
        self.agent_id = self._create_id(f"{self.agent_name}_{start_time}")

        # creds
        self.cred = cred
        # LLM params
        self.platform = platform
        self.model = model

        # init the llm and embeddings objects
        self.llm = self._get_llm_objs(platform=self.platform,
                                      model=self.model,
                                      cred=self.cred)

        # agent defaults
        self.persona_prompt = "You are a highly advanced AI agent capable of solving tasks that you are presented with."

        self.errs = {
            "human_msg": "No prompt available, cannot call LLM",
        }

        # note metadata for this agent
        self.metadata = {
            "agent": {
                "name": self.agent_name,
                "name": self.agent_type,
                "platform": self.platform,
                "model": self.model,
            },
            "events": []
        }
        # log that the agent is ready
        duration = time.time() - start_time
        event = self._log_event(agent_events._EVNT_READY, duration)

    ## helper functions

    def _create_id(self, string):
        """
        create a unique identifier from a string
        """
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def _log_event(self, event_name, duration=0, params={}):
        """
        format an event object to store in the agent's metadata
        event_name: name of the event to log
        duration: how long did this event take, only needed for events
                   that require some waiting (e.g. RTT to LLM APIs)
        params: any other info needed to be logged
        """

        ts = time.time() - duration # to get the actual start time
        event_id = self._create_id(f'{event_name}-{ts}')

        event = {
            "id": event_id,
            "agent": self.agent_name,
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "timestamp": round(ts, 3),
            "duration": round(duration, 3),
            "name": event_name,
            "params": params,
        }
        self.metadata['events'].append(event)

        # log the event
        self.logger.debug(event_name,
                             extra={
                                 'source': self.agent_name,
                                 'data': json.dumps(event, indent=4, cls=SafeEncoder)
                             })


        return event

    def _get_llm_objs(self, platform, model, cred):
        # get the api key from creds
        api_key = self._get_api_key(cred, platform)

        # init the model
        if platform == "openai":
            # get the llm object
            llm = ChatOpenAI(temperature=0,
                             openai_api_key=api_key,
                             model=model,
                             max_tokens=self.max_llm_tokens,
                             request_timeout=60)
        else:
            llm = None

        return llm

    def _get_api_key(self, cred, key):
        """
        get the API key from the cred
        """
        api_key = None
        if isinstance(cred, str):
            api_key = cred
        if isinstance(cred, dict) and key in cred:
            api_key = cred[key]
        return api_key

    def _err_msg(self, t):
        msgs = {
            "field": "I'm having trouble understanding. Try another way of wording your query."
        }
        return msgs.get(t, "Something went wrong, try your query again.")

    ## interfaces

    def get_metadata(self):
        """
        return metadata collected by the agent
        """
        return self.metadata

    def run_prompt(self, sys_msg, human_msg):
        """
        generate a prompt for querying the LLM
        """
        # construct the prompt template
        messages = [
            SystemMessage(content=sys_msg),
            HumanMessage(content=human_msg),
        ]

        # call the LLM
        response = self.llm(messages)

        return response

    def prompt(self, prompt):
        """
        run a query using llm to answer questions about some text data
        this is useful when looking for answers about some context but without doing RAG
        """
        # construct the prompt
        sys_msg = prompt.get("persona", self.persona_prompt)
        human_msg = prompt.get("prompt")

        if human_msg == None:
            result = { "answer": self.errs["human_msg"] }

        else:
            # run prompt
            response = self.run_prompt(sys_msg, human_msg)
            result = { "answer": response.content }

        return result
