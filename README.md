# Atividade Prática - Gestão Operacional de Exames Laboratoriais (DSM6)

Repositório estruturado para a resolução da atividade prática de mineração de dados em Python puro (utilizando exclusivamente a biblioteca padrão), focada em análise operacional, tratamento de dados e métricas de classificação.

## 📁 Arquivos do Projeto

- **`Pratica_DSM6_Exames_Laboratoriais.csv`**: Base de dados fornecida contendo os registros operacionais fictícios dos exames laboratoriais.
- **`main.py`**: Script principal contendo a leitura, limpeza, tratamento de valores ausentes, deduplicação e a geração dos relatórios (R01 a R15).
- **`saida_relatorios.txt`** *(Opcional)*: Arquivo contendo a saída de execução com os resultados de todos os relatórios formatados.

## 🚀 Como Executar

Certifique-se de ter o **Python 3** instalado em sua máquina. 

No seu terminal, na pasta do projeto, execute o script:

    python main.py

## 🛠️ Tecnologias Utilizadas
- Python 3 (Linguagem base)
- Módulo csv (Leitura e manipulação do arquivo CSV)
- Módulo collections (Counter, defaultdict para agregações eficientes)
- Módulo statistics (Cálculo de médias e medianas)