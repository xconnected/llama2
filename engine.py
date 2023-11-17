from llama_cpp import Llama

llm = None
prompt_templates = dict()
conversation = []


def load_prompt_templates(prompt_file):

    with open(prompt_file, mode="r") as f:
        content = f.read()

    prompts = content.split('#')
    prompt_dict = dict()

    for prompt in prompts:
        prompt_title = prompt.split('\n')[0].strip()
        if prompt_title != '':
            prompt_text = '\n'.join(prompt.split('\n')[1:]).strip()
            prompt_dict[prompt_title] = prompt_text

    return prompt_dict


def init_llm(model_path, context_size, prompts_template_file):

    global llm
    llm = Llama(model_path=model_path, n_ctx=int(context_size))

    global prompt_templates
    prompt_templates = load_prompt_templates(prompts_template_file)


def run_llm(user_message, system_message, context, max_tokens):

    if len(context.strip()) > 0:
        prompt = prompt_templates['basic'].format(
                    system_message=system_message,
                    user_message=user_message)
    else:
        prompt = prompt_templates['basic_context'].format(
                    system_message=system_message,
                    context=context,
                    user_message=user_message)

    response = llm(prompt, max_tokens=max_tokens)

    conversation.append({'user': user_message,
                         'assistant': response['choices'][0]['text']})

    return response
