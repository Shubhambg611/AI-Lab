from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from langserve import add_routes
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
model = ChatOpenAI(model_name=model_name)
system_template = "translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ('user','{text}')
])

parser = StrOutputParser()
chain=prompt_template|model|parser

app = FastAPI(title="langchain server",
              version="1.0",
              description="A simple API server using langchain")

add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)
