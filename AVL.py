class Node:
    def __init__(self, chave):
        #Inicia a arvore colocando uma raiz ou apenas coloca um no
        self.chave = chave
        self.filhos(None, None)

    def filhos(self, esquerda, direita):
        #Configura os filhos de um no
        self.esquerda = esquerda
        self.direita = direita

    def FB(self):
        #Usa as profundidades para calcular os fatores de balanceamento
        profE = 0
        if self.esquerda:
            profE = self.esquerda.profundidade()
        profD = 0
        if self.direita:
            profD = self.direita.profundidade()
        return profD - profE

    def profundidade(self):
        #Calcula a profundidade dos lados da arvore (esquerdo ou direito)
        #Basicamente entra recursivamente arvore ate achar o fim. Sao duas variaveis sendo incrementadas.
        #Como a profundidade pode envolver lado oposto(no caso do esquerdo, se nao haver mais esquerdo, pode se procurar filho direito pra continuar calculando)
        #E no final eh retornado o que incrementou mais(que e o que realmente vale)
        profE = 0
        if self.esquerda:
            profE = self.esquerda.profundidade()
        profD = 0
        if self.direita:
            profD = self.direita.profundidade()
        return 1 + max(profE, profD) #Retorna 1 + a mais incrementada

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
        self.executaBalanco() #Apos inserir executa o balanceamento da arvore

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
        if self.direita:
            self.direita.imprimeArvore(indent + 2, count + 2, pai + self.chave)
        if self.esquerda:
            self.esquerda.imprimeArvore(indent + 2, count + 2, pai + self.chave)

incl_raiz = False #Var. global que informa se ha uma raiz inserida, ou seja, se o __init_ da classe ja foi realizado

def menu():
    #Exibe um menu simples para auxiliar o usuario
    validacao = True #true neste caso assume a invalidez da resposta
    while validacao:
        print("1. INPUT.txt\n2. Inserir manualmente\n3. Exibir arvore (identacao)\n0. Sair\n")
        resp = input('Resposta: ')
        if resp<0 or resp >3:
            validacao = True
        else:
            validacao = False
    return resp

def main():
    global incl_raiz #inclui a variavel global que conta se ha raiz inserida
    while True: #Roda o main ate que receba a ordem para sair
        resp = menu()
        if resp is 1: #le o INPUT.txt para inserir nos
            nos = read()
            for no in nos:
                if incl_raiz is False:
                    arvore = Node(no)
                    incl_raiz = True
                else:
                    arvore.insere(no)
        elif resp is 2: #insere manualmente pelo input do user
            if incl_raiz is False:
                arvore = Node(input('Chave do no: '))
                incl_raiz = True
            else:
                arvore.insere(input('Chave do no: '))
        elif resp is 3: #chama a funcao imprimeArvore da classe Node para imprimir a arvore
            arvore.imprimeArvore()
            print ""
        elif resp is 0: #da ordem de saida do main e consequentemente do programa
            return 0

def read():
    #Le os elementos do arquivo e os coloca em um vetor de inteiros
    arquivo = open("INPUT.TXT","r") #abre arquivo com nos
    nodes = arquivo.read().split(';') #vetor nodes recebe os elementos no formato string
    if nodes[-1] is "": #Se for usado ";" o split vai ler um elemento vazio. Entao chama a funcao abaixo para remover esse elemento vazio
        nodes.pop() #removendo o ultimo elemento que e um elemento vazio (do editor de texto)
    else: #Caso foi usado "." no fim, ele transforma a "chave." (chave com ponto) em um float(por causa do ponto) e depois em int, para ser transformado em chaves para nos na lista nodes
        ultimo = float(nodes[-1]) #
        nodes[-1] = int(ultimo)
    nodes = [int(x) for x in nodes] #transformacao dos elementos do vetor de string em vetor de inteiros
    return nodes #retornando um vetor de inteiros

import os
limpaTela = lambda: os.system('cls') # para limpar a tela

if __name__ == '__main__':
    main()
