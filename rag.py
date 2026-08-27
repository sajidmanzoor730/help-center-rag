from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class HelpCenterRAG:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.docs = []

    def ingest(self, docs):
        self.docs = docs
        embeddings = self.model.encode(docs)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))

    def retrieve(self, query, k=3):
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb).astype('float32'), k)
        return [self.docs[i] for i in I[0]]

    def generate_response(self, query):
        context = self.retrieve(query)
        return f"Based on help center: {context} -> Answer: {query}"

rag = HelpCenterRAG()
rag.ingest(["How to reset 2FA?", "How to verify KYC?", "Coinbase fees"])
print(rag.generate_response("I forgot 2FA"))
