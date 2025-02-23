from llama_index.core import (
    Document, 
    VectorStoreIndex, 
    StorageContext, 
    PromptTemplate, 
    load_index_from_storage, 
    get_response_synthesizer,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from src.configs.config_loader import settings
from glob import glob
import json
import os

class RAGBuilder:
    def __init__(self, persist_dir: str="./cf_embeddings", json_file_dir: str="./codeforces"):
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
        self.llm = Gemini(
            model=settings.rag.model, 
            temperature=settings.rag.temperature
        )
        self.embed_model = GeminiEmbedding(model_name="models/text-embedding-004")
        self.persist_dir=persist_dir
        self.json_file_dir=json_file_dir
        self.splitter = SentenceSplitter(chunk_size=400, chunk_overlap=0)

    def _create_docs(self):
        files_path = [f for f in glob(f"{self.json_file_dir}/*.json") if not f.endswith("index.json") and not f.endswith("failure.json")]
        docs = []
        for file_path in files_path:
            with open(file_path, "r") as file:
                problem = json.load(file)
            doc = Document(text=f'Description: {problem["problem_statement"]} \n\n', 
                            id_=problem["id"],
                            metadata={
                                "title": problem["title"],
                                "relevant_algorithm": problem["tags"],
                                "difficulty": problem["rating"]
                            }
                )
            doc.excluded_llm_metadata_keys = ["title"]
            docs.append(doc)
        return docs

    def _build_index(self):
        docs = self._create_docs()
        index = VectorStoreIndex.from_documents(docs, transformations=[self.splitter], embed_model=self.embed_model, show_progress=True)
        index.storage_context.persist(persist_dir=self.persist_dir)
        return index

    def load_index(self):
        if not os.path.exists(self.persist_dir):
            index = self._build_index()
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
            index = load_index_from_storage(storage_context, embed_model=self.embed_model)
        return index

    def update_index(self):
        index = self.load_index()
        docs = self._create_docs()
        index.refresh_ref_docs(docs)
        index.storage_context.persist(persist_dir=self.persist_dir)
        return index

    def build_query_engine(self):
        index = self.load_index()

        # configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=10,
        )

        # configure query
        qa_prompt = PromptTemplate(settings.rag.prompt_tmpl)

        # configure response synthesizer using the PromptTemplate
        response_synthesizer = get_response_synthesizer(
            llm=self.llm,
            response_mode="compact",
            text_qa_template=qa_prompt
        )

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
        )
        return query_engine

if __name__ == "__main__":
    rag = RAGBuilder()
    query_engine = rag.build_query_engine()
    problem = "You are given a set of coins of different denominations and an integer amount representing a total amount of money. Return the minimum number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1. You may assume that you have an infinite number of each kind of coin."
    print(str(query_engine.query(problem)))