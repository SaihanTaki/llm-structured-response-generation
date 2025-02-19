from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import ClassVar, Optional
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
import json


load_dotenv()

client = OpenAI()


def load_documents(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs

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
    def to_json(self) -> str:
        return self.model_dump_json()



file_path = "example_book.pdf"
docs = load_documents(file_path)
content_docs = docs[5:7]
content = ""
for doc in content_docs:
    content += doc.page_content + "\n\n" 

messages=[
        {
            "role": "system",
            "content": (
                "You are an expert at extracting chapter information from a table of contents. "
                "Your task is to extract the chapter title, start page, and end page for each "
                "chapter from the provided text. Don't include subchapters. Identify chapters - "
                "title with chapter/unit prefix. Don't include the chapter/unit prefix in the title. "
                "If an end page is not provided, please infer the end page from the start page "
                "of the next chapter (end page = next start page - 1), "
                "or the end of the document if it's the last chapter. "
                "If there is no next chapter, simply provide the last page number "
                "provided in the content."
            ),
        },
        {"role": "user", "content": f"Here is the table of contents:\n\n{content}"},
    ]

response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=ChapterList,
            temperature=0.1,
            max_completion_tokens=2048,
        )

print(response.choices[0].message.parsed.to_json())