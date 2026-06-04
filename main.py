
import src.funcoes as fn
import src.menus as ui

while True:
    escolha = input(ui.MENU_PRINCIPAL)

    if escolha == "1":
        fn.adiciona_dado()

        pergunta = input("\n\nDeseja a fazer mais alguma ação (s/n)? ").lower().strip()

        if pergunta == "n":
            break
    
    elif escolha == "2":
        fn.ler_dados()

    elif escolha == "3":
        fn.atualiza_dados()
    
    elif escolha == "4":
        fn.deletar_dados()
