# Duck Runner

## Funcionalidades

- **Menu inicial** com opções para jogar, ligar / desligar musica de fundo e sair.
- **Jogabilidade**: O jogador pode correr para a esquerda e direita, pular.
- **Dificuldade** Dificuldade aumenta ao coletar 18 pontos.
- **Avião inimigo**: No inicio do jogo temos um avião que aparece e começa a disparar tiros para baixo.
- **Imunidade**: Após uma colisão com um obstáculo, o jogador fica temporariamente invencível.

## Requisitos
- Python 3.x
- Pygame Zero (pgzrun)
- 
Para instalar o Pygame Zero, use o seguinte comando:
```bash
pip install pgzero
```
## Como Jogar

- **Iniciar o Jogo**: Ao executar o arquivo `duckRunner.py`, o menu será exibido com as seguintes opções:
  - **Jogar**: Começa o jogo.
  - **Som ON/OFF**: Liga/desliga a música de fundo.
  - **Sair**: Fecha o jogo.

- **Controles**:
  - **Seta para cima**: Pular.
  - **Seta para esquerda/direita**: Ir para direita e esquerda.
  - **Espaço** ou **Enter**: Seleciona uma opção no menu.

- **Objetivo**: Chegar em 18 pontos e sobreviver o máximo possivel desviando de obstáculos, e coletar corações para ganhar vidas.

## Como Rodar o Jogo

1. Clone o repositório ou faça o download do código.
2. Navegue até o diretório.
3. Execute o jogo com o comando:

```bash
python duckRunner.py
