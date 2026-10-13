# Projeto de Análise de Dados em Atendimento Pré-Hospitalar (APH)

> Projeto acadêmico da pós-graduação em Engenharia de Dados — Atividade Prática 1.

## Sobre o projeto

O projeto tem como objetivo estruturar, limpar e analisar dados de atendimentos de Atendimento Pré-Hospitalar (APH), aplicando fundamentos de Engenharia de Dados, Python, modelagem relacional e estatística.

Esta primeira etapa concentra-se em preparar uma base analítica confiável e documentar os procedimentos de tratamento e análise. Em etapas futuras, essa base poderá apoiar a investigação de associações entre características registradas do atendimento e desfechos observados, como preparação para estudar modelos probabilísticos.

**Importante:** os dados disponibilizados para desenvolvimento são sintéticos e destinados exclusivamente a estudo. As categorias de desfecho são ilustrativas; não representam diagnósticos reais, não foram validadas clinicamente e não devem ser usadas para orientar atendimento ou decisões de saúde.

## Objetivos da Atividade Prática 1

O trabalho está organizado para atender aos três eixos obrigatórios do manual acadêmico:

1. **Análise exploratória e tratamento em Python:** inspecionar a estrutura da base, verificar tipos, identificar dados ausentes e duplicados, validar domínios e tratar erros/exceções.
2. **Modelagem de dados:** documentar os modelos conceitual e lógico de Entidade-Relacionamento e implementar tabelas relacionais com scripts DDL e carga inicial DML.
3. **Diagnóstico estatístico:** calcular medidas de posição e variabilidade e aplicar testes de hipótese adequados à amostra, documentando resultados e limitações.

## Tecnologias

- Python 3
- Pandas
- NumPy
- SciPy
- SQLite
- Git e GitHub

## Dados utilizados

O arquivo principal é `atendimentos_aph.csv`. A estrutura prevista contém as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `id_atendimento` | Identificador técnico do atendimento |
| `id_paciente` | Identificador fictício do paciente |
| `idade` | Idade registrada no atendimento |
| `hipertensao` | Indicador de histórico de hipertensão |
| `diabetes` | Indicador de histórico de diabetes |
| `tabagismo` | Indicador de tabagismo |
| `sedentarismo` | Indicador de sedentarismo |
| `obesidade` | Indicador de obesidade |
| `doenca_cardiaca` | Indicador de histórico de doença cardíaca |
| `motivo_chamado` | Motivo informado para o chamado |
| `chamados_anteriores` | Quantidade de chamados anteriores registrada |
| `desfecho_registrado` | Categoria ilustrativa do desfecho registrado |

Os indicadores binários seguem o domínio esperado `0` (não) e `1` (sim). Um valor ausente deve ser tratado como desconhecido, e não convertido automaticamente em `0`.

## Estrutura atual do projeto

```text
pro_pos/
├── atendimentos_aph.csv              # dados sintéticos brutos
├── atendimentos_aph_tratados.csv     # saída do tratamento em Python
├── import_dados.py                   # carregamento e inspeção da base
├── tratamento.py                     # limpeza e validação dos dados
├── medidas.py                        # estatística descritiva e teste de hipótese
├── cco.db                            # banco SQLite local (esquema a validar)
├── projeto_um_pos_graduação.odt       # documento de trabalho acadêmico
├── .gitignore
└── README.md
```

A estrutura pode evoluir conforme forem adicionados os diagramas e scripts SQL. Os ambientes virtuais (`venv/`, `meuvenv/` ou `.venv/`) e os arquivos temporários do Python não devem ser versionados.

## Configuração do ambiente

No Linux, abra um terminal na pasta do projeto:

```bash
cd ~/Área\ de\ trabalho/pro_pos
```

Crie e ative um ambiente virtual (use apenas um ambiente para este projeto):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install pandas numpy scipy
```

Para registrar as dependências do ambiente:

```bash
python -m pip freeze > requirements.txt
```

## Execução dos scripts

Execute os scripts a partir da pasta do projeto:

```bash
python import_dados.py
python tratamento.py
python medidas.py
```

O script de importação permite inspecionar as primeiras linhas, as dimensões, as colunas e os tipos dos dados. O tratamento deve produzir uma versão tratada da base, e o script estatístico calcula medidas descritivas e executa a análise de hipótese definida para o projeto.

> Os scripts estão em desenvolvimento. Antes de considerar os resultados finais, confirme que o CSV de saída foi gerado corretamente, que as regras de qualidade foram aplicadas na ordem adequada e que as suposições do teste estatístico foram verificadas.

## Plano de tratamento e qualidade de dados

O processo de limpeza deve incluir, no mínimo:

- conversão explícita de tipos numéricos;
- padronização das categorias textuais;
- identificação de valores ausentes;
- validação de idades e quantidades de chamados;
- validação das colunas binárias;
- detecção de duplicidades por `id_atendimento`;
- tratamento de falhas de leitura do CSV;
- comparação da quantidade de registros antes e depois do tratamento.

Valores inválidos devem ser identificados antes de calcular estatísticas de preenchimento, como a mediana da idade. Não se deve imputar automaticamente um histórico de saúde ausente como ausência da condição.

## Modelagem relacional — a concluir nesta etapa

A modelagem deverá documentar entidades, atributos, chaves primárias, chaves estrangeiras e cardinalidades. A definição final será refletida em scripts SQL, por exemplo:

```text
sql/
├── 01_ddl.sql    # criação das tabelas e restrições
├── 02_dml.sql    # carga inicial de dados sintéticos
└── 03_consultas.sql  # consultas de validação e análise
```

O banco utilizado no projeto é SQLite. A estrutura existente em `cco.db` deverá ser inspecionada antes de decidir se será mantida ou recriada, e a carga inicial deverá respeitar a ordem das chaves estrangeiras.

## Diagnóstico estatístico

A análise descritiva deverá apresentar, para variáveis numéricas adequadas:

- **posição:** média, mediana, moda, quartis e percentis;
- **variabilidade:** amplitude, variância, desvio padrão e intervalo interquartil;
- **frequências:** distribuição de motivos de chamado e desfechos registrados.

O teste Qui-quadrado de independência poderá ser usado para investigar associação entre `motivo_chamado` e `desfecho_registrado`, desde que os dados e as frequências esperadas atendam às condições do teste. O relatório deve informar as hipóteses nula e alternativa, o nível de significância, a estatística, os graus de liberdade, o p-valor e uma interpretação cuidadosa.

A análise é exploratória: associação estatística não demonstra causalidade. Além disso, atendimentos repetidos do mesmo paciente podem afetar a suposição de independência das observações.

## Proteção de dados

Não utilizar nomes, CPF, telefones, endereços ou prontuários de pacientes neste repositório. Dados reais de saúde somente poderão ser usados com as autorizações e salvaguardas éticas e legais aplicáveis. Para o desenvolvimento público deste projeto, utilize exclusivamente dados sintéticos ou adequadamente autorizados e anonimizados.

## Checklist da Atividade Prática 1

- [x] Criar uma base sintética para desenvolvimento.
- [x] Iniciar o repositório Git e registrar a estrutura inicial.
- [x] Criar scripts iniciais de importação, tratamento e análise estatística.
- [ ] Revisar e validar o tratamento de tipos, nulos, duplicidades e exceções.
- [ ] Registrar métricas de qualidade antes e depois da limpeza.
- [ ] Documentar o modelo conceitual de Entidade-Relacionamento.
- [ ] Documentar o modelo lógico.
- [ ] Finalizar os scripts DDL e DML.
- [ ] Executar e interpretar as medidas estatísticas.
- [ ] Validar as condições e interpretar o teste de hipótese.
- [ ] Incorporar métodos, resultados, limitações e conclusão ao relatório acadêmico.

## Repositório

Código-fonte: [github.com/calreis/projeto-analise-risco-aph](https://github.com/calreis/projeto-analise-risco-aph)

---

**Status:** em desenvolvimento — Atividade Prática 1 da pós-graduação em Engenharia de Dados.
