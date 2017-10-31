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
                incl_raiz = False
            else:
                #se nao for nenhum dos casos acima, faz a remocao com os outros casos no outro metodo
                #nesse caso, se o no a ser removido for uma raiz mas nao dos casos espciais acima
                self.remocao(chave)
        else:
            #qualquer outro no ou caso de remocao
            self.remocao(chave)

    def remocao(self, chave):
        #remocao de no folha ou no com apenas um filho, recursivamente. usa os retornos a cada recursao pra percorrer e substituir o no apagado
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
        nodes = []
        #Calcula as posicoes para orientar o desenho na interface grafica
        #coloca em cada no sua posicao (ou posicao aproximada) a ser desenhada na interface grafica da arvore, dependendo de seu parentesco entre outros
        rootOk = rootOk + 1
        node = ()
        if rootOk == 1:
            #da uma posicao centralizada para a raiz
            self.posicao = (1000,  100)
            node = (self.chave,self.posicao)
            nodes.append(node)
        else:
            #calculo para o restante dos nos
            if lado == 1:
                #lado 1 = esquerda
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = 1000/aux
                #calcula um deslocamento adequado para o nivel de cada no
                self.posicao = [posPai[0] - deslocamento, posPai[1]+100]
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)
                #coloca informacoes no vetor nodes para poder levar para a funcao que desenha na tela a arvore
            else:
                #lado 2 = direita
                aux = 2 ** self.nivel
                aux = aux/2
                deslocamento = 1000/aux
                #calcula um deslocamento adequado para o nivel de cada no
                self.posicao = [posPai[0] + deslocamento, posPai[1]+100 ]
                node = (self.chave,self.posicao,posPai)
                nodes.append(node)
                #coloca informacoes no vetor nodes para poder levar para a funcao que desenha na tela a arvore

        if self.esquerda:
            self.esquerda.calcposicao(rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 1)
        if self.direita:
            self.direita.calcposicao (rootOk + 2, posPai = [self.posicao[0], self.posicao[1]], lado = 2)

        return nodes
        #retorna o vetor de nos.
