import src.funcoes as fn
import src.menus as ui
import os
os.system("cls")

while True:
    escolha = input(ui.MENU_PRINCIPAL)
    os.system("cls")

    if escolha == "1":
        fn.coletar_dados()

    elif escolha == "2":
        fn.ler_dados()

    elif escolha == "3":
        fn.atualiza_dados()

    elif escolha == "4":
        fn.deletar_dados()

    elif escolha == "5":
        fn.coletar_arduino()

    elif escolha == "6":
        fn.analisar_ia()

    else:
        print("Opção inválida. Tente novamente.")