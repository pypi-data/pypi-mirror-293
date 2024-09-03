from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore

class VectorStore:
    def __init__(self,embedding_model, project_id, dataset, table, location, credential):
        self.project_id = project_id
        self.dataset = dataset
        self.table = table
        self.location = location
        self.embedding_model = embedding_model
        self.credential = credential

    def create_store(self):
        # Initialize the Vertex AI Embeddings
        self.embedding = VertexAIEmbeddings(
            model_name= self.embedding_model,
            project= self.project_id,
            credentials = self.credential
        )

        # Initialize the BigQuery Vector Store
        self.store = BigQueryVectorStore(
            project_id=self.project_id,
            dataset_name=self.dataset,
            table_name=self.table,
            location=self.location,
            embedding=self.embedding,
            credentials = self.credential
        )

        return self.store
