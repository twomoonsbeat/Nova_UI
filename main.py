from langchain.chat_models import ChatOpenAI
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, PromptHelper, ServiceContext, StorageContext, load_index_from_storage
import openai
import os
import pyttsx3



def play_text_as_sound(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


API_KEY = ""

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = API_KEY


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 0.2
    chunk_size_limit = 600
    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(
        temperature=0.5, model_name="gpt-4", max_tokens=num_outputs)) # type: ignore

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context)

    index.storage_context.persist('./storage')

    return index


def ask_ai(query: str):
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    while True:
        index = load_index_from_storage(storage_context=storage_context)
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return response


construct_index("data")
