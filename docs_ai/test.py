from docs_ai.utils import get_chat_gpt3_5_response

r = get_chat_gpt3_5_response(system="You are a medical doctor", user="What doctor should I see if I Have rush", assistant="")
print(r)