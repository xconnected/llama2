import os


class Config():

    def __init__(self):
        self._app_host = os.environ.get('HOST')
        self._app_port = os.environ.get('PORT')
        self._llm_model = os.environ.get('LLM_MODEL')
        self._llm_model = os.environ.get('LLM_MODEL')
        self._llm_prompts = os.environ.get('LLM_PROMPTS')
        self._llm_context_size = int(os.environ.get('LLM_CONTEXT_SIZE'))
        self._llm_max_tokens = int(os.environ.get('LLM_MAX_TOKENS'))
        self._llm_system_message = os.environ.get('LLM_SYSTEM_MESSAGE')
        self._llm_context = ''

    @property
    def app_host(self):
        return self._app_host

    @app_host.setter
    def app_host(self, value):
        self._app_host = value

    @property
    def app_port(self):
        return self._app_port

    @app_port.setter
    def app_port(self, value):
        self._app_port = value

    @property
    def llm_prompts(self):
        return self._llm_prompts

    @llm_prompts.setter
    def llm_prompts(self, value):
        self._llm_prompts = value.strip()

    @property
    def llm_model(self):
        return self._llm_model

    @llm_model.setter
    def llm_model(self, value):
        self._llm_model = value

    @property
    def llm_max_tokens(self):
        return self._llm_max_tokens

    @llm_max_tokens.setter
    def llm_max_tokens(self, value):
        if int(value) == 0:
            self._llm_max_tokens = 10
        else:
            self._llm_max_tokens = int(value)

    @property
    def llm_context_size(self):
        return self._llm_context_size

    @llm_context_size.setter
    def llm_context_size(self, value):
        if int(value) == 0:
            self._llm_context_size = 10
        else:
            self._llm_context_size = int(value)

    @property
    def llm_system_message(self):
        return self._llm_system_message

    @llm_system_message.setter
    def llm_system_message(self, value):
        if value.strip() == '':
            self._llm_system_message = "You are a helpful assistant"
        else:
            self._llm_system_message = str(value).strip()

    @property
    def llm_context(self):
        return self._llm_context

    @llm_context.setter
    def llm_context(self, value):
        self._llm_context = str(value).strip()

