import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

file = open("src/fade/system_prompt.txt", 'r')
system_prompt = file.read()

def detect_fallacy(phrase):
    chat_completion = client.chat.completions.create(

        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": system_prompt,
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": phrase,
            }
        ],

        model="llama-3.1-70b-versatile",

        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content