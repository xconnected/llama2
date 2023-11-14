import os
from markdown import markdown
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama

load_dotenv()

app_host = os.environ.get('HOST')
app_port = os.environ.get('PORT')
app_model = os.environ.get('MODEL')


llama_context=2048
llama_max_tokens=100
llama_system_message = "You are a helpful assistant and deliver closed sentences"
llama_prompt_template="<s>[INST] <<SYS>> {system_message} <</SYS>> {user_message} [/INST]"

app = Flask(__name__)

# Just a simple dictionary to simulate a conversation, replace this with your logic
conversation = []

# define n_ctx manually to permit larger contexts
LLM = Llama(model_path=app_model, n_ctx=llama_context)


def run_llama(message):
	input_message = llama_prompt_template.format(system_message=llama_system_message, user_message=message)
	return LLM(input_message, max_tokens=llama_max_tokens)


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

	return ({'message' : markdown(response)})

@app.route('/conversation', methods=['GET'])
def get_conversation():
	return jsonify(conversation)

if __name__ == '__main__':
	app.run(host=app_host, port=app_port, debug=True)
