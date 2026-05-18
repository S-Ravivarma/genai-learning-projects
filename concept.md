# GenAI Cheat Sheet

## Prompt Template
Reusable message structure. Variables use pannalam.
from langchain_core.prompts import ChatPromptTemplate

## LCEL Chain
prompt | llm | parser
Left to right — output of one becomes input of next.

## MessagesPlaceholder
Prompt la history inject aagra slot.
Illama pottaa — LLM previous messages kaanaadhu.

## Memory
chat_history = []
Every turn — HumanMessage + AIMessage append pannuvom.
Pass to chain — {"history": chat_history, "input": user}

## Output Parser
LLM response object → clean string convert pannudhu.
from langchain_core.output_parsers import StrOutputParser

## Local LLM
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3:8b")
No API key. No quota. Free. Slow.

## Cloud LLM
from langchain_google_genai import ChatGoogleGenerativeAI
API key needed. Fast. Quota limited.

## Provider Switch
Only LLM line change. Rest of code same.





You Said — "Upload design pannalai"
That's the surface answer.
Real reason — even if upload pannalum, current system handle panna mudiyaadhu.
Why?

Real Problem — LLM Has Token Limit
PDF oru 100 pages iruku. Full PDF — LLM ku send panna try pannina:
LLM: "I can only accept 8000 tokens"
100 page PDF: 50,000+ tokens
Result: CRASH
LLM — entire PDF memory la vecha maadiri process panna mudiyaadhu. Context window limit iruku.

Second Problem — No Search Mechanism
User kekkudhu:
"What is the refund policy mentioned in the document?"
Current system — full document scan panna mechanism illai. Enga iruku nu theriyaadhu.

So RAG Solves This — How?
Normal Chat:
User Question → LLM → Answer
(LLM knows nothing about your PDF)

RAG:
PDF → Split into chunks → Convert to numbers → Store in DB
         ↓
User Question → Search DB → Find relevant chunks
         ↓
Relevant chunks + Question → LLM → Answer with source

Real World Example
PDF: 200 page legal document

User: "What does clause 7.3 say about termination?"

RAG System:
1. Searches vector DB
2. Finds clause 7.3 — page 45
3. Sends only that chunk to LLM
4. LLM answers with exact reference

Current System:
→ Cannot do this. Period.