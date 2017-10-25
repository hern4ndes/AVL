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
                print 'CASO NO NA DIREITA'
                self.chave = self.direita.chave
                self.filhos = self.direita.filhos
                self.direita = self.direita.direita
            elif self.direita is None and self.esquerda is not None:
                print 'CASO NO NA ESQUERDA'
                self.chave = self.esquerda.chave
                self.filhos = self.esquerda.filhos
                self.esquerda = self.esquerda.esquerda
            elif self.direita is None and self.esquerda is None:
                print 'CASO APENAS RAIZ'
                self.__init__('Arvore vazia. Insira nos.')
                incl_raiz = False
            else:
                print 'CASO RAIZ COM DOIS FILHOS (NAO E ESPECIAL)'
                self.remocao(chave)
        else:
            print 'NEM UM POUCO ESPECIAL'
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
                print 'rot esq in ' + str(self.chave) + ' FB: ' + str(self.FB())
                self.rot_E()
                #return
            else:
                print 'rot dup esq in ' + str(self.chave) + ' FB: ' + str(self.FB())
                self.rot_dup_E()
                #return
        elif bal < -1:
            if self.esquerda.esquerda is not None:
                print 'rot dir in ' + str(self.chave) + ' FB: ' + str(self.FB())
                self.rot_D()
                #return
            else:
                print 'rot dup dir in ' + str(self.chave) + ' FB: ' + str(self.FB())
                self.rot_dup_D()
                #return

        print 'visitado:' + str(self.chave)
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


incl_raiz = False #Var. global que informa se ha uma raiz inserida, ou seja, se o __init_ da classe ja foi realizado

def menu():
    #Exibe um menu simples para auxiliar o usuario
    validacao = True #true neste caso assume a invalidez da resposta
    while validacao:
        print("\n1. INPUT.txt\n2. Inserir manualmente\n3. Exibir arvore (identacao)\n4. Localizar\n5. Remover no\n0. Sair\n")
        resp = input('Resposta: ')
        if resp<0 or resp >5:
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
                arvore = Node(input('Chave do no para inserir: '))
                incl_raiz = True
            else:
                arvore.insere(input('Chave do no para inserir: '))
        elif resp is 3: #chama a funcao imprimeArvore da classe Node para imprimir a arvore
            arvore.imprimeArvore()
            print ""
        elif resp is 4:
            arvore.localizar(input('Chave do no para localizar: '))
        elif resp is 5:
            arvore.remover(input('Chave do no para remover: '))
            arvore.imprimeArvore()
            arvore.rebalanceamento()
        elif resp is 0: #da ordem de saida do main e consequentemente do programa
            return 0

def read():
    #Le os elementos do arquivo e os coloca em um vetor de inteiros
    arquivo = open("INPUT.TXT","r") #abre arquivo com nos
    nodes = arquivo.read().split(';') #vetor nodes recebe os elementos no formato string
    ultimo = float(nodes[-1])
    nodes[-1] = int(ultimo)
    nodes = [int(x) for x in nodes] #transformacao dos elementos do vetor de string em vetor de inteiros
    return nodes #retornando um vetor de inteiros

if __name__ == '__main__':
    main()
