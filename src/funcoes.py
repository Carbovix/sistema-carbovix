import src.menus as ui
import os
import csv

def adiciona_dado():
    os.system("cls")

    nome_maquina = input("Digite o nome da máquina: ")
    qnt_emissao = input("Digite a quantidade emitida pela máquina: ")

    linha = f"{nome_maquina}, {qnt_emissao}\n"

    with open("data/dados.csv", "a", newline="") as arquivo:
        arquivo.write(linha)

    print("\nDado adicionado com sucesso!")

def atualiza_dados():
    nome_maquina = input("Digite o nome da máquina que deseja atualizar: ")

    with open("data/dados.csv", "r") as arquivo:
        linhas = arquivo.readlines()

        todas_linhas = []
        index_linha = None
        dado = None

        for cont, linha in enumerate(linhas):
            todas_linhas.append(linha)
            partes = linha.split(", ")

            if partes[0] == nome_maquina:
                print(linha)
                index_linha = cont
                dado = partes

        if index_linha is None:
            print("Máquina não encontrada.")
            return

        pergunta = input(ui.MENU_ALTERACAO_DADO)

        if pergunta == "1":
            nome_atualizado = input("Digite o nome atualizado: ")
            linha_atualizada = f"{nome_atualizado}, {dado[1]}"

        elif pergunta == "2":
            quantidade_atualizada = input("Digite a quantidade atualizada: ")
            linha_atualizada = f"{dado[0]}, {quantidade_atualizada}"

    with open("data/dados.csv", "w") as arquivo:
        for i, linha in enumerate(todas_linhas):
            if i == index_linha:
                arquivo.write(linha_atualizada)
            else:
                arquivo.write(linha)       
def ler_dados():
    os.system("cls")
    nome_maquina = input("Digite qual maquina você deseja verificar: ")

    with open("data/dados.csv", "r") as arquivo:
        linhas = arquivo.readlines()
        
        
        for linha in linhas:
            dado = linha.split(", ")
            
            if dado[0] == nome_maquina:
                print(linha)

def deletar_dados():
    os.system("cls")
    nome_maquina = input("Digite o nome da máquina que deseja deletar: ")

    arquivo_path = "data/dados.csv"
    linhas_mantidas = []
    encontrado = False
    with open(arquivo_path, "r", newline="") as arquivo:
        leitor_csv = csv.reader(arquivo)
        for linha in leitor_csv:
            if linha and linha[0] == nome_maquina:
                encontrado = True
                continue
            linhas_mantidas.append(linha)

    if encontrado:
        confirmacao = input(f"Tem certeza que deseja deletar? (Digite: S para sim, N para não)").strip().upper()
        if confirmacao == "N":
            print("Operação de exclusão cancelada.")
            return

        with open(arquivo_path, "w", newline="") as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerows(linhas_mantidas)
        print(f"Dado da máquina '{nome_maquina}' foi deletado com sucesso.")
        input("Pressione Enter para continuar...")
    else:
        print(f"O dado da máquina '{nome_maquina}' não foi encontrado.")
        input("Pressione Enter para continuar...")
        

