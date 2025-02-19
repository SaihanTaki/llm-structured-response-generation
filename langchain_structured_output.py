from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Literal, ClassVar, Optional
import os
import re


load_dotenv()


def load_documents(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs


def get_chat_llm(
    provider: Literal["openai", "google"]="google",
    temperature: int=0.1,
    max_token: int=2048
):
    if provider == "google":
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=temperature,
            max_tokens=max_token,
            api_key=os.environ["GOOGLE_API_KEY"]
        )
    elif provider == "openai":
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=temperature,
            max_tokens=max_token,
            api_key=os.environ["OPENAI_API_KEY"]
        )
    else:
        raise ValueError("Provider should be 'openai' or 'google'")
    return llm


class Chapter(BaseModel):
    SI: int
    title: str = Field(..., description="The title of the chapter / unit")
    start: int = Field(..., description="The start page of the chapter / unit")
    end: Optional[int] = Field(None, description="The end page of the chapter / unit")
    _counter: ClassVar[int] = 0
    
    def __init__(self, **data):
        if "SI" not in data or data["SI"] is None:
            data["SI"] = self.__class__._counter + 1
            self.__class__._counter += 1
        super().__init__(**data)
        return None


class ChapterList(BaseModel):
    chapters: list[Chapter]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at extracting chapter information from a table of contents. \
            Your task is to extract the chapter title, start page, and end page for each \
            chapter from the provided text. Don't include subchapters. Identify chapters - \
            title with chapter/unit prefix. Don't include the chapter/unit prefix in the title"
            "The output should be a JSON list of chapters, \
            formatted according to the following schema:\n{format_instructions}\n"
            "If an end page is not provided, please infer the end page from the start page \
            of the next chapter (end page = next start page - 1), \
            or the end of the document if it's the last chapter. "
            "If there is no next chapter, simply provide the last page number \
            provided in the content.",
        ),
        ("human", "Here is the table of contents:\n\n{table_of_content}"),
    ]
)


parser = PydanticOutputParser(pydantic_object=ChapterList)
prompt = prompt.partial(format_instructions=parser.get_format_instructions())


file_path = "example_book.pdf"
docs = load_documents(file_path)
content_docs = docs[5:7]
content = ""
for doc in content_docs:
    content += doc.page_content + "\n\n" 
llm = get_chat_llm("google")
chain = prompt | llm 
response = chain.invoke({"table_of_content": content}).content
response = re.sub(r'```|json', '', response)  
print(response)
