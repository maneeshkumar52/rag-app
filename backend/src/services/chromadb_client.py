import chromadb
import uuid

class ChromaDBClient:
    def __init__(self, db_url: str):
        self.client = chromadb.PersistentClient(path=db_url)

    def add_document(self, collection_name: str, document: dict):
        collection = self.client.get_or_create_collection(collection_name)
        collection.add(documents=[document])

    def get_document(self, collection_name: str, document_id: str):
        collection = self.client.get_collection(collection_name)
        return collection.get(ids=[document_id])

    def query_documents(self, collection_name: str, query: str, n_results: int = 5):
        collection = self.client.get_collection(collection_name)
        return collection.query(query=query, n_results=n_results)

    def delete_document(self, collection_name: str, document_id: str):
        collection = self.client.get_collection(collection_name)
        collection.delete(ids=[document_id])

    def ingest_document(self, collection_name: str, content: str, metadata: dict = None):
        collection = self.client.get_or_create_collection(collection_name)
        doc_id = str(uuid.uuid4())
        # Chroma expects 'ids', 'documents', and optionally 'metadatas'
        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata or {}]
        )

    def retrieve_documents(self, query: str, collection_name: str = "default", n_results: int = 2):
        collection = self.client.get_collection(collection_name)
        results = collection.query(query_texts=[query], n_results=n_results)
        # Adapt this to your ChromaDB result structure
        # Chroma returns results['documents'] as a list of lists
        docs = []
        if results and "documents" in results:
            for doc_list in results["documents"]:
                for doc in doc_list:
                    docs.append({"content": doc})
        return docs