import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq()

PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699}

def get_price(item):
    print(F"tool called: get_prices({item})")
    return f"{PRICES.get(item.lower(), 'unknown')}"

tools = [{
    "type": "function",                                      # ①
    "function": {
        "name": "get_price",                                 # ②
        "description": "Get the price of a shop item the user asks about.",  # ③
        "parameters": {                                       # ④
            "type": "object",
            "properties": {"item": {"type": "string", "description": "the item name"}},
            "required": ["item"],
        },
    },
}]


def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(          # ① send message + tools menu
        model="llama-3.3-70b-versatile", messages=messages, tools=tools)
    msg = response.choices[0].message

    if msg.tool_calls:                                  # ② did it ask for a tool?
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)  # ③ read its request, run it
            result = get_price(args["item"])
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        response = client.chat.completions.create(      # ④ send it all back → nice answer
            model="llama-3.3-70b-versatile", messages=messages)
        msg = response.choices[0].message

    return msg.content

print(agent("How much are the bag?"))      # → tool fires → "₹799"
print(agent("Hi! What can you help with?"))   # → no tool → just chats