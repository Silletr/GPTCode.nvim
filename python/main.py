from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": "Hi!"}]
)

print(response.choices[0].message.content)
