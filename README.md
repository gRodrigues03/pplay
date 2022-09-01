# pplay
Framework para criação de jogos em Python utilizado pelos alunos de Ciência da Computação da Universidade Federal Fluminense.

Vesão customizada com adições e mudanças feitas para ampliar a praticidade e utilidade do PPlay.
Modificada por um aluno da Turma de Laboratório de Programação de Jogos de 2022.1 na UFF.

Adições:
Janela de tamanho variável e modo tela cheia, ambos com aspect ratio e resolução fixos e com a posição do mouse corrigida
Câmera incompleta
Controle de opacidade
Inversão de imagem na horizontal e na vertical (adaptado também para animações)
Modos de mistura (blending modes)

Mudanças:
A criação de gameobjects aceita posição (x, y), largura e altura para facilitar a utilização (pra quem usa, claro)
Agora é possível criar uma gameimage à partir de outra gameimage, sem que seja necessário carregar a imagem novamente.
Antes, toda vez que uma gameimage, sprite ou animação eram criados, era necessário que a imagem fosse carregada novamente, mas agora é possivel usar o load_image para carregar uma imagem para uma variável ou usar o atributo da classe gameimage, image. Tudo dito sobre carregamento de imagens se aplica à todas as classes que usam imagens (duh)
Agora em vez de importar cada módulo por vez, pode se utilizar somente um comando de import: from PPlay import *
A classe de animação é a única que causa problemas, um deles foi resolvido, o tempo de animação.
Antes, o tempo de animação era calculado e registrado com .append, salvando depois do final da lista do tempo já definido da criação do objeto. Sendo assim, a velocidade era inalterável. Sem contar que as vezes a lista saía com o tamanho errado, dando erro logo de cara.
Agora a lista é recriada toda vez que o set_sequence_time é chamado. Do tamanho certo e com uma velocidade consistente, alterável sem que seja necessário criar o objeto novamente.

Pendências:
Som estéreo
Collided perfect para Animation
Animation baseada numa sequência de imagens
Aspect ratio variável usando a câmera para re-centralizar a tela depois de mudar o aspect ratio
(Sem isso, a tela original permaneceria no canto superior esquerdo e somente os lados direto e inferior seriam expandidos.)
Finalizar a câmera

Mais informações e documentação detalhada no site do projeto:
http://www2.ic.uff.br/pplay/
