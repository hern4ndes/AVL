#!/usr/bin/python
# -*- coding: utf8 -*-

class Node:
    def __init__(self, chave):
        #Inicia a arvore colocando uma raiz ou apenas coloca um no
        self.chave = chave
        self.filhos(None, None)
        self.posicao = (None,None)
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
            print '\nNo localizado:\n No: ' + str(self.chave) + '\n Pai: ' + str(pai) + '\n Filhos:\n  Esquerda: ' + filhoesq + '\n  Direita: ' + filhodir + '\n FB: ' + str(self.FB())

    def remover(self, chave):
        global incl_raiz
        #avalia o caso especial de remocao e depois manda pra remocao
        if chave == self.chave:
            if self.esquerda is None and self.direita is not None:
                self.chave = self.direita.chave
                self.filhos = self.direita.filhos
                self.direita = self.direita.direita
            elif self.direita is None and self.esquerda is not None:
                self.chave = self.esquerda.chave
                self.filhos = self.esquerda.filhos
                self.esquerda = self.esquerda.esquerda
            elif self.direita is None and self.esquerda is None:
                self.__init__('Arvore vazia. Insira nos.')
                incl_raiz = False
            else:
                self.remocao(chave)
        else:
            self.remocao(chave)

    def remocao(self, chave):
        if chave < self.chave:
            self.esquerda = self.esquerda.remocao(chave)
        elif chave > self.chave:
            self.direita = self.direita.remocao(chave)
        else:
            if self.direita is None:
                return self.esquerda
            if self.esquerda is None:
                return self.direita
            aux = self.direita.menor()
            self.chave = aux.chave
            self.direita = self.direita.deletamenor()
        return self

    def menor(self):
        if self.esquerda is None:
            return self
        else:
            return self.esquerda.menor()

    def deletamenor(self):
        if self.esquerda is None:
            return self.direita
        self.esquerda = self.esquerda.deletamenor()
        return self

    def rebalanceamento(self):
        if self.esquerda is not None:
            self.esquerda.rebalanceamento()
        bal = self.FB()
        if bal > 1:
            if self.direita.direita is not None:
                print 'Rebalanceamento: Rotacao a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_E()
            else:
                print 'Rebalanceamento: Rotacao dupla a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_dup_E()
        elif bal < -1:
            if self.esquerda.esquerda is not None:
                print 'Rebalanceamento: Rotacao a direita em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB())
                self.rot_D()
            else:
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
            print " " * indent + str(self.chave) +'  (raiz FB: ' + str(self.FB()) + ')'
        else:
            print " " * indent + str(self.chave) +'  (pai: ' + str(pai) + ' FB: '+ str(self.FB()) + ')'
            pai = 0

        #navega recursivamente na arvore levando como paramentros instrucoes para a printagem
        if self.esquerda:
            self.esquerda.imprimeArvore(indent + 2, count + 2, pai + self.chave)
        if self.direita:
            self.direita.imprimeArvore(indent + 2, count + 2, pai + self.chave)

    def calculaNiveis(self, rootOk = 0, nivelRoot = 0):
        #calcula os niveis dos nos pra ajudar no calculo da posicao
        rootOk = rootOk + 1
        if rootOk == 1:
            nivelRoot = self.altura()
        else:
            self.nivel = nivelRoot - self.altura() + 1
        if self.esquerda:
            self.esquerda.calculaNiveis(rootOk + 2, nivelRoot = nivelRoot)
        if self.direita:
            self.direita.calculaNiveis(rootOk + 2, nivelRoot = nivelRoot)

    def calcposicao(self,  rootOk = 0, posPai = [0,0], lado = 0):
        nodes = []
        #Calcula as posicoes para orientar o desenho na interface grafica
        rootOk = rootOk + 1
        node = ()
        if rootOk == 1:
            self.posicao = (1000,  100)
            node = (self.chave,self.posicao)
            nodes.append(node)
        else:
            if lado == 1:
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = 1000/aux
                self.posicao = [posPai[0] - deslocamento, posPai[1]+100]
                print self.posicao
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)
            else:
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = 1000/aux
                self.posicao = [posPai[0] + deslocamento, posPai[1]+100 ]
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)

        if self.esquerda:
            self.esquerda.calcposicao(rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 1)
        if self.direita:
            self.direita.calcposicao (rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 2)

        return nodes

