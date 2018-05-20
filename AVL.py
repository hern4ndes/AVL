# -*- coding: utf8 -*-

from Tkinter import *
import pygame


# import AVL

XDMI = 1000
YDMI = 720

White = (255, 255, 255)
Black = 0, 0, 0
Red = 255, 0, 0
Blue = 0, 0, 255
Green = 0, 0, 255
Cyan = 0, 180, 105

RAIZ = False
nodes = []
fatores = []
localizado = " "
localizarOk = 0

window = Tk()  # cria uma janela
window.title('AVL')  # seta o titulo da janela
window.geometry('300x300')  # seta o tamanho da janela


class Node:
    def __init__(self, chave, palavras):
        # Inicia a arvore colocando uma raiz ou apenas coloca um no
        self.chave = chave
        self.palavras = palavras
        self.filhos(None, None)
        self.posicao = (None, None)
        self.nivel = None

    def filhos(self, esquerda, direita):
        # Configura os filhos de um no
        self.esquerda = esquerda
        self.direita = direita

    def FB(self):
        # Usa as alturas para calcular os fatores de balanceamento
        alturaE = 0
        if self.esquerda:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita:
            alturaD = self.direita.altura()
        return alturaD - alturaE

    def altura(self):
        # Calcula a altura dos lados da arvore (esquerdo ou direito)
        # Basicamente entra recursivamente arvore ate achar o fim. Sao duas variaveis sendo incrementadas.
        # O calculo da altura pode envolver o lado oposto(no caso do esquerdo, se nao haver mais esquerdo, pode se procurar filho direito pra continuar calculando)
        # E no final eh retornado 1+ o que incrementou mais(que e o que realmente vale)
        alturaE = 0
        if self.esquerda:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita:
            alturaD = self.direita.altura()
        return 1 + max(alturaE, alturaD)  # Retorna 1 + a mais incrementada

    def rot_E(self):
        # Realiza a operacao de rotacao simples a esquerda
        #oldpalavras = self.palavras
        #olddireitapalavras = self.direita.palavras
        self.chave, self.direita.chave  = self.direita.chave, self.chave  # atribuicao multipla: atribui respectivamente
        old_esquerda = self.esquerda  # passa o no a direita pra uma variavel auxiliar
        self.filhos(self.direita, self.direita.direita)  # configura os filhos pro no
        self.esquerda.filhos(old_esquerda, self.esquerda.esquerda)  # configura os filhos pro no
        #self.palavras = olddireitapalavras
        #self.direita.palavras = oldpalavras

    def rot_D(self):
        #oldpalavras = self.palavras
        #oldesquerdapalavras = self.esquerda.palavras
        # Realiza a operacao de rotacao simples a direita
        self.chave, self.esquerda.chave,  = self.esquerda.chave, self.chave  # atribuicao multipla: atribui respectivamente
        old_direita = self.direita  # passa o no a direita pra uma variavel auxiliar
        self.filhos(self.esquerda.esquerda, self.esquerda)  # configura os filhos pro no
        self.direita.filhos(self.direita.direita, old_direita)  # configura os filhos pro no
        #self.palavras = oldesquerdapalavras
        #self.esquerda.palavras = oldpalavras
     
       
    def rot_dup_D(self):
        # Realiza a operacao de rotacao dupla a direita - reaproveita as funcoes anteriores
        self.esquerda.rot_E()  # Chama uma rotacao a esquerda
        self.rot_D()  # depois uma a direita (assim como eh feito manualmente)

    def rot_dup_E(self):
        # Realiza a operacao de rotacao dupla a esquerda - reaproveita as funcoes anteriores
        self.direita.rot_D()  # Chama uma rotacao a direita
        self.rot_E()  # depois uma a esquerda (assim como eh feito manualmente)

    def executaBalanco(self):
    
        # Executa o balanceamento de um no recem inserido. Usa os fatores de balanceamento, e as operacoes de rotacao
        bal = self.FB()  # bal recebe o fator de balanceamento do no na qual vai sofrer balanceamento
        if bal > 1:  # se for maior que um teremos uma operacao de rotacao (dupla) a esquerda
            if self.direita.FB() > 0:  # se caso o FB do no ah direita for maior que 0, sera uma rotacao simples
                self.rot_E()
            else:  # caso contrario, sera dupla
                self.rot_dup_E()
        elif bal < -1:  # se caso for menor que -1 teremos uma operacao de rotacao (dupla) a direita
            if self.esquerda.FB() < 0:  # se caso o FB do no ah esquerda for maior que 0, sera uma rotacao simples
                self.rot_D()
            else:  # caso contrario, sera dupla
                self.rot_dup_D()

    def insere(self, chave, palavras):
        # Realiza a insercao de um no com chave. Usa o __init__ e a a propria funcao recursivamente
        if chave < self.chave:  # Se a chave a ser inserida for menor que a chave atual, continua o algoritmo a esquerda ou insere a esquerda
            if not self.esquerda:
                self.esquerda = Node(chave, palavras)
            else:
                self.esquerda.insere(chave, palavras)
        elif chave > self.chave:  # Se a chave inserida for maior ou igual que a chave atual, continua o algoritmo a direita ou insere a direita
            if not self.direita:
                self.direita = Node(chave, palavras)
            else:
                self.direita.insere(chave, palavras)
        self.executaBalanco()  # Apos inserir executa o balanceamento do no inserido

    def localizar(self, chave, pai="-"):
        global localizado
        localizarOk = 0
        if chave < self.chave:  # se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.localizar(chave, pai)
        elif chave > self.chave:  # se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.localizar(chave, pai)
        elif chave == self.chave:  # No caso de chave igual, encontramos o elemento procurado. Assim printamos as informacoes
            filhoesq = "-"
            filhodir = "-"
            if self.esquerda is not None:
                filhoesq = str(self.esquerda.chave)
            if self.direita is not None:
                filhodir = str(self.direita.chave)
            localizado = ('No: ' + str(self.chave) + ' Filho da Esquerda: ' + str(
                filhoesq) + '  Filho da Direita: ' + str(filhodir)  + ";Dados:" +str(self.palavras))
            print localizado
            localizarOk = 1
        if localizarOk != 1:
            print("No nao localizado")
        return localizarOk

    def localizarindice(self, chave, indice, pai="-"):
        global localizado
        if chave < self.chave:  # se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.localizarindice(chave,indice, pai)
        elif chave > self.chave:  # se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.localizarindice(chave,indice, pai)
        elif chave == self.chave:  # No caso de chave igual, encontramos o elemento procurado. Assim printamos as informacoes
            filhoesq = "-"
            filhodir = "-"
            if self.esquerda is not None:
                filhoesq = str(self.esquerda.chave)
            if self.direita is not None:
                filhodir = str(self.direita.chave)
            
            #localizado = ('No: ' + str(self.chave) + ' Filho da Esquerda: ' + str(filhoesq) + '  Filho da Direita: ' + str(filhodir)  + ";Dados:" +str(self.palavras))
            for i in self.palavras:
                if i is self.palavras[indice]:
                    print i 
             
    

    def remover(self, chave):
        global RAIZ
        # avalia o caso especial de remocao e depois manda pra remocao
        # o caso especial é quando temos apenas dois nos, e a raiz deve ser excluida
        if chave == self.chave:
            if self.esquerda is None and self.direita is not None:
                # se tiver apenas a raiz e um no na direita
                self.chave = self.direita.chave
                self.filhos = self.direita.filhos
                self.direita = self.direita.direita
            elif self.direita is None and self.esquerda is not None:
                # se tiver apenas a raiz e um no na esquerda
                self.chave = self.esquerda.chave
                self.filhos = self.esquerda.filhos
                self.esquerda = self.esquerda.esquerda
            elif self.direita is None and self.esquerda is None:
                # se tiver restando apenas a raiz, ele troca a raiz por uma mensagem de arvore vazia
                self.__init__('Vazio')
                RAIZ = False
            else:
                # se nao for nenhum dos casos acima, faz a remocao com os outros casos no outro metodo
                # nesse caso, se o no a ser removido for uma raiz mas nao dos casos espciais acima
                self.remocao(chave)
        else:
            # qualquer outro no ou caso de remocao
            self.remocao(chave)

    def remocao(self, chave):
        # remocao de no folha ou no com apenas um filho, recursivamente. usa os retornos a cada recursao pra percorrer e substituir o no apagado
        if chave < self.chave:
            self.esquerda = self.esquerda.remocao(chave)
        elif chave > self.chave:
            self.direita = self.direita.remocao(chave)
        else:
            if self.direita is None:
                return self.esquerda
            if self.esquerda is None:
                return self.direita
            # remocao de no com dois filhos. substitui o no removido pelo menor no da subarvore da direita. tem dois metodos auxiliarres
            # o metodo menor busca o menor no da subarvore da direita. o metodo deletamenor deleta esse no, pois ele ja foi substiuir o no removido
            aux = self.direita.menor()
            self.chave = aux.chave
            self.direita = self.direita.deletamenor()
        return self

    def menor(self):
        # busca o menor no da subarvore direita do no removido
        if self.esquerda is None:
            return self
        else:
            return self.esquerda.menor()

    def deletamenor(self):
        # exclui o menor no da subarvore da direita, pois esse no foi substituir o no removido
        if self.esquerda is None:
            return self.direita
        self.esquerda = self.esquerda.deletamenor()
        return self

    def rebalanceamento(self):
        # Apos uma remocao, este metodo busca nos com FBs maiores que um ou menores que -1 para realizar o balanceamento. Utiliza logica semelhante a da funcao
        # de rebalanceamento ao inserir um no
        if self.esquerda is not None:
            self.esquerda.rebalanceamento()
        bal = self.FB()  # bal recebe o FB do no acessado atualmente
        if bal > 1:
            # FBs>1 fazem rotacoes a esquerda
            if self.direita.direita is not None:
                # se o no da direita da direita existir, entao sera uma rotacao simples a esquerda
                print 'Rebalanceamento: Rotacao a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_E()
            else:
                # caso nao, sera dupla a esquerda
                print 'Rebalanceamento: Rotacao dupla a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(
                    self.FB())
                self.rot_dup_E()
        elif bal < -1:
            # FBs<-1 fazem rotacoes a direita
            if self.esquerda.esquerda is not None:
                # se o no da direita da direita existir, entao sera uma rotacao simples a direita
                print 'Rebalanceamento: Rotacao a direita em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_D()
            else:
                # caso nao, sera dupla a direita
                print '\nRebalanceamento: Rotacao dupla a direita em \n' + str(self.chave) + ' que tinha o FB ' + str(
                    self.FB())
                self.rot_dup_D()

        if self.direita is not None:
            self.direita.rebalanceamento()

    def imprimeArvore(self, indent=0, count=0, pai=0):
        # Printa a arvore na ordem raiz -> filho dir - filho esq. Mostra o pai de cada no e seu respectivo fator de balanceamento
        count = count + 1
        if count is 1:
            # A identacao se da por uma multiplicacao de uma string com um espaco simples por uma variavel com um valor, recebida de uma execucao anterior
            print " "
            print " " * indent + str(self.chave) + '  (Raiz FB: ' + str(self.FB()) + ')'
            print " " * indent,
            print  self.palavras

        else:
            print " " * indent + str(self.chave) + '  (pai: ' + str(pai) + ' FB: ' + str(self.FB()) + ')'
            print " " * indent,
            print self.palavras
            pai = 0

        # navega recursivamente na arvore levando como paramentros instrucoes para a printagem
        if self.esquerda:
            self.esquerda.imprimeArvore(indent + 2, count + 2, pai + self.chave)
        if self.direita:
            self.direita.imprimeArvore(indent + 2, count + 2, pai + self.chave)

    def calculaNiveis(self, rootOk=0, nivelRoot=0):
        # calcula os niveis dos nos pra ajudar no calculo da posicao
        # coloca dentro de cada no o seu nivel (ou nivel aproximado em alguns casos), apenas para auxiliar na orientacao da apresentacao grafica da arvore
        # note que os niveis comecam com 1 e nao representam o conceito de niveis. Isso e apenas o nome do metodo, que apenas auxilia a interface grafica.
        rootOk = rootOk + 1
        if rootOk == 1:
            # a altura toda da arvore e o nivel dela
            nivelRoot = self.altura()
        else:
            self.nivel = nivelRoot - self.altura() + 1
        if self.esquerda:
            self.esquerda.calculaNiveis(rootOk + 2, nivelRoot=nivelRoot)
        if self.direita:
            self.direita.calculaNiveis(rootOk + 2, nivelRoot=nivelRoot)

    def calcposicao(self, rootOk=0, posPai=[0, 0], lado=0):
        rootOk = rootOk + 1
        node = ()
        if rootOk == 1:
            self.posicao = (XDMI, 100)
            node = (self.chave, self.posicao)
            nodes.append(node)
            fatores.append(self.FB())
        else:
            if lado == 1:
                aux = 2 ** self.nivel
                aux = aux / 2
                deslocamento = XDMI / aux
                self.posicao = [posPai[0] - deslocamento, posPai[1] + 100]
                node = (self.chave, self.posicao, posPai)
                nodes.append(node)
                fatores.append(self.FB())
            else:
                aux = 2 ** self.nivel
                aux = aux / 2
                deslocamento = XDMI / aux
                self.posicao = [posPai[0] + deslocamento, posPai[1] + 100]
                node = (self.chave, self.posicao, posPai)
                nodes.append(node)
                fatores.append(self.FB())

        if self.esquerda:
            self.esquerda.calcposicao(rootOk + 2, posPai=[self.posicao[0], self.posicao[1]], lado=1)
        if self.direita:
            self.direita.calcposicao(rootOk + 2, posPai=[self.posicao[0], self.posicao[1]], lado=2)
        # retorna o vetor de nos.


arvore = Node("Vazio", " ")


def read():
    nodes = []

    arquivo = open("INPUT.TXT", "r")  # abre arquivo com nos
    TepNodes = arquivo.read()  # vetor nodes recebe os elementos no formato string
    TepNodes = TepNodes.strip('Dict_AVL = ').strip('{').strip('}').split('], ')

    for i in range(len(TepNodes)):  # i =  numero de linhas
        TepNodes[i] = TepNodes[i].strip(']').split(':[')

        for j in range(len(TepNodes[i])):  # numero de listas por linha
            node = []
            TepNodes[i][j] = TepNodes[i][j].strip(',').split(',')

        node.append(int(TepNodes[i][0][0][1:(len(TepNodes))]))

        for k in range(len(TepNodes[i][1])):  # numero de palavras na segunda lista
            TepNodes[i][1][k] = TepNodes[i][1][k].strip(' ')
            node.append(str((TepNodes[i][1][k][1:(len(TepNodes[i][1][k]) - 1)])))

        nodes.append(node)

    return nodes


# funcao para o evento de clique do botao inserir do arquivo
def arq_button():
    global arvore
    global RAIZ
    nos = read()

    for i in range(len(nos)):
        if RAIZ is False:
            arvore = Node(nos[i][0], nos[i][1:len(nos[i])])
            RAIZ = True

        else:
            arvore.insere(nos[i][0], nos[i][1:len(nos[i])])

# funcao para o evento de clique do botao inserir manual
def manual_button():
    global EntryID
    global EntryName
    ManualInsert = Tk()  # cria uma janela
    ManualInsert.title('AVL')  # seta o titulo da janela
    ManualInsert.geometry('300x200')  # seta o tamanho da janela
    EntryID = Entry(ManualInsert, width=25, justify='center')  # cria uma entrada de texto
    EntryName = Entry(ManualInsert, width=25, justify='center')  # cria uma entrada de texto
    EntryID.insert(0, 'Valor')  # seta o texto
    EntryName.insert(0, 'Nome')  # seta o texto
    EntryID.bind('<Button-1>', lambda event: limparTexto(EntryID))  # Limpa o texto quando se clica (campo valor)
    EntryID.pack()  # gerenciador de geometria
    EntryName.bind('<Button-1>', lambda event: limparTexto(EntryName))  # Limpa o texto quando se clica(campo nome)
    EntryName.pack()
    EntryID.focus_set()  # obtem o foco para a entrada de texto
    EntryName.focus_set()
    insert_btn = Button(ManualInsert, text='Inserir', width=20, command=inserir_btn_func) #botão de inserir
    insert_btn.pack()


def limparTexto(self):  # funcao para limpar text field quando clicado
    self.delete('0', END)

def inserir_btn_func():
    notification = Tk()
    notification.title("Nó inserido")
    notification.geometry("300x50")
    global arvore
    global RAIZ
    words = []
    try:
        words = EntryName.get().split(" ")
    except:
        pass

    if not EntryID.get():  # [] entrada vazia
        label = Label(notification, text="Digite a ID do Nó a ser  inserido", height=0, width=100)
    else:
        if RAIZ is False:
            global arvore
            arvore = Node(int(EntryID.get()), words)
        else:
            arvore.insere(int(EntryID.get()), words)
        label = Label(notification, text="Nó " + EntryID.get() + " inserido", height=0, width=100)

        RAIZ = True

    b = Button(notification, text="ok", width=20, command=notification.destroy)
    label.pack()
    b.pack(side='bottom', padx=0, pady=0)


def remover_button():
    global entrada
    janelaRemover = Tk()  # cria uma janela
    janelaRemover.title('Remover')  # seta o titulo da janela
    janelaRemover.geometry('150x50')  # seta o tamanho da janela
    entrada = Entry(janelaRemover, width=25, justify='center')  # cria uma entrada de texto
    entrada.insert(0, 'Numero para remover')  # seta o texto
    entrada.pack()  # gerenciador de geometria
    entrada.focus_set()  # obtem o foco para a entrada de texto     
    entrada.bind('<Button-1>', lambda event: limparTexto(entrada))
    remover_btn = Button(janelaRemover, text='Remover', width=20, command=remover_button_func)  # botão de remover
    remover_btn.pack()

def remover_button_func():
    global arvore
    if not entrada.get():  # [] entrada vazia
        entrada.insert(0, 'Digite o Nó')
    else:
        localizarOk = arvore.localizar(int(entrada.get()))
        print ":>>>>>>>>>>>>>>>>>>>>>>>>",localizarOk
        remover = int(entrada.get())

        if localizarOk is 1:
            arvore.remover(int(entrada.get()))
            arvore.rebalanceamento()
            encontrado = Tk()
            encontrado.title("Remoção")
            encontrado.geometry('300x50')
            resultado = Label(encontrado, text='Nó removido com sucesso.')
            resultado.pack()
        elif localizarOk is 0:
            naoencontrado = Tk()
            naoencontrado.title("Remoção")
            naoencontrado.geometry('300x50')
            resultado = Label(naoencontrado, text='Nó não encontrado.')
            resultado.pack()



def localizar_button():
    global localizado
    global valor
    pesquisar = Tk()  # cria uma janela
    pesquisar.title("Localizar")  # seta o titulo da janela
    pesquisar.geometry("200x70")  # seta o tamanho da janela
    valor = Entry(pesquisar, width=25, justify='center')  # cria uma entrada de texto
    valor.insert(0, "Digite o valor para localizar")  # seta o texto
    valor.pack()  # gerenciador de geometria
    valor.focus_set()  # obtem o foco para a entrada de texto
    localizarBtn = Button(pesquisar, text='Localizar', width=20, command = BtnLocalizarCmd)  # botão de inserir
    localizarBtn.pack()
    valor.bind('<Button-1>', lambda event: limparTexto(valor))

def  BtnLocalizarCmd():

    if not valor.get():  # [] entrada vazia
        valor.insert(0, 'Digite o Nó')
    else:
       arvore.localizar(int(valor.get()))
    
def telaLocalizarPalavra():
    global numero
    global posicao
    pesquisar = Tk()  # cria uma janela
    pesquisar.title("Localizar com Palavra")  # seta o titulo da janela
    pesquisar.geometry("200x70")  # seta o tamanho da janela
    numero = Entry(pesquisar, width=25, justify='center')  # cria uma entrada de texto
    numero.insert(0, "Digite a chave")  # seta o texto
    numero.pack()  # gerenciador de geometria
    numero.focus_set()  # obtem o foco para a entrada de texto
    posicao = Entry(pesquisar, width=25, justify='center')  # cria uma entrada de texto
    posicao.insert(0, "Digite a posicao[0,1,2...]")  # seta o texto
    posicao.pack()  # gerenciador de geometria
    posicao.focus_set()  # obtem o foco para a entrada de texto
    numero.bind('<Button-1>', lambda event: limparTexto(numero))
    posicao.bind('<Button-1>', lambda event: limparTexto(posicao))
    localizarBtn = Button(pesquisar, text='Buscar', width=20, command = BtnLocalizarPalavracmd)  # botão de inserir
    localizarBtn.pack()

def BtnLocalizarPalavracmd():
    if not numero.get() or not posicao.get():  # [] entrada vazia
        numero.insert(0, 'Digite o Nó')
        posicao.insert(0, 'Digite o Nó')
    else:
        arvore.localizarindice(int(numero.get()),int(posicao.get()))
       
def identacao_button():
    notification = Tk()
    notification.title("Nó inserido")
    notification.geometry("300x50")
    arvore.imprimeArvore()
    label = Label(notification, text="Verificar o console", height=0, width=100)
    b = Button(notification, text="ok", width=20, command=notification.destroy)
    label.pack()
    b.pack(side='bottom', padx=0, pady=0)


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
        pygame.draw.circle(screen, Blue, (nodes[i][1][0] / 2, nodes[i][1][1]), 20, 2)
        text = font.render(str(nodes[i][0]), True, Black)
        screen.blit(text, (nodes[i][1][0] / 2 - 10, nodes[i][1][1] - 10))
        text = font.render(str(fatores[i]), True, Black)
        screen.blit(text, (nodes[i][1][0] / 2 + 25, nodes[i][1][1] - 10))
        for j in range(1, len(nodes)):
            pygame.draw.aaline(screen, Cyan, (nodes[j][2][0] / 2, nodes[j][2][1] + 20),
                               (nodes[j][1][0] / 2, nodes[j][1][1] - 20), 3)
    fpsClock = pygame.time.Clock()
    pygame.display.update()
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
    pygame.quit()


import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def limparConsole_button():
    cls()


btn_arq = Button(window, text='Inserir do Arquivo', width=20, command=arq_button)
btn_manual = Button(window, text='Inserir Nó Manualmente', width=20, command=manual_button)
btn_remover = Button(window, text='Remover Nó', width=20, command=remover_button)
btn_identacao = Button(window, text='Notação Indentada', width=20, command=identacao_button)
btn_localizar = Button(window, text='Localizar Nó', width=20, command=localizar_button)
btn_localizarPalavra = Button(window, text='Localizar Nó com palavra', width=20, command=telaLocalizarPalavra)
btn_natural = Button(window, text='Notação Natural', width=20, command=natural_button)
btn_limpConsole = Button(window, text='Limpar Console', width=20, command=limparConsole_button)

btn_arq.pack()
btn_manual.pack()
btn_remover.pack()
btn_localizar.pack()
btn_localizarPalavra.pack()
btn_identacao.pack()
btn_natural.pack()
btn_limpConsole.pack()

window.mainloop()
