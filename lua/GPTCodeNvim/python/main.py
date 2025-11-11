#!/usr/bin/env python3
import os
import sys
import traceback
from dotenv import load_dotenv

# -------------------------------------------------
#  g4f (gpt4free) – set cookies only if the env vars exist
# -------------------------------------------------
try:
    from g4f import set_cookies, Client
except Exception as e:
    print("ERROR: Could not import g4f –", e, file=sys.stderr)
    sys.exit(1)


load_dotenv()


def set_g4f_cookies():
    token = os.getenv("CHATGPT_SESSION")
    did = os.getenv("CHATGPT_DID")
    if token and did:
        set_cookies(
            ".chatgpt.com",
            {
                "__Secure-next-auth.session-token": token,
                "oai-did": did,
            },
        )
    else:
        print(
            "WARN: CHATGPT_SESSION or CHATGPT_DID not set – running without auth.",
            file=sys.stderr,
        )


# -------------------------------------------------
#  Main
# -------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("ERROR: No prompt supplied.", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]

    print(f"Received from Neovim: {prompt!r}")

    set_g4f_cookies()

    client = Client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        print(answer)
    except Exception as exc:
        print("ERROR: g4f request failed:", exc, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
