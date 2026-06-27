from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

model = ChatGroq(model='llama-3.3-70b-versatile', temperature=0.3)

chain = prompt | model

history = []

print("Chat with the bot (type 'quite' to exit)")

while True:
    question = input("You: ")
    if question.strip().lower() in {"quite", "exit"}:
        break

    answer = chain.invoke(
        {"history": history, "question": question}).content
    print("Bot: ", answer)

    history.append(HumanMessage(question))
    history.append(AIMessage(answer))

    print(f"(history now has {len(history)} messages)")

# print(history)