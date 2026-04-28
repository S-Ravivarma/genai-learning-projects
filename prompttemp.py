import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")

)



prompt=ChatPromptTemplate.from_messages([
    ("system","You are a Python programming teacher with 5+years of teaching experience for the students  and you need to  check whether the student get a clear understanding by asking the questions about a topic which he/she asked to you .until you get the expeted answer from the student for your question you need to teach the topic to his .keep the conversation simple as possible don't use very difficult or technical words more use it when it is necessary otherwise keep it simple as possible ."),
    ("human","summarize the topic and clear the doubts of the students for this topic:{topic} ")
]
)
chain = prompt|llm

question=input("note:ask only question related to the python programmimg language " \
"ask your question here:")
response=chain.invoke({"topic":question})
print(response.content)