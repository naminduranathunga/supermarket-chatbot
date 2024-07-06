from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_1"))

def generate_final_response(question, context, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Answer the user's questions."},
                {"role": "system", "content": context},
                {"role": "user", "content": question},
            ]
        )
    return response.choices[0].message.content