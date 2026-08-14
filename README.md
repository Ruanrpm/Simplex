# Simplex

## Sobre o projeto

Este projeto implementa o algoritmo Simplex para resolver problemas de programação linear em Python. Ele inclui suporte às etapas de Fase I e Fase II do método Simplex, detecta soluções inviáveis e trata problemas de maximização e minimização.

O código lê um problema de um arquivo de entrada, normaliza as restrições, monta as matrizes necessárias e executa o processo iterativo para encontrar a solução ótima.

## Tecnologias utilizadas

- Python 3
- Biblioteca padrão do Python (`re`)

## Arquitetura / Estrutura do projeto

O repositório está organizado da seguinte forma:

- `src/main.py`: script principal que controla a leitura do problema, inicializa o solver e imprime o resultado.
- `src/simplex/Simplex.py`: implementação do método Simplex com fase I e fase II.
- `src/functions/`: funções auxiliares de álgebra linear e parser de entrada.
  - `ler_arquivo.py`: lê e interpreta o problema a partir de um arquivo de texto.
  - `inversa.py`: calcula a inversa de matrizes com eliminação de Gauss-Jordan.
  - `laplace.py`: calcula determinantes por expansão de Laplace.
  - `mult_matrizes.py`, `mult_matriz_vetor.py`, `mult_vetor_matriz.py`, `transposta.py`: operações matriciais.

### Estrutura de diretórios simplificada

```text
Projeto Simplex/
├─ entrada.txt
├─ entradas_exercicios.txt
├─ README.md
└─ src/
   ├─ main.py
   ├─ functions/
   │  ├─ inversa.py
   │  ├─ laplace.py
   │  ├─ ler_arquivo.py
   │  ├─ mult_matriz_vetor.py
   │  ├─ mult_matrizes.py
   │  ├─ mult_vetor_matriz.py
   │  └─ transposta.py
   └─ simplex/
      └─ Simplex.py
```

## Funcionalidades

- Leitura de problema de programação linear a partir de arquivo de texto.
- Suporte a objetivos `max` e `min`.
- Normalização de restrições com `<=`, `>=` e `=`.
- Inserção automática de variáveis de folga e tratamento de variáveis artificiais para a Fase I.
- Cálculo da base inicial e atualização iterativa da solução.
- Detecção de problemas inviáveis e ilimitados.
- Impressão da solução final, valor de `z`, base final e matrizes/vetores utilizados.

## Pré-requisitos

- Python 3 instalado.

Nenhuma dependência externa é necessária além da biblioteca padrão do Python.

## Instalação

1. Clone o repositório.
2. Navegue até a pasta do projeto:

```bash
cd "Projeto Simplex"
```

3. Não há dependências adicionais a instalar.

## Configuração

O projeto não utiliza variáveis de ambiente externas, Docker ou serviços externos.

O arquivo de entrada padrão é `entrada.txt`, que deve estar no mesmo diretório em que o script principal é executado.

### Formato do arquivo de entrada

- Primeira linha: função objetivo, exemplo `max z = 3x1 + 3x2 + 13x3` ou `min z = - x1 - 2x2`.
- Linhas seguintes: restrições associadas ao problema.
- Restrições podem usar `<=`, `>=` ou `=`.
- Declarações de não negatividade podem ser escritas como `x1, x2, x3 >= 0`.

Exemplo disponível em `entrada.txt`.

## Execução

Execute o solver a partir da raiz do projeto:

```bash
python src/main.py
```

O script `main.py` lê `entrada.txt`, resolve o problema e imprime o resultado no terminal.


## Desenvolvimento

Para continuar desenvolvendo o projeto, os pontos principais são:

- adaptar o parser para suportar mais formatos de entrada;
- melhorar a estabilidade numérica das operações matriciais;
- adicionar testes automatizados de unidade;
- criar interface de entrada/saída mais amigável.

## Status do projeto

O projeto está em estado funcional como solver de Simplex baseado em arquivo de entrada. Não há testes automatizados e não há suporte a instalação via gerenciador de pacotes.

## Observações

- O projeto foi implementado como um utilitário de linha de comando em Python.
- A entrada e saída são tratadas localmente, sem integrações externas.

