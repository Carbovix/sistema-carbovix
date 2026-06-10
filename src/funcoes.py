import src.menus as ui
import os
import csv

def adiciona_dado():
    os.system("cls")

    nome_maquina = input("Digite o nome da máquina: ")
    qnt_emissao = input("Digite a quantidade emitida pela máquina: ")

    linha = f"{nome_maquina}, {qnt_emissao}"

    with open("data/dados.csv", "a", newline="") as arquivo:
        arquivo.write(linha)

    print("\nDado adicionado com sucesso!")

def coletar_dados():
    consumo_kwh = float(input("Digite o consumo mensal em kWh: "))
    capital = float(input("Digite a quantidade de capital disponível (R$): "))
    prazo = float(input("Digite o prazo de retorno (anos): "))
    meta_reducao = float(input("Digite a meta de redução (em kg): "))

    carbono_indireto = consumo_kwh * 0.1

    with open("data/dados.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"""Consumo de energia (kWh/mês): {consumo_kwh} \nCapital disponível (R$): {capital} \nPrazo de retorno (anos): {prazo} \nMeta de redução (kg): {meta_reducao} \nEmissão de carbono indireta (kg CO2): {carbono_indireto}""")

    print("\nDados salvos com sucesso!")        

def deletar_dados():
    numero_dado = input("Digite o registro do dado que deseja deletar: ")

    arquivo_path = "data/dados.csv"
    linhas_mantidas = []
    encontrado = False
    with open(arquivo_path, "r", newline="") as arquivo:
        leitor_csv = csv.reader(arquivo)
        for linha in leitor_csv:
            if linha and linha[0] == numero_dado:
                encontrado = True
                continue
            linhas_mantidas.append(linha)

    if encontrado:
        with open(arquivo_path, "w", newline="") as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerows(linhas_mantidas)
            print(f"Dado com registro '{numero_dado}' foi deletado com sucesso.")
    else:
        print(f"O dado com registro '{numero_dado}' não foi encontrado.")
