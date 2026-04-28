import os 
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage


load_dotenv()
# llm=ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )
llm = ChatOllama(model="llama3:8b")
prompt = ChatPromptTemplate.from_messages([
    ("system","You are a Python programming teacher with 5+years of teaching experience for the students  and you need to  check whether the student get a clear understanding by asking the questions about a topic which he/she asked to you .until you get the expeted answer from the student for your question you need to teach the topic to his .keep the conversation simple as possible don't use very difficult or technical words more use it when it is necessary otherwise keep it simple as possible ."),
    MessagesPlaceholder(variable_name="history"),
    ("human","summarize the topic and clear the doubts of the students for this topic:{input}" )

])

chain=prompt|llm
chat=[]
print("Python Teacher Bot - Type 'exit' to quit")
print("-" * 40)
while True:

    user=input("You:")
    if user.lower()=="exit":
        print("session ended sucessfully")
        break

    response = chain.invoke({"history":chat,"input":user})
    print(f"\nTeacher:{response.content}\n")
    chat.append(HumanMessage(content=user))
    chat.append(AIMessage(content=response.content))
