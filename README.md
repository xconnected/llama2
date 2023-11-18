# llama2

This repo contains a personal attempt to use the LLama2 model with a simple GUI.
The GUI is not fool proof but shall make it easier to play around with the language model.
The implementation is based on python, but for execution a c++ compiler e.g. gcc or similar must be available.
On Linux systems this is normally out of the box, on Windows systems the free visual studio distribution should be sufficient.

Rhe core of the example is build on llama-cpp-python library and the Llama2 model.
The latter one can be downloaded from HuggingFace (requires a registration at Meta as well)

**The model must be in the .gguf format.**

## Recommended Installation Approach

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

In future the GUI will offer to choose from different prompts.

Note:
I observed different behaviour on different systems, based on the prompt formatting.
If the system behaves strane try to remove line breaks or spaces from the prompt.
Note:
