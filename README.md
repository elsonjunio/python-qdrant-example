# Sistema de Vetorização e Busca de Documentos

Desenvolvi este projeto para testar o funcionamento do Qdrant. Este é um sistema Python para processamento, vetorização e busca semântica de documentos usando o banco de dados vetorial Qdrant.



## Visão Geral

Este sistema oferece:
- Extração de documentos (PDF e áudio)
- Vetorização de texto usando sentence-transformers
- Busca semântica via Qdrant
- Interface de linha de comando simples

Tecnologias utilizadas:
- Qdrant (banco de dados vetorial)
- SentenceTransformers (vetorização de texto)
- PyPDF2 (processamento de PDF)
- SpeechRecognition (processamento de áudio)

## Instalação

1. Clone o repositório e instale as dependências:
   ```bash
    git clone https://github.com/elsonjunio/python-qdrant-example.git
    cd python-qdrant-example.git
    poetry install
   ```
2. Execute o Qdrant (o sistema espera localhost:6333 por padrão):
   ```bash
    cd docker
    docker compose up -d
   ```
## Componentes Principais

```bash
.
├── docker
│   └── docker-compose.yaml # Arquivo de configuração docker para executar Qdrunt
├── documents
│   └── ue000057.pdf # Documento em PDF para teste
├── pyproject.toml # Configuração do projeto
├── README.md # Este doc
└── src
    ├── core
    │   ├── database.py # Operações com o banco vetorial
    │   ├── extractors.py # Lógica de extração de documentos
    │   ├── __init__.py
    │   └── models.py # Estruturas de dados
    └── main.py # Interface de linha de comando
```

## Fluxo de Dados

    Entrada: Arquivo PDF ou de áudio

    Extração: Conteúdo de texto é extraído

    Vetorização: Texto é convertido em embeddings

    Armazenamento: Vetores são salvos no Qdrant

    Consulta: Usuário busca com linguagem natural

    Resultados: Documentos similares são retornados

## Como Usar

Execute o aplicativo principal:
```bash
poetry run src/main.py
```

Opções do menu:

    1-Adicionar Documento: Processa arquivos PDF ou áudio

    2-Buscar: Consulta o banco de dados vetorial

    3-Sair: Encerra o aplicativo

## Limitações

    Processamento de áudio requer conexão com a API do Google

    O modelo padrão (all-MiniLM-L6-v2) é otimizado para inglês

    Servidor Qdrant deve estar rodando separadamente

    PDFs grandes podem requerer mais memória para processamento