import os
from markdown import markdown
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from config import Config
from engine import run_llm, init_llm, conversation
from dotenv import load_dotenv
import time
import logging


load_dotenv()

logging.basicConfig(level=logging.DEBUG, filename='llm.log')

logging.info(f'Load Config')
cfg = Config()

logging.info(f'Init LLM')
init_llm(cfg.llm_model, cfg.llm_context_size)

logging.info(f'Start Flask')
app = Flask(__name__)
        
@app.route('/')
def index():
    system_message = cfg.llm_system_message
    nb_tokens = cfg.llm_max_tokens
    return render_template("index.html", system_message=system_message, nb_tokens=nb_tokens)


@app.route('/interaction', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    logging.info(f'u:{user_message} c:{cfg.llm_context}')
    
    t_start = time.time()
    
    # Call Llama2 function with the message
    llm_output = run_llm(user_message, 
                         cfg.llm_system_message, 
                         cfg.llm_context, 
                         cfg.llm_max_tokens)

    t_elapsed = time.time() - t_start

    # Extract response
    response = llm_output['choices'][0]['text']

    return jsonify({'elapsed': f' [{t_elapsed:.2f}s] ', 'message': markdown(response)})


@app.route('/system-message', methods=['POST'])
def set_system_message():
    data = request.get_json()
    cfg.llm_system_message = data.get('message')
    return jsonify({'message': cfg.llm_system_message})


@app.route('/nb-tokens', methods=['POST'])
def set_nb_tokens():
    data = request.get_json()
    cfg.llm_max_tokens = int(data.get('message'))
    return jsonify({'message': cfg.llm_max_tokens})


@app.route('/context', methods=['POST'])
def set_context():
    data = request.get_json()
    cfg.llm_context = data.get('message')
    return jsonify({'message': cfg.llm_context})


@app.route('/conversation', methods=['GET'])
def get_conversation():
    return jsonify(conversation)


if __name__ == '__main__':
    app.run(host=cfg.app_host, port=cfg.app_port, debug=True)
