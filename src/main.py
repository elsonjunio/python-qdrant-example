from pathlib import Path
from core.database import VectorDatabase
from core.extractors import get_extractor
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    db = VectorDatabase()

    while True:
        clear_screen()
        print('=== Sistema de Gerenciamento de Documentos ===')
        print('1. Adicionar documento')
        print('2. Buscar informação')
        print('3. Sair')

        choice = input('Escolha uma opção: ')

        if choice == '1':
            file_path = input(
                'Digite o caminho do arquivo (PDF ou áudio): '
            ).strip()
            if not Path(file_path).exists():
                input(
                    'Arquivo não encontrado. Pressione Enter para continuar...'
                )
                continue

            try:
                ext = Path(file_path).suffix
                extractor = get_extractor(ext)
                documents = extractor.extract(file_path)

                if documents:
                    db.save_documents(documents)
                    print(
                        f'Documento processado e salvo com sucesso! {len(documents)} trechos extraídos.'
                    )
                else:
                    print('Nenhum conteúdo válido foi extraído do arquivo.')

                input('Pressione Enter para continuar...')
            except Exception as e:
                print(f'Erro ao processar arquivo: {str(e)}')
                input('Pressione Enter para continuar...')

        elif choice == '2':
            query = input('Digite sua pergunta: ').strip()
            if not query:
                continue

            results = db.search(query)

            print('\nResultados encontrados:')
            for i, result in enumerate(results, 1):
                print(f'\nResultado {i} (Similaridade: {result.score:.2f}):')
                print(result.content)
                print('-' * 50)

            input('\nPressione Enter para continuar...')

        elif choice == '3':
            print('Saindo...')
            break

        else:
            input('Opção inválida. Pressione Enter para continuar...')


if __name__ == '__main__':
    main()
