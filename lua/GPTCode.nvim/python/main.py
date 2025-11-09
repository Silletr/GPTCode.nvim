from g4f.client import Client

client = Client()
query = input("Enter query to AI: ")

response = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": query}]
)

print(response.choices[0].message.content)
