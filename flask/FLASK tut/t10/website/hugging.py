from transformers import pipeline

system_prompt = """
You are an assistant that only answers educational questions.
If the user asks non-educational questions,
reply with:
'Sorry, I can only answer educational questions.'
"""

user_prompt = "Write Python code to print hello world"

pipe = pipeline(
    "text-generation",
    model="distilgpt2"
)

prompt = system_prompt + "\nUser: " + user_prompt

result = pipe(prompt, max_new_tokens=50)

print(result[0]['generated_text'])