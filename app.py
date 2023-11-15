import os
from markdown import markdown
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama

load_dotenv()

app_host = os.environ.get('HOST')
app_port = os.environ.get('PORT')
llm_model = os.environ.get('LLM_MODEL')
llm_context_size = int(os.environ.get('LLM_CONTEXT_SIZE'))
llm_max_tokens = int(os.environ.get('LLM_MAX_TOKENS'))
llm_system_message = os.environ.get('LLM_SYSTEM_MESSAGE')

if llm_context_size == 0:
    llm_context_size = 2048

if llm_system_message == '':
    system_message = "You are a helpful assistant"

prompt_template = """
<s>[INST] <<SYS>> {system_message} <</SYS>>
{user_message}
[/INST]"""

app = Flask(__name__)

conversation = []

LLM = Llama(model_path=llm_model, n_ctx=llm_context_size)


def run_llama(user_message):
    input_message = prompt_template.format(system_message=llm_system_message,
                                           user_message=user_message)
    return LLM(input_message, max_tokens=llm_max_tokens)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')

    # Call Llama2 function with the message
    llama_output = run_llama(message)

    # Extract response
    response = llama_output['choices'][0]['text']

    # Storing conversation history
    conversation.append({'user': message, 'bot': response})
    return ({'message': markdown(response)})


@app.route('/conversation', methods=['GET'])
def get_conversation():
    return jsonify(conversation)


if __name__ == '__main__':
    app.run(host=app_host, port=app_port, debug=True)
