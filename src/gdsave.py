from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Caminhos
input_file = "documents/texto_extraido.txt"

# Configurar modelo de vetorização
model = SentenceTransformer('all-MiniLM-L6-v2')

# Configurar cliente do QDrant
qdrant_client = QdrantClient("http://localhost:6333")

# Criar a coleção no QDrant
collection_name = "manual_vetorizado"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
)

# Função para tratar o texto e dividir em parágrafos
def process_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    pages = data.split("--- Página ")
    paragraphs = []
    for page in pages[1:]:  # Ignorar a introdução sem conteúdo
        lines = page.split("\n", 1)  # Quebrar título da página
        page_number = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""

        # Dividir conteúdo em parágrafos e adicionar ao resultado
        for paragraph in content.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                paragraphs.append({"page": page_number, "content": paragraph})
    return paragraphs

# Processar texto
paragraphs = process_text(input_file)

# Vetorizar e salvar no QDrant
for idx, paragraph in enumerate(paragraphs):
    vector = model.encode(paragraph["content"])  # Vetorizar o conteúdo
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "page": paragraph["page"],
                    "content": paragraph["content"]
                }
            )
        ]
    )

print(f"Texto vetorizado e salvo no QDrant na coleção '{collection_name}'.")