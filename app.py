import os
from markdown import markdown
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama


load_dotenv()


class Config():
    def __init__(self):
        self.host = os.environ.get('HOST')
        self.app_port = os.environ.get('PORT')
        self.llm_model = os.environ.get('LLM_MODEL')
        self.llm_context_size = self.set_context_size(os.environ.get('LLM_CONTEXT_SIZE'))
        self.llm_max_tokens = self.set_max_tokens(os.environ.get('LLM_MAX_TOKENS'))
        self.llm_system_message = self.set_system_message(os.environ.get('LLM_SYSTEM_MESSAGE'))

    def set_max_tokens(self, nb_tokens):
        nb_tokens=int(nb_tokens)
        if nb_tokens == 0:
            self.llm_max_tokens = 10
        else:
            self.llm_max_tokens = nb_tokens

    def set_context_size(self, ctx_size):
        ctx_size = int(ctx_size)
        if ctx_size == 0:
            self.llm_context_size = 2048
        else:
            self.llm_context_size = ctx_size

    def set_system_message(self, message):
        if message == '':
            self.llm_system_message = "You are a helpful assistant"
        else:
            self.llm_system_message = str(message).strip()


def get_prompt(user_message):
    template = "<s>[INST] <<SYS>> {system_message} <</SYS>>{user_message}[/INST]"
    return template.format(system_message=cfg.llm_system_message, user_message=user_message)


app = Flask(__name__)
cfg = Config()
conversation = []
LLM = Llama(model_path=cfg.llm_model, n_ctx=cfg.llm_context_size)


def run_llama(user_message):
    return LLM(get_prompt(), max_tokens=cfg.llm_max_tokens)


@app.route('/')
def index():
    return render_template("index.html", system_prompt=cfg.llm_system_message)


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


@app.route('/system_message', methods=['POST'])
def set_system_message():
    global cfg
    data = request.get_json()
    cfg.set_system_message(data.get('message')) 
    return jsonify({'message': cfg.llm_system_message})


@app.route('/conversation', methods=['GET'])
def get_conversation():
    return jsonify(conversation)


if __name__ == '__main__':
    app.run(host=app_host, port=app_port, debug=True)
