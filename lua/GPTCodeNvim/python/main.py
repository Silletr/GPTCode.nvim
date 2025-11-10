import os
import sys
from g4f import set_cookies, Client

set_cookies(
    ".chatgpt.com",
    {
        "__Secure-next-auth.session-token": os.getenv("CHATGPT_SESSION"),
        "oai-did": os.getenv("CHATGPT_DID"),
    },
)

text = sys.argv[1] if len(sys.argv) > 1 else ""
print(f"Received from Neovim: {text}")

client = Client()
response = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": text}]
)

print(response.choices[0].message.content)
