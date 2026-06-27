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

history = [HumanMessage("My name is Nirbhay."), AIMessage("Hi, Nirbhay!")]

print(chain.invoke({"history": history, "question": "What's in my name?"}).content)