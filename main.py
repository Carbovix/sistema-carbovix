import src.funcoes as fn
import src.menus as ui

while True:
    escolha = input(ui.MENU_PRINCIPAL)

    if escolha == "1":
        fn.adiciiona_dado(escolha)
