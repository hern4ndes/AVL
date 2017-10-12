"""
O que fazer a seguir:
Tentar ver os casos de nos iguais
Verficar se as acoes de rotacao condizem os os nomes das funcoes
Comecar a trabalhar na interface grafica
"""
class Node:
    def __init__(self, chave):
        self.chave = chave
        self.filhos(None, None)

    def filhos(self, esquerda, direita):
        self.esquerda = esquerda
        self.direita = direita

    def FB(self):
        profE = 0
        if self.esquerda:
            profE = self.esquerda.profundidade()
        profD = 0
        if self.direita:
            profD = self.direita.profundidade()
        return profD - profE

    def profundidade(self):
        profE = 0
        if self.esquerda:
            profE = self.esquerda.profundidade()
        profD = 0
        if self.direita:
            profD = self.direita.profundidade()
        return 1 + max(profE, profD)

    def rot_E(self):
        self.chave, self.direita.chave = self.direita.chave, self.chave
        old_esquerda = self.esquerda
        self.filhos(self.direita, self.direita.direita)
        self.esquerda.filhos(old_esquerda, self.esquerda.esquerda)

    def rot_D(self):
        self.chave, self.esquerda.chave = self.esquerda.chave, self.chave
        old_direita = self.direita
        self.filhos(self.esquerda.esquerda, self.esquerda)
        self.direita.filhos(self.direita.direita, old_direita)

    def rot_dup_D(self):
        self.esquerda.rot_E()
        self.rot_D()

    def rot_dup_E(self):
        self.direita.rot_D()
        self.rot_E()

    def executaBalanco(self):
        bal = self.FB()
        if bal > 1:
            if self.direita.FB() > 0:
                self.rot_E()
            else:
                self.rot_dup_E()
        elif bal < -1:
            if self.esquerda.FB() < 0:
                self.rot_D()
            else:
                self.rot_dup_D()

    def insere(self, chave):
        if chave <= self.chave:
            if not self.esquerda:
                self.esquerda = Node(chave)
            else:
                self.esquerda.insere(chave)
        else:
            if not self.direita:
                self.direita = Node(chave)
            else:
                self.direita.insere(chave)
        self.executaBalanco()

    def imprimeArvore(self, indent = 0, count = 0, pai = 0):
        count = count + 1

        if count is 1:
            print " "
            print " " * indent + str(self.chave) + '  (raiz FB: ' + str(self.FB()) + ')'
        else:
            print " " * indent + str(self.chave) + '  (pai: ' + str(pai) + ' FB: '+ str(self.FB()) + ')'
            pai = 0

        if self.esquerda:
            self.esquerda.imprimeArvore(indent + 2, count + 2, pai + self.chave)
        if self.direita:
            self.direita.imprimeArvore(indent + 2, count + 2, pai + self.chave)

incl_raiz = False #Var. global que informa se ha uma raiz inserida, ou seja, se o __init_ da classe ja foi realizado

def menu():
    validacao = True #true neste caso assume a invalidez da resposta
    while validacao:
        print("1. Inserir manualmente\n2. Printar arvore (identacao)\n3. Inserir a partir do arquivo\n")
        resp = input('Resposta: ')
        if resp<0 or resp >3:
            validacao = True
        else:
            validacao = False
    return resp

def main():
    global incl_raiz
    while True:
        resp = menu()
        if resp is 1:
            if incl_raiz is False:
                arvore = Node(input('[Manualmente] Raiz: '))
                incl_raiz = True
            else:
                arvore.insere(input('[Manualmente] No: '))
            limpaTela()
        elif resp is 2:
            arvore.imprimeArvore()
            print ""
        elif resp is 3:
            nos = read()
            for no in nos:
                if incl_raiz is False:
                    arvore = Node(no)
                    incl_raiz = True
                else:
                    arvore.insere(no)
        elif resp is 0:
            return 0

def read():
    """
    Objetivo: Ler os elementos do arquivo .TXT e retorna-los como inteiros.
    Parametros: Nao se aplica
    Retorno: Vetor de inteiros a serem inseridos como nos na arvore
    """
    arquivo = open("INPUT.TXT","r") #abre arquivo com nos
    nodes = arquivo.read().split(';') #vetor nodes recebe os elementos no formato string
    nodes.pop() #removendo o ultimo elemento que e um elemento vazio (do editor de texto)
    nodes = [int(x) for x in nodes] #transformacao dos elementos do vetor de string em vetor de inteiros
    return nodes #retornando um vetor de inteiros

import os
limpaTela = lambda: os.system('cls') # para limpar a tela

if __name__ == '__main__':
    main()
