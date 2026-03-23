import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação / caindo em parábola
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 0
        self.angulo = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0  # qual img está usando no momento
        self.imagem = self.IMGS[0]

    #no pygame = eixo x cresce p/ direita e y p/ baixo, se direção contraria: valor negativo
    def pular(self):
        self.velocidade = -10.5 #pula pra cima no y
        self.tempo = 0
        self.altura = self.y

    def mover(self):

        # calcular o deslocamento (S=so+vot+at²/2)
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16: #pixels
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -=2 # ajuste p tornar o pulo menos "pesado" no topo

        self.y += deslocamento

        # angulo passaro
        # se o pássaro estiver subindo ou se ainda estiver acima do ponto inicial do pulo
        if deslocamento < 0 or self.y < (self.altura + 50):
            # garante que ele não incline mais do que a rotação máxima (25 graus)
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
            else:
                # se ele estiver caindo, rotaciona o bico para baixo até ficar vertical (-90 graus)
                if self.angulo > -90:
                    self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):

        # def qual img do pássaro usar
        self.contagem_imagem +=1

        # ciclo de animação: asa p cima, meio, para baixo, meio e repete
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # não bater asa enquanto cai
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            # garante que a próxima batida não seja imediata
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a img
        # rotacionar a imagem do pássaro
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        # define centro da img original p servir de eixo na rotação
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        # cria novo retângulo baseado na img rotacionada, mantendo o centro fixo
        retangulo = imagem_rotacionada.get.rect(center=pos_centro_imagem)
        # renderiza img final na tela usando a posição do topo-esquerdo do retângulo
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        # cria mask de colisão baseada nos px reais da img, detecta colisão apenas quando os px do bird encostam em algo
        pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200  # dist entre os canos
    VELOCIDADE = 5   # v movimento p esquerda

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0 # pos y cano superior
        self.pos_base = 0 # pos y cano inferior
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # gera altura random p o meio do vão entre canos
        self.altura = random.randrange(50, 450)
        # calc pos do cano de cima (altura do vão menos altura do próprio cano)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        # calc pos do cano de baixo (altura do vão mais a dist definida)
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        # Renderiza os canos (topo e base) na superfície de exibição
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        # cria as masks para os canos sup e infr com base nas imgs
        topo_mask = pygame.mask.from_surface(passaro.CANO_TOPO)
        base_mask = pygame.mask.from_surface(passaro.CANO_BASE)
        # calcula a dist (offset) entre o pássaro e o cano do topo e da base
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        # verif se existe ponto de sobreposição entre as masks
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # retorna Verdadeiro se houver colisão em qualquer um dos canos
        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        # inicia a img 1 na posição 0
        self.x1 = 0
        # inicia a img 2 logo após a 1 para criar continuidade
        self.x2 = self.LARGURA

    def mover(self):
        # move as duas partes do chão p/ a esq com base na velocidade
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # qnd a img 1 sai pela esq, a img 2 já se reposiciona atras dela e assim continua
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x1 + self.LARGURA
        if  self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

    def desenhar (self, tela):
        # renderiza as duas partes do chão simultaneamente para evitar espaços vazios
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    # desenha a img de fundo na posição inicial (0, 0)
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    # renderiza cada pássaro e cada cano das listas de ambos
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    # rend texto da pontuação na tela (cor branca, anti-aliasing ativado)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    # posiciona o texto no canto superior direito da tela
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    # desenha o chão (por cima dos canos para esconder a base deles)
    chao.desenhar(tela)
    # att a tela para exibir as mudanças deste frame
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]  # cria lista de pássaros (suporta múltiplos pássaros para IA no futuro)
    chao = Chao(730)     # instancia o objeto do chão na altura 730
    canos = [Cano(700)]  # cria lista de canos iniciando com o primeiro cano na posição 700
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))  # config a janela do jogo com as dimensões definidas
    pontos = 0  # inicializa o contador de pontos
    relogio = pygame.time.Clock()   # objeto de relógio para controlar a taxa de quadros (FPS)

    rodando = True
    while rodando:
        relogio.tick(30) # taxa de fps=30

        # percorre todos os eventos detectados pelo Pygame (teclado, mouse, etc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()





        desenhar_tela(tela, passaros, canos, chao, pontos)
