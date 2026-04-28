import os 
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm=ChatOllama(model="llama3:8b")

praser=StrOutputParser()

prompt = ChatPromptTemplate.from_messages([ ( "system", """You are an expert AI Research Assistant.

When user gives a topic:
1. Give a clear 3-line summary
2. List 3 key points
3. Give 1 real world application
4. Ask if user wants to explore any specific area

Keep responses structured and concise."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
    ])

chain=prompt|llm|praser

chat =[]

print("=" * 50)
print("   AI Research Assistant (Local Llama3)")
print("=" * 50)
print("Type any topic to research. Type 'exit' to quit.")
print("Type 'clear' to start fresh research.\n")
while True:
    user =input("Enter the Research topic :").strip()

    if not user:
        print("Please enter the topic name.\n")
        continue

    if user.lower()=="exit":
        print("goodbye")
        break

    if user.lower()=="clear":
        chat=[]
        print("chat cleared. start new chat.\n")
        continue

    print("\n Researching......\n")

    response = chain.invoke({
        "history":chat,
        "input":user
    })

    print(f"Assistant:\n{response}\n")
    print("-" * 50)

    chat.append(HumanMessage(content=user))
    chat.append(AIMessage(content=response))