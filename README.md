# 🌿 Carbovix

Sistema de monitoramento e análise de emissões de carbono voltado para o setor industrial brasileiro. Desenvolvido como projeto acadêmico, o Carbovix combina coleta de dados em tempo real via Arduino, cálculo de emissões diretas e indiretas, e geração de recomendações personalizadas de redução de emissões utilizando inteligência artificial.

---

## 🎯 Contexto e objetivo

Sistemas de monitoramento de carbono já existem no mercado, mas em geral apenas monitoram — não orientam. O diferencial do Carbovix é cruzar os dados de emissão da empresa com sua capacidade de investimento e metas declaradas, entregando uma recomendação aplicável e personalizada, não genérica.

O sistema roda inteiramente no terminal e foi projetado para operar em ambiente industrial, com um sensor posicionado na chaminé principal da empresa.

---

## 📦 Dependências

```bash
pip install pyserial groq
```

| Biblioteca | Finalidade |
|---|---|
| `pyserial` | Comunicação serial com o Arduino via porta COM |
| `groq` | Acesso à API de IA (modelo LLaMA 3.3 70B) |

Bibliotecas padrão utilizadas: `os`, `csv`.

---

## ⚙️ Configuração

No código a chave API não foi disponibilizada por questões de segurança.
Para utilizar a função de sugestão com IA `analisar_ia()`, em `src/funcoes.py`, substitua o valor de `CHAVE_API` pela sua chave da API do Groq:

```python
CHAVE_API = "SUA_CHAVE_AQUI"
```

Chave gratuita disponível em: [console.groq.com](https://console.groq.com)

---

## 🗂️ Estrutura do projeto

```
sistema-carbovix/
├── main.py              # Ponto de entrada, loop principal do menu
├── data/
│   ├── dados.txt        # Dados cadastrados da empresa (sobrescrito a cada cadastro)
│   ├── emissoes.csv     # Última leitura de emissão coletada pelo Arduino
│   └── analise_ia.txt   # Última análise gerada pela IA (opcional, salvo pelo usuário)
└── src/
    ├── funcoes.py       # Toda a lógica do sistema
    └── menus.py         # Strings dos menus exibidos no terminal
```

---

## 🚀 Execução

```bash
python main.py
```

---

## 🖥️ Funcionalidades

### `[1]` Cadastrar dados da empresa
Coleta via terminal os dados necessários para a análise:
- Consumo mensal de energia elétrica (kWh)
- Capital disponível para investimento (R$)
- Prazo desejado de retorno do investimento (anos)
- Meta de redução de emissões (kg CO₂)

Já calcula e salva automaticamente a **emissão indireta** (Escopo 2) com base no consumo elétrico informado. Sobrescreve o arquivo `dados.txt` a cada execução — o sistema sempre trabalha com os dados mais recentes.

### `[2]` Consultar dados
Exibe no terminal todos os dados cadastrados da empresa, lidos diretamente do `dados.txt`.

### `[3]` Atualizar dado
Permite alterar um campo específico sem precisar recadastrar tudo. Ao atualizar o consumo elétrico, a emissão indireta é recalculada automaticamente.

### `[4]` Deletar dado
Remove um campo específico do cadastro da empresa.

### `[5]` Coletar leitura do Arduino
Conecta ao Arduino via porta COM (configurável), coleta leituras de PPM durante um período definido pelo usuário e salva a **projeção mensal de emissões** no `emissoes.csv`. Sobrescreve a leitura anterior a cada execução — garante que a IA sempre trabalhe com o dado mais atual.

### `[6]` Análise IA
Lê todos os dados disponíveis (`dados.txt` + `emissoes.csv`), monta um prompt estruturado e envia para o modelo LLaMA 3.3 70B via API do Groq. A resposta inclui:
- Diagnóstico de viabilidade da meta declarada
- Solução ou combinação de soluções recomendadas
- Estimativa de redução em kg CO₂/mês e percentual
- Pontos de ajuste caso os recursos sejam insuficientes para o ideal

O resultado pode ser salvo em `data/analise_ia.txt`.

---

## 🔬 Metodologia de cálculo de emissões

O sistema segue a estrutura do **GHG Protocol**, padrão internacional para inventários de emissões:

### Escopo 1 — Emissões diretas (Arduino)

O sensor coleta leituras em PPM a cada segundo. O sistema calcula a média do período coletado e projeta para o mês com a seguinte fórmula:

```
kg CO₂/mês = média_ppm × (10.000 ÷ 3.600) × 1,96 × 10⁻⁶ × 86.400 × 30
```

Onde:
- `10.000 m³/h` → vazão de referência assumida para uma chaminé industrial de médio porte
- `÷ 3.600` → converte vazão de m³/h para m³/s, compatível com a leitura por segundo do Arduino
- `1,96 kg/m³` → densidade do CO₂ (constante física)
- `× 86.400 × 30` → projeção de segundos para um mês completo

> A vazão foi fixada como referência pois o protótipo utiliza o sensor MQ-135, que não permite medição de vazão. Em uma implantação real, a vazão seria medida por um anemômetro acoplado à chaminé.

### Escopo 2 — Emissões indiretas (energia elétrica)

```
kg CO₂/mês = kWh/mês × 0,1
```

Fator de emissão de 0,1 kg CO₂/kWh baseado na média da rede elétrica brasileira, conforme dados do Ministério de Minas e Energia (MME/PNMC).

---

## 🛠️ Hardware — Sensor MQ-135

O protótipo utiliza o sensor **MQ-135** conectado a um Arduino Uno para simular a coleta de dados de uma chaminé industrial.

**Decisão de projeto:** o MQ-135 é um sensor de qualidade do ar que detecta múltiplos gases (CO₂, amônia, benzeno, fumaça) e retorna um valor analógico em PPM sem isolar o CO₂ especificamente. Ele foi escolhido por disponibilidade e custo (protótipo acadêmico), sendo utilizado como **simulação didática** do conceito.

Em um sistema real de produção, o sensor seria substituído por um modelo **NDIR (Non-Dispersive Infrared)**, como o **MH-Z19B** ou **SCD30**, que medem CO₂ de forma isolada e precisa, permitindo a aplicação direta da fórmula de conversão sem aproximações.

O código Arduino envia os dados pela serial no formato `PPM: 415.23` a cada segundo. A função `coletar_arduino()` filtra apenas as linhas que começam com `"PPM:"`, ignorando mensagens de status como `"Sis_iniciado!"` e `"ALERTA! GAS ALTO!"`.

---

## 🤖 Escolha da IA — Groq + LLaMA 3.3 70B

A análise de emissões envolve variáveis heterogêneas (financeiras, técnicas, ambientais e de mercado) que não se prestam a um algoritmo determinístico simples. O uso de um LLM permite cruzar todas essas variáveis e gerar recomendações contextualizadas.

**Por que Groq:** oferece free tier generoso (~500.000 tokens/dia, ~1.000 requisições/dia) sem necessidade de cartão de crédito, suficiente para uso acadêmico e demonstrações.

**Por que LLaMA 3.3 70B:** modelo open source de alta capacidade, com bom desempenho em análises técnicas em português. É o modelo de maior qualidade disponível no free tier do Groq.

A IA recebe um **system prompt** com referências reais do mercado brasileiro (custos de cada tecnologia, fontes de dados como IEA, IEDI e CNI) para embasar as recomendações com dados concretos, não apenas conhecimento genérico do modelo.

---

## 📌 Decisões de projeto resumidas

| Decisão | Motivo |
|---|---|
| Dados salvos em `.txt` e `.csv` simples | Sem dependência de banco de dados, fácil portabilidade e leitura |
| Sobrescrita a cada nova coleta | Evita acúmulo de registros desatualizados e garante que a IA use sempre o dado mais recente |
| Vazão fixa de 10.000 m³/h | Referência de chaminé industrial de médio porte; documentada para transparência na apresentação |
| Free tier Groq | Viabilidade acadêmica sem custo, com limites suficientes para o protótipo |
| MQ-135 como simulação | Disponibilidade de hardware; limitação explicitamente documentada |