# A simple attempt to use Llama2

This repo contains a simple attempt to use the LLama2 model solely and fully locallywith a very simple GUI.
The GUI is not "fool proof" and is was made just to play around with the language model.

The implementation is based on standard python libraries. For the language model a c++ compiler like gcc or similar is required.
On Linux systems these compilers are normally available out-of-the-box. On Windows systems gcc or the free visual studio must be separately installed.

This example is not optimized and was tested only with CPU support. 
If an Nvidia GPU is present it should be detected and integrated. 
If not this can be easily accomplished, as the llama-cpp-python library supports this.

The core of the example is build on **llama-cpp-python** library and the Llama2 model from Meta.
The Llama2 model can be downloaded from HuggingFace (requires a registration)

## General Notes
- The model must be in the .gguf format. The older .ggml format won't work
- The GUI is crafted based on Flask (development server) with all the given limitations
- There is no indication if the model is busy - consult the console or the log files
- This example is the outcome of a few hours work. Most time was spend on the boilerplate (GUI etc.)
- The library **llama-cpp-python** perform the work, visit the author here: https://github.com/abetlen/llama-cpp-python
- There are security measures built in, so it is strongly recommended to not use this code in public!

## Installation

### Clone the repo 
```git clone <url>```

Optional: 
Enter the cloned folder and setup a virtual python environment 
```python -m venv .venv```

Activate the virtual python environment here shown on Linux
```source .venv/bin/activate```


### Install required libraries
```pip install -r requirements.txt```


### Download the LLM
Place the the llm into the cloned folder under ./data
if you decide to use a different folder, you need to update the ```.env``` file.
**The model must be in the .gguf format. The older .ggml format won't work**


### Customize the .env file 
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

### Customize the prompts.txt file (if desired)
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

**Note:** I observed different behaviour on different systems, based on the prompt formatting.
If the system behaves strane try to remove line breaks or spaces from the prompt.


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
The fields have following function:

- **Top-Left Max. number of tokens to generate::** System prompt to instruct the system how to behave
- **Middle-Left Formulate the system prompt:** Number of tokens created as response
- **Bottom-Left Context:** Context to be used to build the response. As mentioned above if there is any text in the context window, the prompt will be adjusted. However there is currently no check on the context size, so if it is too large the LLM will ignore parts of the prompt.
- **Top-Right Conversation:** Display the conversation. Next to the label "Llama2:" in brackets, the time it took to build the response is shown.
- **Bottom-Right "Entry Field":** User inquiery - where the text can be entered and submitted with the enter/retun key


## Example
![image](https://github.com/xconnected/llama2/assets/4428021/e0015f65-a253-4a4e-b722-094024a94abf)

![image](https://github.com/xconnected/llama2/assets/4428021/edbacc77-9e81-479b-ab28-1dca9640ec1b)

Well arent these responses impressive :D

**Note:** 

- The result shown was produced only with CPU and no GPU support.
- The language model used is: ```llama-2-7b-chat.Q5_K_S.gguf``` which is only 4.7GB in size

# Ideas
Will be implemented if I find the time, use case or demand

- Selection of additional prompts or crafting prompts on the GUI
- Selection of additional language model versions on the GUI
- Reinitialization of the LLM to adjust the context size
- Inclusion of context from pdf-files
- Inclusion of context from html-files / url
