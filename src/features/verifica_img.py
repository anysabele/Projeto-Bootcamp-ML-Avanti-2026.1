import os

import pandas as pd
from PIL import Image


def verifica_img_corrompida(diretorio_imagens, nome_csv="dataset_limpo.csv"):
    lista_dados = []
    arquivos_corrompidos = 0

    diretorio_dataset = os.path.normpath(diretorio_imagens)

    root_projeto = os.path.dirname(os.path.dirname(diretorio_dataset))

    for root, dirs, files in os.walk(diretorio_imagens):
        for file in files:
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")
            ):
                caminho_completo = os.path.join(root, file)
                try:
                    with Image.open(caminho_completo) as img:
                        img.verify()

                    caminho_relativo = os.path.relpath(caminho_completo, root_projeto)
                    caminho_relativo = caminho_relativo.replace("\\", "/")
                    subtipo = os.path.basename(root)

                    pasta_pai = os.path.dirname(root)
                    classe_principal = os.path.basename(pasta_pai)

                    label_composto = f"{classe_principal}/{subtipo}"

                    lista_dados.append(
                        {
                            "caminho_completo": caminho_relativo,
                            "nome_arquivo": file,
                            "classe": classe_principal,
                            "subtipo": subtipo,
                            "label_final": label_composto,
                        }
                    )
                except Exception:
                    print(f"Corrompido: {caminho_completo}")
                    arquivos_corrompidos += 1
    if lista_dados:
        df = pd.DataFrame(lista_dados)
        df = df.sort_values(by="label_final")
        df.to_csv(nome_csv, index=False)
        print(f"CSV gerado: {nome_csv}")
        print(f"Total de imagens válidas: {len(df)}")
        print(f"Arquivos corrompidos ignorados: {arquivos_corrompidos}")
    else:
        print("Nenhuma imagem válida encontrada.")


if __name__ == "__main__":
    pasta_dataset = r"/home/joaoinacio/Projeto-Bootcamp-ML-Avanti-2026.1/data/raw"
    verifica_img_corrompida(pasta_dataset)
