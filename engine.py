from llama_cpp import Llama


template_1 = """
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message}
[/INST]"""

template_2 = """
<s>[INST]<<SYS>>
{system_message}
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<</SYS>>
{context}

{user_message}
[/INST]"""

template_3 = """ 
<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

{user_message_1} [/INST] {model_output_1} </s>\
<s>[INST] {user_message_2} [/INST] {model_output_2} </s>\
<s>[INST] {user_message_3} [/INST] 
"""

llm = None
conversation = []

def init_llm(model_path, context_size):
    global llm
    llm = Llama(model_path=model_path, n_ctx=int(context_size))


def run_llm(user_message, system_message, context, max_tokens):

    if  len(context.strip()) > 0:
        template = template_2
    else:
        template = template_1

    prompt = template.format(
        system_message=system_message,
        context=context,
        user_message=user_message)

    response = llm(prompt, max_tokens=max_tokens)

    conversation.append({'user': user_message, 'assistant': response['choices'][0]['text']})

    return response


