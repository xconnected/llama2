# llama2

This repo contains a personal attempt to use the LLama2 model with a simple GUI.
The GUI is not fool proof but shall make it easier to play around with the language model.
The implementation is based on python, but for execution a c++ compiler e.g. gcc or similar must be available.
On Linux systems this is normally out of the box, on Windows systems the free visual studio distribution should be sufficient.

This example is not optimized and has been tested only with CPU support. 
If an Nvidia GPU is present it should be detected and integrated. 
If not this can be easily accomplished, as the llama-cpp-python library supports this.

The core of the example is build on llama-cpp-python library and the Llama2 model.
The Llama2 model can be downloaded from HuggingFace (requires a registration at Meta as well)

**The model must be in the .gguf format.**

## Installation

Clone the repo 
```git clone <url>```

Enter the cloned folder and setup a virtual python environment 
```python -m venv .venv```

Install required libraries
```pip install -r requirements.txt```

Download the LLM
Place the the llm into the cloned folder under ./data
if you decide to use a different folder, you need to update the ```.env``` file.

Customize the .env file 
The .env file can be adjusted to the actual needs. Except of the chosen language model, the default should work out-of-the-box
```
HOST=localhost --> preferred host name for the GUI
PORT=8081 --> port to access the GUI on the host
LLM_MODEL=./data/llama-2-7b-chat.Q5_K_S.gguf ---> selected language model including the path
LLM_PROMPTS=prompts.txt --> name of the file containing the prompts
LLM_CONTEXT_SIZE=2048 --> max context size 
LLM_MAX_TOKENS=200 --> max tokens to produce, can be adjusted on the gui
LLM_SYSTEM_MESSAGE=You are a helpful assistant --> default system message can be adjusted on the gui
```

Customize the prompts.txt file 
The prompts file contains the default prompts (basic, basic_context) as used by the example app
They can be adjusted as desired and follow the standard prompting practice for LLama.
Prompts are structured as follows:

```
#PromptName
<prompt text>
```

The prompt file as delivered contains (only basic and basic_context are used):

```
#basic
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message}
[/INST]

#basic_context
<s>[INST]<<SYS>>
{system_message}
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<</SYS>>
{context}

{user_message}
[/INST]

#memory
<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

{user_message_1} [/INST] {model_output_1} </s>\
<s>[INST] {user_message_2} [/INST] {model_output_2} </s>\
<s>[INST] {user_message_3} [/INST] 
```

By default the "basic" prompt is used. 
If there is any text in the context window, "basic_context" is being used.

In future the GUI will offer to choose from different prompts.

Note:
I observed different behaviour on different systems, based on the prompt formatting.
If the system behaves strane try to remove line breaks or spaces from the prompt.
Note:

## Usage

To start the example app enter:

```
# python app.py
```

In the console the initialization process and processing information of lama2 is displayed.
All other output is directed into the file ```llm.log```

When the system is up, it can be accessed woth the browser at the specified host e.g. ```localhost:8081```

![image](https://github.com/xconnected/llama2/assets/4428021/309c3b36-ae8a-4a64-ac74-beaaab74f53d)

The entry fields on the right, can be updated at any time. The update is initiated when leaving the text box.

As mentioned above if there is any text in the context window, the prompt will be adjusted.
However there is currently no check on the context size, so if it is too large the LLM will ignore parts of the prompt.

Inquieries to the LLM can be entered in the text boy below the conversation window and are submitted with the return key.

The inquiery is displayed together with the response in the conversation as shown below. 
Next to Llama2: in brackets it is shown how many seconds it took to create the response.

![image](https://github.com/xconnected/llama2/assets/4428021/d9410593-ad08-4680-8c1a-1a274f1247c4)

Well isn't this response impressive :D

Note: 
The result shown was produced only with CPU and no GPU support.
The language model used is: ```llama-2-7b-chat.Q5_K_S.gguf``` which is only 4.7GB in size
