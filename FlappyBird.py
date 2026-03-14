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

    def desenhar(self):

        # def qual img do pássaro usar
        self.contagem_imagem +=1

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

        # desenhar a img

class Cano:
    pass

class Chao:
    pass