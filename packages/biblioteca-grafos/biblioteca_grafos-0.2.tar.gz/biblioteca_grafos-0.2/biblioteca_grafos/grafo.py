# my_library/classe_exemplo.py
from collections import defaultdict, deque

class Grafo:
    def __init__(self):
        self.grafo = {}
        self.qtdVertices = 0
        self.visitado = []
        self.lista_adjacencia = {}
        self.matriz_adjacencia = []
        self.armazenar_grafo()

    def informacoes(self):
        mensagem = ''
        contagem_arestas = 0
        soma_grau = 0

        with open('entrada.txt', 'r') as arquivo:
            # Lê a primeira linha separadamente
            qtdVertices = next(arquivo).strip()
            mensagem += f"Quantidade de vertices: {qtdVertices}\n"
            contagem_numeros = defaultdict(int)

            # Agora lê o restante das linhas
            for linha in arquivo:
                contagem_arestas+=1
                numeros = linha.split()
                for numero in numeros:
                    numero = int(numero)  # Converte para inteiro
                    contagem_numeros[numero] += 1  # Incrementa a contagem para esse número
            
            mensagem += f"Quantidade de arestas: {contagem_arestas}\n"

            # Exibe o número de ocorrências de cada número
            for numero, contagem in contagem_numeros.items():
                # Incrementa a soma dos graus de cada vértice para se realizar o cálculo do grau médio posteriormente
                soma_grau += contagem
            
            mensagem += f"Grau medio: {int(soma_grau)/int(qtdVertices)}\n"

            # Resgata o maior valor registrado no dicionário (grau máximo)
            maior_grau = max(contagem_numeros.values())
        
            # Contagem de quantos vértices têm cada grau
            contagem_graus = defaultdict(int)
            for grau in contagem_numeros.values():
                contagem_graus[grau] += 1
            
            # DISTRIBUIÇÃO EMPÍRICA
            for grau in range(1, maior_grau + 1):
                qtd = contagem_graus.get(grau, 0) # Se o grau não existir, retorna 0
                mensagem += f'{grau} {int(qtd) / int(qtdVertices)}\n'
        
        with open('saida.txt', 'w') as arquivo_saida:
            arquivo_saida.write('--------------INFORMACOES DO GRAFO--------------\n\n')

        with open('saida.txt', 'a') as arquivo_saida:
            arquivo_saida.write(f'{mensagem}\n')
        
        return print('Arquivo de saida com informacoes gerado')
    
    def representacao(self):
        while True:
            print('Digite 1 para Representação por matriz de adjacência')
            print('Digite 2 para Representação por lista de adjacência')
            try:
                escolha = int(input("Escolha: "))
                
                if escolha == 1:
                    self.rep_matriz()
                    break  
                elif escolha == 2:
                    self.rep_lista()
                    break  
                else:
                    print("Opção inválida! Por favor, digite 1 ou 2.")
            except ValueError:
                print("Entrada inválida! Por favor, insira um número.")

    def rep_matriz(self):
        print('==================== RESULTADO =========================\n')        
        return print(f'Matriz de adjacencia: \n\n{self.matriz_adjacencia}\n')
    
    def rep_lista(self):
        
        with open('entrada.txt', 'r') as arquivo:
            lista_adjacencia = ''

            # Lê a primeira linha separadamente
            qtdVertices = int(next(arquivo).strip())
            relacionamento_numeros = defaultdict(str)
            numeros_unicos = set()

            for linha in arquivo:
                numeros = linha.split()
                vertice1 = numeros[0]
                vertice2 = numeros[1]
                    
                relacionamento_numeros[f'{vertice1}'] += f'-> {vertice2}'
                relacionamento_numeros[f'{vertice2}'] += f'-> {vertice1}'
                for numero in numeros:
                    numeros_unicos.add(int(numero)) 

            for numero_unico in numeros_unicos:
                lista_adjacencia += f'{numero_unico}{relacionamento_numeros[f'{numero_unico}']}\n'

            print('\n')
            print('==================== RESULTADO =========================\n')
            
        return print(f'Lista de Adjacencia: \n\n{lista_adjacencia}')
    
    def armazenar_grafo(self):

        with open('entrada.txt', 'r') as arquivo:

            # Lê a primeira linha separadamente
            self.qtdVertices = int(next(arquivo).strip())
            self.matriz_adjacencia = [[0 for _ in range(self.qtdVertices)] for _ in range(self.qtdVertices)]

            for linha in arquivo:
                numeros = linha.split()
                if len(numeros) >= 2:
                    vertice1 = int(numeros[0])
                    vertice2 = int(numeros[1])
                    
                    self.matriz_adjacencia[vertice1-1][vertice2-1] = 1
                    self.matriz_adjacencia[vertice2-1][vertice1-1] = 1
        
        for i in range(self.qtdVertices):
            for j in range(self.qtdVertices):
                if self.matriz_adjacencia[i][j] == 1:
                    self.grafo[i+1] = self.grafo.get(i+1, [])
                    self.grafo[i+1].append(j+1)
    
    def dfs_componente(self, v, visitado, componente_atual):
        visitado[v] = True
        componente_atual.append(v)
        
        for u in self.grafo[v]:
            if not visitado[u]:
                self.dfs_componente(u, visitado, componente_atual)

    def busca_profundidade(self, v, primeira_chamada=True, caminho=[], pai='Nenhum', nivel=0, saida=[]):

        if v in self.grafo.keys():

            if not self.visitado:
                self.visitado = [False] * (len(self.grafo) + 1)
            
            self.visitado[v] = True
            caminho.append(f' {v} ')  # Adiciona o vértice ao caminho
            saida.append(f'Vertice: {v} -> Nivel: {nivel} | Pai: {pai} \n')

            for u in self.grafo[v]:
                if not self.visitado[u]:
                    self.busca_profundidade(u, primeira_chamada=False, caminho=caminho, pai=str(v), nivel=nivel+1, saida=saida)

            if primeira_chamada:
                # Imprime o caminho ao final da pilha de execuções da chamada recursiva
                saida.append('\n')
                saida.append("->".join(map(str, caminho)))
                
                with open('saida.txt', 'a') as arquivo_saida:
                    arquivo_saida.write('--------------BUSCA POR PROFUNDIDADE--------------\n\n')
                    arquivo_saida.write(f'{"".join(saida)}\n\n')
                    return print('Arquivo de saida atualizado com informacoes da busca por profundidade')
        else:
            print('Não existe esse vértice no grafo, chame a função com outro vértice inicial')

    def busca_largura(self, v):

        if v in self.grafo.keys():

            visitadoLargura = [False] * (len(self.grafo) + 1)

            fila = deque([v])  # Usamos deque para operações eficientes de fila
            nivel = {v: 0}  # Dicionário para rastrear o nível de cada vértice
            pai = {v: 'Nenhum'} # Dicionário para rastrear o pai de cada vértice
            resultado = []

            while fila:
                vAtual = fila.popleft()  # Remove o primeiro elemento da fila
                if not visitadoLargura[vAtual]:
                    resultado.append(vAtual)
                    visitadoLargura[vAtual] = True
                    for i in self.grafo[vAtual]:
                        if not visitadoLargura[i]:
                            fila.append(i)
                            pai[i] = str(vAtual)
                            nivel[i] = nivel[vAtual] + 1
            
            with open('saida.txt', 'a') as arquivo_saida:
                saida = ''
                for vertice in resultado:
                    saida += (f"Vertice: {vertice} -> Nivel: {nivel[vertice]} | Pai: {pai[vertice]}\n")
                saida += f'\n'+ " -> ".join(map(str, resultado))
                arquivo_saida.write('--------------BUSCA POR LARGURA--------------\n\n')
                arquivo_saida.write(f'{saida}\n\n')
                return print('Arquivo de saida atualizado com informacoes da busca por largura')
        else:
            print('Não existe esse vértice no grafo, chame a função com outro vértice inicial')

    def encontrar_componentes_conexos(self):
        visitado = [False] * (len(self.grafo) + 1)
        componentes = []
        
        for v in self.grafo:
            if not visitado[v]:
                componente_atual = []
                self.dfs_componente(v, visitado, componente_atual)
                componentes.append(componente_atual)

        print("\nComponentes conexos do grafo:")
        for i, componente in enumerate(componentes):
            print(f"Componente {i + 1}: {componente}")
        print('')

def main():
   
    grafo = Grafo()

    # grafo.representacao()
    grafo.informacoes()
    grafo.busca_profundidade(2)
    grafo.busca_largura(1)
    grafo.encontrar_componentes_conexos()


if __name__ == "__main__":
    main()



# def desenhar_grafo(matriz_adjacencia):
#         qtdVertices = len(matriz_adjacencia)

#         # Para cada vértice, verificamos suas conexões
#         for i in range(qtdVertices):
#             for j in range(i, qtdVertices):
#                 if matriz_adjacencia[i][j] == 1:
#                     # Conexão horizontal
#                     print(f"{i+1} -- {j+1}")
        
#         print("\nRepresentação Completa do Grafo:")
#         for i in range(qtdVertices):
#             print(f"{i+1}: ", end="")
#             for j in range(qtdVertices):
#                 if matriz_adjacencia[i][j] == 1:
#                     print(f" {j+1}", end="")
#             print()


