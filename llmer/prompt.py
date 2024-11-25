def chatml(messages):
    content = ""
    for message in messages:
        if message["role"] == "system":
            content += "<|im_start|>system\n" + message["content"] + "<|im_end|>\n"
        elif message["role"] == "user":
            content += "<|im_start|>user\n" + message["content"] + "<|im_end|>\n"
        elif message["role"] == "assistant":
            content += "<|im_start|>assistant\n" + message["content"] + "<|im_end|>\n"
    content += "<|im_start|>assistant\n"
    return content
