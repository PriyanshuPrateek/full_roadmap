import faiss
import numpy as np
import os
import pickle


class VectorStore:

    def __init__(self, dimension=384, index_path="vector_store/faiss.index", meta_path="vector_store/texts.pkl"):

        self.dimension = dimension
        self.index_path = index_path
        self.meta_path = meta_path

        if os.path.exists(index_path) and os.path.exists(meta_path):

            self.index = faiss.read_index(index_path)

            with open(meta_path, "rb") as f:
                self.texts = pickle.load(f)

        else:

            self.index = faiss.IndexFlatIP(dimension)

            self.texts = []


    def normalize(self, embedding):

        embedding = np.array(embedding).astype('float32')

        norm = np.linalg.norm(embedding)

        if norm == 0:
            return embedding

        return embedding / norm


    def add(self, embedding, text):

        if text in self.texts:
            return  

        embedding = self.normalize(embedding)

        embedding = np.array([embedding]).astype('float32')

        self.index.add(embedding)

        self.texts.append(text)

        self.save()


    def search(self, embedding, k=5):

        if len(self.texts) == 0:
            return []

        embedding = self.normalize(embedding)

        embedding = np.array([embedding]).astype('float32')

        similarities, indices = self.index.search(embedding, k)

        results = []

        threshold = 0.7

        for i, idx in enumerate(indices[0]):

            sim = similarities[0][i]

            if idx < len(self.texts) and sim >= threshold:

                results.append(self.texts[idx])

        return results


    def save(self):

        os.makedirs("vector_store", exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "wb") as f:
            pickle.dump(self.texts, f)