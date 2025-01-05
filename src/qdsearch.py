from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client import QdrantClient


# Configurações
collection_name = "manual_vetorizado"  # Nome da coleção no QDrant
qdrant_host = "http://localhost:6333"  # Endereço do QDrant

# Configurar o modelo de vetorização
model = SentenceTransformer('all-MiniLM-L6-v2')

# Conectar ao QDrant
qdrant_client = QdrantClient(url=qdrant_host)

# Função para vetorizar uma pergunta
def vectorize_question(question: str):
    return model.encode(question)

# Função para buscar os vetores mais próximos no QDrant
def search_qdrant(question: str, top_k: int = 3):
    # Vetorizar a pergunta
    question_vector = vectorize_question(question)

    # Buscar no QDrant
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=question_vector,
        limit=top_k  # Número de resultados
    )
    
    # Retornar os resultados encontrados
    return results

# Testando com uma pergunta
if __name__ == "__main__":
    question = "O que são glândulas sebáceas?"
    top_k = 3  # Número de trechos relevantes para retornar

    results = search_qdrant(question, top_k)

    print("Resultados encontrados:")
    for result in results:
        print(f"Trecho: {result.payload['content']}")
        print(f"Similaridade: {result.score}")
        print("---")
