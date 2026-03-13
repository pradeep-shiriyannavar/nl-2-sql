from config import client, LLM_MODEL, TEMPERATURE, MAX_TOKEN

def call_llm_system(prompt, system=None, model=LLM_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKEN):
    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,   # This is Azure CHAT DEPLOYMENT NAME
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()