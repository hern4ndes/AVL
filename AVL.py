# -*- coding: utf8 -*-

from Tkinter import *
import pygame
#import AVL

XDMI = 1000
YDMI = 720

White = (255, 255, 255)
Black = 0, 0, 0
Red = 255, 0, 0
Blue = 0, 0, 255
Green = 0, 0, 255
Cyan = 0,180,105

RAIZ = False
nodes = []
fatores = []
localizado = " "
removerOk = 0

window = Tk() # cria uma janela
window.title('AVL') # seta o titulo da janela
window.geometry('450x300') # seta o tamanho da janela
entry = Entry(window, width=25, justify='center') # cria uma entrada de texto
entry.insert(0, '') # seta o texto
entry.pack() # gerenciador de geometria
entry.focus_set() # obtm o foco para a entrada de texto

class Node:
    def __init__(self, chave):
        #Inicia a arvore colocando uma raiz ou apenas coloca um no
        self.chave = chave
        self.filhos(None, None)
        self.posicao = (None, None)
        self.nivel = None

    def filhos(self, esquerda, direita):
        #Configura os filhos de um no
        self.esquerda = esquerda
        self.direita = direita

    def FB(self):
        #Usa as alturas para calcular os fatores de balanceamento
        alturaE = 0
        if self.esquerda:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita:
            alturaD = self.direita.altura()
        return alturaD - alturaE

    def altura(self):
        #Calcula a altura dos lados da arvore (esquerdo ou direito)
        #Basicamente entra recursivamente arvore ate achar o fim. Sao duas variaveis sendo incrementadas.
        #Como o calculo da altura pode envolver lado oposto(no caso do esquerdo, se nao haver mais esquerdo, pode se procurar filho direito pra continuar calculando)
        #E no final eh retornado 1+ o que incrementou mais(que e o que realmente vale)
        alturaE = 0
        if self.esquerda:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita:
            alturaD = self.direita.altura()
        return 1 + max(alturaE, alturaD) #Retorna 1 + a mais incrementada

    def rot_E(self):
        #Realiza a operacao de rotacao simples a esquerda
        self.chave, self.direita.chave = self.direita.chave, self.chave #atribuicao multipla: atribui respectivamente
        old_esquerda = self.esquerda #passa o no a direita pra uma variavel auxiliar
        self.filhos(self.direita, self.direita.direita) #configura os filhos pro no
        self.esquerda.filhos(old_esquerda, self.esquerda.esquerda) #configura os filhos pro no

    def rot_D(self):
        #Realiza a operacao de rotacao simples a direita
        self.chave, self.esquerda.chave = self.esquerda.chave, self.chave #atribuicao multipla: atribui respectivamente
        old_direita = self.direita #passa o no a direita pra uma variavel auxiliar
        self.filhos(self.esquerda.esquerda, self.esquerda) #configura os filhos pro no
        self.direita.filhos(self.direita.direita, old_direita) #configura os filhos pro no

    def rot_dup_D(self):
        #Realiza a operacao de rotacao dupla a direita - reaproveita as funcoes anteriores
        self.esquerda.rot_E() #Chama uma rotacao a esquerda
        self.rot_D() #depois uma a direita (assim como eh feito manualmente)

    def rot_dup_E(self):
        #Realiza a operacao de rotacao dupla a esquerda - reaproveita as funcoes anteriores
        self.direita.rot_D() #Chama uma rotacao a direita
        self.rot_E() #depois uma a esquerda (assim como eh feito manualmente)

    def executaBalanco(self):
        #Executa o balanceamento de um no recem inserido. Usa os fatores de balanceamento, e as operacoes de rotacao
        bal = self.FB() #bal recebe o fator de balanceamento do no na qual vai sofrer balanceamento
        if bal > 1: #se for maior que um teremos uma operacao de rotacao (dupla) a esquerda
            if self.direita.FB() > 0: #se caso o FB do no ah direita for maior que 0, sera uma rotacao simples
                self.rot_E()
            else: #caso contrario, sera dupla
                self.rot_dup_E()
        elif bal < -1: #se caso for menor que -1 teremos uma operacao de rotacao (dupla) a direita
            if self.esquerda.FB() < 0: #se caso o FB do no ah esquerda for maior que 0, sera uma rotacao simples
                self.rot_D()
            else: #caso contrario, sera dupla
                self.rot_dup_D()

    def insere(self, chave):
        #Realiza a insercao de um no com chave. Usa o __init__ e a a propria funcao recursivamente
        if chave < self.chave: #Se a chave a ser inserida for menor que a chave atual, continua o algoritmo a esquerda ou insere a esquerda
            if not self.esquerda:
                self.esquerda = Node(chave)
            else:
                self.esquerda.insere(chave)
        elif chave > self.chave: #Se a chave inserida for maior ou igual que a chave atual, continua o algoritmo a direita ou insere a direita
            if not self.direita:
                self.direita = Node(chave)
            else:
                self.direita.insere(chave)
        self.executaBalanco() #Apos inserir executa o balanceamento do no inserido

    def localizar(self, chave, pai="-"):
        global localizado
        global removerOk
        localizado = "Não Localizado!"
        removerOk = 0
        if chave < self.chave: #se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave) #guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.localizar(chave, pai)
        elif chave > self.chave: #se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave) #guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.localizar(chave, pai)
        elif chave == self.chave: #Se chegar num caso de chave igual, eh porque encontramos. Assim printamos as informacoes
            filhoesq = "-"
            filhodir = "-"
            if self.esquerda is not None:
                filhoesq = str(self.esquerda.chave)
            if self.direita is not None:
                filhodir = str(self.direita.chave)
            localizado = ('Nó: ' + str(self.chave) + '\nPai: ' + str(pai) + '\nFilho da Esquerda: ' + str(filhoesq) + '\nFilho da Direita: ' + str(filhodir) + '\nFB: ' + str(self.FB()))
            removerOk = 1


    def remover(self, chave):
        global RAIZ
        #avalia o caso especial de remocao e depois manda pra remocao
        #o caso especial é quando temos apenas dois nos, e a raiz deve ser excluida
        if chave == self.chave:
            if self.esquerda is None and self.direita is not None:
                #se tiver apenas a raiz e um no na direita
                self.chave = self.direita.chave
                self.filhos = self.direita.filhos
                self.direita = self.direita.direita
            elif self.direita is None and self.esquerda is not None:
                #se tiver apenas a raiz e um no na esquerda
                self.chave = self.esquerda.chave
                self.filhos = self.esquerda.filhos
                self.esquerda = self.esquerda.esquerda
            elif self.direita is None and self.esquerda is None:
                #se tiver restando apenas a raiz, ele troca a raiz por uma mensagem de arvore vazia
                self.__init__('Vazio')
                RAIZ = False
            else:
                #se nao for nenhum dos casos acima, faz a remocao com os outros casos no outro metodo
                #nesse caso, se o no a ser removido for uma raiz mas nao dos casos espciais acima
                self.remocao(chave)
        else:
            #qualquer outro no ou caso de remocao
            self.remocao(chave)

    def remocao(self, chave):
        #remocao de no folha ou no com apenas um filho, recursivamente. usa os retornos a cada recursao pra percorrer e substituir o no apagado
        try:
            if chave < self.chave:
                self.esquerda = self.esquerda.remocao(chave)
            elif chave > self.chave:
                self.direita = self.direita.remocao(chave)
            else:
                if self.direita is None:
                    return self.esquerda
                if self.esquerda is None:
                    return self.direita
                #remocao de no com dois filhos. substitui o no removido pelo menor no da subarvore da direita. tem dois metodos auxiliarres
                #o metodo menor busca o menor no da subarvore da direita. o metodo deletamenor deleta esse no, pois ele ja foi substiuir o no removido
                aux = self.direita.menor()
                self.chave = aux.chave
                self.direita = self.direita.deletamenor()
            return self

        except(AttributeError):
            #Se o no nao for encontrado,
            erroRemocao = Tk()
            erroRemocao.title('AVL') # seta o titulo da janela
            erroRemocao.geometry('200x50') # seta o tamanho da janela
            confirmacao = Label(erroRemocao, text="Nó não encontrado!")
            confirmacao.pack()

    def menor(self):
        #busca o menor no da subarvore direita do no removido
        if self.esquerda is None:
            return self
        else:
            return self.esquerda.menor()

    def deletamenor(self):
        #exclui o menor no da subarvore da direita, pois esse no foi substituir o no removido
        if self.esquerda is None:
            return self.direita
        self.esquerda = self.esquerda.deletamenor()
        return self

    def rebalanceamento(self):
        #Apos uma remocao, este metodo busca nos com FBs maiores que um ou menores que -1 para realizar o balanceamento. Utiliza logica semelhante a da funcao
        #de rebalanceamento ao inserir um no
        if self.esquerda is not None:
            self.esquerda.rebalanceamento()
        bal = self.FB()#bal recebe o FB do no acessado atualmente
        if bal > 1:
            #FBs>1 fazem rotacoes a esquerda
            if self.direita.direita is not None:
                #se o no da direita da direita existir, entao sera uma rotacao simples a esquerda
                print 'Rebalanceamento: Rotacao a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_E()
            else:
                #caso nao, sera dupla a esquerda
                print 'Rebalanceamento: Rotacao dupla a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_dup_E()
        elif bal < -1:
            #FBs<-1 fazem rotacoes a direita
            if self.esquerda.esquerda is not None:
                #se o no da direita da direita existir, entao sera uma rotacao simples a direita
                print 'Rebalanceamento: Rotacao a direita em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_D()
            else:
                #caso nao, sera dupla a direita
                print '\nRebalanceamento: Rotacao dupla a direita em \n' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_dup_D()

        if self.direita is not None:
            self.direita.rebalanceamento()

    def imprimeArvore(self, indent = 0, count = 0, pai = 0):
        #Printa a arvore na ordem raiz -> filho dir - filho esq. Mostra o pai de cada no e seu respectivo fator de balanceamento
        count = count + 1
        if count is 1:
            #A identacao se da por uma multiplicacao de uma string com um espaco simples por uma variavel com um valor, recebida de uma execucao anterior
            print " "
            print " " * indent + str(self.chave) + '  (raiz FB: ' + str(self.FB()) + ')'
        else:
            print " " * indent + str(self.chave) + '  (pai: ' + str(pai) + ' FB: '+ str(self.FB()) + ')'
            pai = 0

        #navega recursivamente na arvore levando como paramentros instrucoes para a printagem
        if self.esquerda:
            self.esquerda.imprimeArvore(indent + 2, count + 2, pai + self.chave)
        if self.direita:
            self.direita.imprimeArvore(indent + 2, count + 2, pai + self.chave)


    def calculaNiveis(self, rootOk = 0, nivelRoot = 0):
        #calcula os niveis dos nos pra ajudar no calculo da posicao
        #coloca dentro de cada no o seu nivel (ou nivel aproximado em alguns casos), apenas para auxiliar na orientacao da apresentacao grafica da arvore
        #note que os niveis comecam com 1 e nao representam o conceito de niveis. Isso e apenas o nome do metodo, que apenas auxilia a interface grafica.
        rootOk = rootOk + 1
        if rootOk == 1:
            #a altura toda da arvore e o nivel dela
            nivelRoot = self.altura()
        else:
            self.nivel = nivelRoot - self.altura() + 1
        if self.esquerda:
            self.esquerda.calculaNiveis(rootOk + 2, nivelRoot = nivelRoot)
        if self.direita:
            self.direita.calculaNiveis(rootOk + 2, nivelRoot = nivelRoot)

    def calcposicao(self,  rootOk = 0, posPai = [0,0], lado = 0):
        rootOk = rootOk + 1
        node = ()
        if rootOk == 1:
            self.posicao = (XDMI,  100)
            node = (self.chave,self.posicao)
            nodes.append(node)
            fatores.append(self.FB())
        else:
            if lado == 1:
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = XDMI/aux
                self.posicao = [posPai[0] - deslocamento, posPai[1]+100]
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)
                fatores.append(self.FB())
            else:
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = XDMI/aux
                self.posicao = [posPai[0] + deslocamento, posPai[1]+100 ]
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)
                fatores.append(self.FB())

        if self.esquerda:
            self.esquerda.calcposicao(rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 1)
        if self.direita:
            self.direita.calcposicao (rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 2)
        #retorna o vetor de nos.


arvore = Node("Vazio")

def read():
    #Le os elementos do arquivo e os coloca em um vetor de inteiros
    arquivo = open("INPUT.TXT","r") #abre arquivo com nos
    nodes = arquivo.read().split(';') #vetor nodes recebe os elementos no formato string
    ultimo = float(nodes[-1])
    nodes[-1] = int(ultimo)
    nodes = [int(x) for x in nodes] #transformacao dos elementos do vetor de string em vetor de inteiros
    return nodes #retornando um vetor de inteiros

#funcao para o evento de clique do botao
def arq_button():
    global arvore
    global RAIZ
    nos = read()
    for no in nos:
        if RAIZ is False:
            arvore = Node(no)
            RAIZ = True
        else:
            arvore.insere(no)

def manual_button():
    global arvore
    global RAIZ
    if not entry.get(): #[] entrada vazia
        entry.insert(0, 'Digite o Nó')
    else:
        if RAIZ is False:
            global arvore
            arvore = Node(int(entry.get()))
        else:
            arvore.insere(int(entry.get()))
        RAIZ = True

def remover_button():
    global arvore
    if not entry.get(): #[] entrada vazia
        entry.insert(0, 'Digite o Nó')
    else:
        remover = int(entry.get())
        arvore.localizar(remover)
        if removerOk is 1:
            arvore.remover(int(entry.get()))
            arvore.rebalanceamento()
            encontrado = Tk()
            encontrado.title("Remoção")
            encontrado.geometry('300x50')
            resultado = Label(encontrado, text='Nó removido com sucesso.')
            resultado.pack()
        elif removerOk is 0:
            naoencontrado = Tk()
            naoencontrado.title("Remoção")
            naoencontrado.geometry('300x50')
            resultado = Label(naoencontrado, text='Nó não encontrado.')
            resultado.pack()

def localizar_button():
    global localizado
    if not entry.get(): #[] entrada vazia
        entry.insert(0, 'Digite o Nó')
    else:
        arvore.localizar(int(entry.get()))
        localizar = Tk()
        localizar.title("Localizar")
        localizar.geometry('300x50')
        resultado = Label(localizar, text=localizado);
        resultado.pack()

def identacao_button():
    arvore.imprimeArvore()

def natural_button():
    del nodes[:]
    del fatores[:]
    WindowSize = [XDMI, YDMI]
    arvore.calculaNiveis()
    arvore.calcposicao()
    pygame.init()
    pygame.display.set_caption('AVL: Notação Natural')
    screen = pygame.display.set_mode(WindowSize)
    font = pygame.font.SysFont("Arial", 13)
    screen.fill(White)
    for i in range(len(nodes)):
        pygame.draw.circle(screen,Blue , (nodes[i][1][0]/2,nodes[i][1][1]),20, 2)
        text = font.render(str(nodes[i][0]), True, Black)
        screen.blit(text,(nodes[i][1][0]/2-10,nodes[i][1][1]-10))
        text = font.render(str(fatores[i]), True, Black)
        screen.blit(text,(nodes[i][1][0]/2+25,nodes[i][1][1]-10))
        for i in range(1,len(nodes)):
            pygame.draw.aaline(screen, Cyan, (nodes[i][2][0]/2,nodes[i][2][1]+20),(nodes[i][1][0]/2,nodes[i][1][1]-20), 3)
    fpsClock = pygame.time.Clock()
    pygame.display.update()
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
    pygame.quit()

import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def limparConsole_button():
    cls()

btn_arq = Button(window, text='Inserir do Arquivo', width=20, command = arq_button)
btn_manual = Button(window, text='Inserir Nó Manualmente', width=20, command = manual_button)
btn_remover = Button(window, text='Remover Nó', width=20, command = remover_button)
btn_identacao = Button(window, text='Notação Indentada', width=20, command = identacao_button)
btn_localizar = Button(window, text ='Localizar Nó', width=20, command = localizar_button)
btn_natural = Button(window, text='Notação Natural', width=20, command = natural_button)
btn_limpConsole = Button(window, text='Limpar Console', width=20, command =limparConsole_button)

btn_arq.pack()
btn_manual.pack()
btn_remover.pack()
btn_localizar.pack()
btn_identacao.pack()
btn_natural.pack()
btn_limpConsole.pack()

window.mainloop()
