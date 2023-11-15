import os
from markdown import markdown
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama


template_1 = """
<s>[INST]
<<SYS>>{system_message}<</SYS>>
{user_message}
[/INST]"""

template_2 = """
<s>[INST]
<<SYS>>{system_message}. Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Context: {context}
<</SYS>>
{user_message}
[/INST]"""

load_dotenv()


class Config():
    def __init__(self):
        self._app_host = ""
        self._app_port = 0
        self._llm_model = ""
        self._llm_max_tokens = 0
        self._llm_context_size = 0
        self._llm_system_message = ''
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
        if value == '':
            self._llm_system_message = "You are a helpful assistant"
        else:
            self._llm_system_message = str(value).strip()

    @property
    def llm_context(self):
        return self._llm_context

    @llm_context.setter
    def llm_context(self, value):
        self._llm_context = str(value).strip()


app = Flask(__name__)

cfg = Config()

cfg.app_host = os.environ.get('HOST')
cfg.app_port = os.environ.get('PORT')
cfg.llm_model = os.environ.get('LLM_MODEL')
cfg.llm_context_size = os.environ.get('LLM_CONTEXT_SIZE')
cfg.llm_max_tokens = os.environ.get('LLM_MAX_TOKENS')
cfg.llm_system_message = os.environ.get('LLM_SYSTEM_MESSAGE')
cfg.llm_context = ''

conversation = []

LLM = Llama(model_path=cfg.llm_model, n_ctx=cfg.llm_context_size)

def run_llama(user_message):
    global cfg

    context = cfg.llm_context
    if len(context) > 10:
        template = template_2
    else:
        template = template_1

    prompt = template.format(
        system_message=cfg.llm_system_message,
        context=context,
        user_message=user_message)

    return LLM(prompt, max_tokens=cfg.llm_max_tokens)


@app.route('/')
def index():
    global cfg
    system_message = cfg.llm_system_message
    nb_tokens = cfg.llm_max_tokens
    return render_template("index.html", system_message=system_message, nb_tokens=nb_tokens)


@app.route('/interaction', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')

    # Call Llama2 function with the message
    llm_output = run_llama(message)

    # Extract response
    response = llm_output['choices'][0]['text']

    # Storing conversation history
    conversation.append({'user': message, 'bot': response})

    return jsonify({'message': markdown(response)})


@app.route('/system-message', methods=['POST'])
def set_system_message():
    global cfg
    data = request.get_json()
    cfg.llm_system_message = data.get('message')
    return jsonify({'message': cfg.llm_system_message})


@app.route('/nb-tokens', methods=['POST'])
def set_nb_tokens():
    global cfg
    data = request.get_json()
    cfg.llm_max_tokens = int(data.get('message'))
    return jsonify({'message': cfg.llm_max_tokens})


@app.route('/context', methods=['POST'])
def set_context():
    global cfg
    data = request.get_json()
    cfg.llm_context = data.get('message')
    return jsonify({'message': cfg.llm_context})


@app.route('/conversation', methods=['GET'])
def get_conversation():
    return jsonify(conversation)


if __name__ == '__main__':
    app.run(host=cfg.app_host, port=cfg.app_port, debug=True)
