import src.menus as ui
import os
import csv

ARQUIVO_TXT = "data/dados.txt"
ARQUIVO_CSV = "data/emissoes.csv"


def _ler_dados_txt():
    dados = {}
    with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                dados[chave.strip()] = valor.strip()
    return dados


def _salvar_dados_txt(dados):
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as arquivo:
        for chave, valor in dados.items():
            arquivo.write(f"{chave}: {valor}\n")


def coletar_dados():
    os.system("cls")

    consumo_kwh = float(input("Digite o consumo mensal em kWh: "))
    capital = float(input("Digite a quantidade de capital disponível (R$): "))
    prazo = float(input("Digite o prazo de retorno (anos): "))
    meta_reducao = float(input("Digite a meta de redução (em kg): "))

    carbono_indireto = consumo_kwh * 0.1

    with open(ARQUIVO_TXT, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Consumo de energia (kWh/mês): {consumo_kwh}\n")
        arquivo.write(f"Capital disponível (R$): {capital}\n")
        arquivo.write(f"Prazo de retorno (anos): {prazo}\n")
        arquivo.write(f"Meta de redução (kg): {meta_reducao}\n")
        arquivo.write(f"Emissão de carbono indireta (kg CO2): {carbono_indireto}\n")

    os.system("cls")
    print("\nDados salvos com sucesso!")


def ler_dados():
    os.system("cls")

    try:
        dados = _ler_dados_txt()
    except FileNotFoundError:
        print("Nenhum dado cadastrado ainda.")
        return

    print()
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")
    
    input("\nDigite Enter para voltar... ")
    os.system("cls")


def atualiza_dados():
    os.system("cls")

    try:
        dados = _ler_dados_txt()
    except FileNotFoundError:
        print("Nenhum dado cadastrado ainda.")
        return

    print("\nDados atuais:")
    cont = 1
    for chave, valor in dados.items():
        print(f"[{cont}] {chave}: {valor}")
        cont += 1

    pergunta = input("\nDigite qual dado você deseja alterar: ").strip()

    if pergunta == "1":
        novo_valor = float(input("Digite o novo consumo de energia (kWh/mês): "))
        dados["Consumo de energia (kWh/mês)"] = str(novo_valor)
        dados["Emissão de carbono indireta (kg CO2)"] = str(novo_valor * 0.1)

    elif pergunta == "2":
        novo_valor = float(input("Digite o novo capital disponível (R$): "))
        dados["Capital disponível (R$)"] = str(novo_valor)

    elif pergunta == "3":
        novo_valor = float(input("Digite o novo prazo de retorno (anos): "))
        dados["Prazo de retorno (anos)"] = str(novo_valor)

    elif pergunta == "4":
        novo_valor = float(input("Digite a nova meta de redução (kg): "))
        dados["Meta de redução (kg)"] = str(novo_valor)

    else:
        os.system("cls")
        print("Opção inválida.")
        return

    _salvar_dados_txt(dados)
    os.system("cls")
    print("\nDado atualizado com sucesso!")

    input("\nDigite Enter para voltar... ")
    os.system("cls")


def deletar_dados():
    os.system("cls")

    try:
        dados = _ler_dados_txt()
    except FileNotFoundError:
        print("Nenhum dado cadastrado ainda.")
        return
    
    while True:
        print("\nDados atuais:")
        cont = 1
        for chave, valor in dados.items():
            print(f"[{cont}] {chave}: {valor}")
            cont += 1

        pergunta = input("\nDigite qual dado você deseja alterar: ").strip()

        chaves = list(dados.keys())
        mapa = {"1": chaves[0], "2": chaves[1], "3": chaves[2], "4": chaves[3]}

        if pergunta not in mapa:
            os.system("cls")
            print("Opção inválida.")
            continue
        
        else:
            chave_deletar = mapa[pergunta]
            break
    
    while True:
        confirmacao = input(f"Tem certeza que deseja deletar '{chave_deletar}'? (S/N): ").strip().lower()

        if confirmacao == "n":
            print("Operação de exclusão cancelada.")
            input("Digite Enter para voltar...")
            os.system("cls")
            return

        elif confirmacao == "s":
            del dados[chave_deletar]
            _salvar_dados_txt(dados)
            print(f"\nCampo '{chave_deletar}' deletado com sucesso.")
            
            input("\nDigite Enter para voltar... ")
            os.system("cls")
            return

        else:
            os.system("cls")
            print("Opção inválida!")
            continue

def coletar_arduino():
    os.system("cls")

    try:
        import serial
    except ImportError:
        print("Biblioteca 'pyserial' não instalada.")
        print("Execute: pip install pyserial")
        return

    porta   = input("Digite a porta COM do Arduino (ex: COM3): ").strip()
    duracao = int(input("Por quantos segundos deseja coletar leituras? "))

    print(f"\nConectando em {porta}...")

    try:
        arduino = serial.Serial(porta, 9600, timeout=1)
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    import time

    leituras = []
    tempo_fim = time.time() + duracao
    VAZAO_M3H = 10000
    DENSIDADE = 1.96

    print(f"Coletando por {duracao} segundos...\n")

    while time.time() < tempo_fim:
        linha = arduino.readline().decode("utf-8").strip()
        if not linha.startswith("PPM:"):
            continue
        try:
            ppm = float(linha.replace("PPM:", "").strip())
            leituras.append(ppm)
            print(f"  Leitura: {ppm} ppm")
        except ValueError:
            continue

    arduino.close()

    if not leituras:
        print("\nNenhuma leitura recebida. Verifique a porta e o Arduino.")
        return

    media_ppm = sum(leituras) / len(leituras)
    kg_por_seg = media_ppm * VAZAO_M3H / 3600 * DENSIDADE * 10**-6
    kg_por_mes = kg_por_seg * 60 * 60 * 24 * 30

    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Chaminé Industrial", round(kg_por_mes, 4)])

    print(f"\nMédia coletada:       {media_ppm:.2f} ppm")
    print(f"Emissão estimada/mês: {kg_por_mes:.2f} kg CO₂")
    print(f"\nDado salvo em {ARQUIVO_CSV} com sucesso!")
    
    input("\nDigite Enter para voltar... ")
    os.system("cls")


def analisar_ia():
    os.system("cls")

    try:
        from groq import Groq
    except ImportError:
        print("Biblioteca 'groq' não instalada.")
        print("Execute: pip install groq")
        return

    try:
        dados_empresa = _ler_dados_txt()
    except FileNotFoundError:
        print("Nenhum dado da empresa encontrado. Use a opção [1] primeiro.")
        return

    emissoes_diretas = []
    total_direto_kg  = 0.0

    try:
        with open(ARQUIVO_CSV, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if len(linha) >= 2:
                    try:
                        nome = linha[0].strip()
                        qtd  = float(linha[1].strip())
                        emissoes_diretas.append(f"{nome}: {qtd} kg CO₂/mês")
                        total_direto_kg += qtd
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass

    if not emissoes_diretas:
        emissoes_diretas = ["Nenhuma emissão direta registrada via Arduino ainda."]

    bloco_empresa = "\n".join(f"  {k}: {v}" for k, v in dados_empresa.items())
    bloco_csv     = "\n".join(f"  {e}" for e in emissoes_diretas)
    total_indireto = dados_empresa.get("Emissão de carbono indireta (kg CO2)", "0")

    try:
        total_geral = total_direto_kg + float(total_indireto)
    except ValueError:
        total_geral = total_direto_kg

    CHAVE_API = "SUA_CHAVE_AQUI"
    client = Groq(api_key=CHAVE_API)

    system_instruction = """Você é um especialista sênior em sustentabilidade, eficiência energética
e transição energética para o setor industrial brasileiro.

Você tem profundo conhecimento do mercado brasileiro, das políticas energéticas nacionais,
dos custos reais de cada tecnologia no Brasil e das soluções mais aplicadas na indústria nacional.

Referências que você deve usar nas suas análises:
- Eficiência Energética e Térmica: otimização de caldeiras, troca de motores e automação (IEDI/CNI).
- Substituição por Biomassa e Biocombustíveis: bagaço de cana, cavaco de madeira, biogás.
  Fontes biológicas respondem por ~48% da matriz energética industrial brasileira (IEA).
- Contratos de Energia Renovável (PPAs): compra direta de energia solar/eólica no mercado livre
  para neutralizar emissões de Escopo 2.
- Coprocessamento de Resíduos: substituição do coque de petróleo nos fornos de cimento por
  resíduos urbanos e industriais — estratégia madura no setor cimenteiro nacional.
- Reciclagem e Economia Circular: uso de sucata nas indústrias de aço e alumínio.
- Eletrificação de Processos Térmicos: substituição de caldeiras a gás/óleo por caldeiras elétricas,
  viável no Brasil pela matriz elétrica majoritariamente renovável.
- Créditos de carbono (mercado voluntário brasileiro): R$ 20 a R$ 150 por tCO₂.
- Energia solar fotovoltaica: R$ 3.000 a R$ 5.000 por kWp instalado, retorno típico de 4 a 7 anos.
- Filtros e lavadores de gases (scrubbers): R$ 50 mil a R$ 2 milhões conforme capacidade.
- Eficiência energética geral: R$ 20 mil a R$ 500 mil, retorno de 2 a 4 anos.

Suas respostas devem ser sempre em português, profissionais, diretas e aplicáveis à realidade brasileira."""

    prompt = f"""Analise os dados abaixo de uma empresa do setor industrial brasileiro e entregue
uma recomendação completa de redução de emissões de carbono.

════════════════════════════════════════
DADOS DA EMPRESA
════════════════════════════════════════
{bloco_empresa}

════════════════════════════════════════
EMISSÕES DIRETAS POR MÁQUINA (Escopo 1 — coletadas via sensor)
════════════════════════════════════════
{bloco_csv}
  Total direto: {total_direto_kg:.2f} kg CO₂/mês

════════════════════════════════════════
TOTAL GERAL DE EMISSÕES
════════════════════════════════════════
  Escopo 1 (direto):  {total_direto_kg:.2f} kg CO₂/mês
  Escopo 2 (elétrico): {total_indireto} kg CO₂/mês
  Total combinado:    {total_geral:.2f} kg CO₂/mês

════════════════════════════════════════
SUA ANÁLISE DEVE OBRIGATORIAMENTE CONTER:
════════════════════════════════════════

1. VIABILIDADE
   Diga claramente se a meta de redução declarada é viável dentro do prazo e orçamento informados.
   Use cálculos reais para justificar (quanto a meta representa em % do total emitido, quanto
   cada solução custaria aproximadamente, qual seria a redução esperada).

2. SOLUÇÃO RECOMENDADA
   Indique a melhor solução ou combinação de soluções para esta empresa específica.
   Justifique a escolha com base nos dados fornecidos e na realidade do mercado brasileiro.
   Se for uma combinação, explique a ordem de prioridade e por quê.

3. RESULTADO ESPERADO
   Estime a redução de emissões em kg CO₂/mês e em percentual que a solução deve entregar,
   e o retorno financeiro aproximado do investimento.

4. PONTOS DE AJUSTE (se necessário)
   Se a meta, o orçamento ou o prazo não forem suficientes para o ideal, diga o que precisaria
   ser diferente: quanto mais de capital, quantos anos a mais de prazo, ou qual meta seria
   realista com os recursos atuais.
"""

    print("Analisando dados com IA... aguarde.\n")

    try:
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user",   "content": prompt}
            ]
        )
        resultado = response.choices[0].message.content

    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        print("Verifique se a chave API está correta no arquivo funcoes.py.")
        return

    print("=" * 60)
    print("  ANÁLISE CARBOVIX — Recomendação personalizada")
    print("=" * 60)
    print(resultado)
    print("=" * 60)

    salvar = input("\nDeseja salvar a análise em arquivo .txt? (s/n): ").strip().lower()
    if salvar == "s":
        with open("data/analise_ia.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write("ANÁLISE CARBOVIX\n")
            arquivo.write("=" * 60 + "\n")
            arquivo.write(resultado)
        print("Análise salva em: data/analise_ia.txt")

    input("\nDigite Enter para voltar... ")
    os.system("cls")
