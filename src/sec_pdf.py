from PyPDF2 import PdfReader

# Caminho para o arquivo PDF e para o arquivo de saída
pdf_path = "documents/doc_a.pdf"
output_file = "documents/texto_extraido.txt"

# Inicializar um arquivo para salvar o conteúdo
with open(output_file, "w", encoding="utf-8") as file:
    # Carregar o PDF
    reader = PdfReader(pdf_path)

    # Ler todas as páginas
    for page_number, page in enumerate(reader.pages, start=1):
        # Extrair o texto da página
        text = page.extract_text()

        # Escrever a página no arquivo com separadores
        file.write(f"--- Página {page_number} ---\n")
        file.write(text)
        file.write("\n\n")  # Adiciona uma linha em branco após cada página

print(f"Texto extraído e salvo em: {output_file}")