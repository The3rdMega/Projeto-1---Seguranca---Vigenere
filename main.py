from typing import Union
from unidecode import unidecode
import math
"""
Parte I: cifrador/decifrador
O cifrador recebe uma chave e uma mensagem que é cifrada segundo a cifra de Vigenère,
gerando um criptograma, enquanto o decifrador recebe uma chave e um criptograma que
é decifrado segundo a cifra de Vigenère, recuperando uma mensagem. Os primeiros
usuários da cifra de Vigenère utilizavam um “quadrado de Vigenère” (como mostrado na
Figura 1) para descobrir rapidamente qual letra do texto cifrado usar, dado um texto 
plano e fluxo de teclas específicos.
"""

"""
Funcionamento do Vigenère:
- Assuma uma "chave" e uma "mensagem"
- Repita a chave em padrão cíclico até que ela seja do tamanho da mensagem
- Converta cada letra da chave para um número de 1 a 26 usando A1Z26
- Para encriptar: Para cada index da string de palavras (excluindo "espaço"), 
  desloque o caractere para a direita do alfabeto o exato número de vezes determinado 
  pelo index da chave
- Para decriptar: Faça o exato mesmo com o ciphertext, mas desloque para a esquerda
"""

# Variáveis Globais
dicionarioA1Z26 = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
dicionarioA1Z26_invertido = {value: key for key, value in dicionarioA1Z26.items()}
frequenciaPortugues = {
                        'a':	14.63,
                        'b':	1.04,
                        'c':	3.88,
                        'd':	4.99,
                        'e':	12.57,
                        'f':	1.02,
                        'g':	1.30,
                        'h':	1.28,
                        'i':	6.18,
                        'j':	0.40,
                        'k':	0.02,
                        'l':	2.78,
                        'm':	4.74,
                        'n':	5.05,
                        'o':	10.73,
                        'p':	2.52,
                        'q':	1.20,
                        'r':	6.53,
                        's':	7.81,
                        't':	4.34,
                        'u':	4.63,
                        'v':	1.67,
                        'w':	0.01,
                        'x':	0.21,
                        'y':	0.01,
                        'z':	0.47
}
frequenciaIngles = {
                        'a':	8.167,
                        'b':	1.492,
                        'c':	2.782,
                        'd':	4.253,
                        'e':	12.702,
                        'f':	2.228,
                        'g':	2.015,
                        'h':	6.094,
                        'i':	6.966,
                        'j':	0.153,
                        'k':	0.772,
                        'l':	4.025,
                        'm':	2.406,
                        'n':	6.749,
                        'o':	7.507,
                        'p':	1.929,
                        'q':	0.095,
                        'r':	5.987,
                        's':	6.327,
                        't':	9.056,
                        'u':	2.758,
                        'v':	0.978,
                        'w':	2.360,
                        'x':	0.150,
                        'y':	1.974,
                        'z':	0.074
}

class Vigenere:        
    def conversor_A1Z26(self, chave: str) -> Union[list[int],int]:
        if len(chave) > 1:
            listaNumerica = []
            for caractere in chave:
                listaNumerica.append(dicionarioA1Z26[caractere])
            return listaNumerica
        else:
            return [dicionarioA1Z26[caractere] for caractere in chave]

    def cifrador(self, chave, mensagem):
        criptograma = ''
        mensagem = mensagem.lower()
        mensagemOriginal = mensagem #armazenar os indexes de espaços para depois
        mensagem = mensagem.replace(" ", "")
        mensagem = unidecode(mensagem)
        tamanho = len(mensagem)  
        chaveExtendida = (chave * (tamanho // len(chave) + 1)) [:tamanho] #Repete a chave tamanho vezes e remove o texto extra que ultrapassa o tamanho da mensagem
        
        # chaveExtendida e Mensagem tem o mesmo tamanho
        
        # Converter chaveExtendida para lista de números (1 a 26)
        chaveNumerica = self.conversor_A1Z26(chaveExtendida)
        for index, char in enumerate(mensagem):
            pos_msg = dicionarioA1Z26[char] - 1
            pos_key = chaveNumerica[index] - 1
            deslocamento = ((pos_msg + pos_key) % 26) + 1
            criptograma += dicionarioA1Z26_invertido[deslocamento]
            
        # Colocar os espaços novamente no criptograma
        criptogramaChars= iter(criptograma)
        criptograma = "".join(
            char if char == " " else next(criptogramaChars)
            for char in mensagemOriginal
        )

        return criptograma


    def decifrador(self, chave, criptograma):
        mensagem = ''
        criptograma = criptograma.lower()
        criptogramaOriginal = criptograma #armazenar os indexes de espaços para depois
        criptograma = criptograma.replace(" ", "")
        criptograma = unidecode(criptograma)
        tamanho = len(criptograma)  
        chaveExtendida = (chave * (tamanho // len(chave) + 1)) [:tamanho] #Repete a chave tamanho vezes e remove o texto extra que ultrapassa o tamanho do criptograma
        
        # chaveExtendida e Criptograma tem o mesmo tamanho
        
        # Converter chaveExtendida para lista de números (1 a 26)
        chaveNumerica = self.conversor_A1Z26(chaveExtendida)
        for index, char in enumerate(criptograma):
            pos_cifra = dicionarioA1Z26[char] - 1
            pos_key = chaveNumerica[index] - 1
            deslocamento = ((pos_cifra - pos_key) % 26) + 1
            mensagem += dicionarioA1Z26_invertido[deslocamento]

        # Colocar os espaços novamente no criptograma
        mensagemChars= iter(mensagem)
        mensagem = "".join(
            char if char == " " else next(mensagemChars)
            for char in criptogramaOriginal
        )

        return mensagem

"""
Parte II: ataque de recuperação de chave por análise de frequência
Serão fornecidas duas mensagens cifradas (uma em português e outra em inglês)
com chaves diferentes. Cada uma das mensagens deve ser utilizada para 
recuperar a chave geradora do keystream usado na cifração e então decifradas.
Para as frequências das letras use: 
https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras

"""
class Atacante:
    def __init__(self):
        pass

    def kasiski(self, ciphertext: str) -> list[int]:
        # Primeiro, precisamos de alguma maneira de encontrar padrões espaçados de 3 letras
        # Memoização (Dicionário armazena trigramas conhecidos)
        # dicionário[trigrama(palavras de "três-letras" únicas encontradas)][list[int](lista das posições que esse trigrama aparece)]

        # Só por precaução, limpa o ciphertext de espaços em branco
        ciphertext = ciphertext.lower().replace(" ", "")

        # Então primeiro tem o parsing:
        frequenciaTrecho = dict()
        for n in range(len(ciphertext)-2):
            if ciphertext[n:n+3] in frequenciaTrecho:
                frequenciaTrecho[ciphertext[n:n+3]].append(n)
            else:
                frequenciaTrecho[ciphertext[n:n+3]] = [n]
        # frequenciaTrecho agora tem todas as combinações de palavras de 3 letras que aparecem no ciphertext
        # Como queremos apenas padrões de 3 letras repetidos, apagemos do dicionário todos os padrões que aparecem menos de 1 vez
        frequenciaTrecho = {trigrama: lista for trigrama, lista in frequenciaTrecho.items() if len(lista) >= 2}

        # Se não houver padrões repetidos, podemos tentar com bigramas
        if len(frequenciaTrecho) == 0:
            print("Kasiski não encontrou padrões de 3 letras. Tentando com 2...")
            frequenciaTrecho = dict()
            for n in range(len(ciphertext)-1):
                if ciphertext[n:n+2] in frequenciaTrecho:
                    frequenciaTrecho[ciphertext[n:n+2]].append(n)
                else:
                    frequenciaTrecho[ciphertext[n:n+2]] = [n]
            frequenciaTrecho = {trigrama: lista for trigrama, lista in frequenciaTrecho.items() if len(lista) >= 2}
            if len(frequenciaTrecho) == 0:
                return []
            



        # Agora, precisamos calcular as distâncias em si
        # Para isso, precisamos gerar um dicionário do formato: tamanho: int
        # distâncias possíveis:
        distanciasPossiveis = dict()
        for trigrama, lista in frequenciaTrecho.items():
            distancias = []
            for index in range(len(lista)-1): # [15,20,21] -> len(lista) = 3 -> range(3-1) = 2 = 0,1
                distanciaAtual = lista[index+1] - lista[index]
                if distanciaAtual in distancias:
                    pass # Se temos 2 distâncias iguais, tratamos ela como uma só, pois possívelmente é a mesma chave
                else:
                    distancias.append(distanciaAtual)
            # Precisamos dos divisores possíveis de cada uma dessas distâncias
            for item in distancias:
                divisores = [divisor for divisor in range(2,item+1) if item % divisor == 0]
                for divisor in divisores:
                    if divisor in distanciasPossiveis:
                        distanciasPossiveis[divisor] += 1
                    else:
                        distanciasPossiveis[divisor] = 1
        # Depois desse parsing, temos o dicionário distanciasPossiveis que contém o valor de cada distância, só precisamos colocar esses
        # valores em uma lista ordenada da chave com maior valor até a chave de menor valor:
        return sorted(distanciasPossiveis, key=distanciasPossiveis.get, reverse = True)
    

    def criarStreams(self, ciphertext: str, m: int):
        # Só por precaução, limpa o ciphertext de espaços em branco
        ciphertext = ciphertext.lower().replace(" ", "")
        return [list(ciphertext[streamValue :: m]) for streamValue in range(m)]

    def frequencia(self, stream: list[str]) -> dict[str, int]:
        # Mesma coisa do dicionário com memoização
        frequenciaStream = {letra: 0 for letra in dicionarioA1Z26}
        
        for caractere in stream:
            frequenciaStream[caractere] += 1
        
        return frequenciaStream
    
    def mapeamento(self, streamFrequency: dict[str, int], lingua: str):
        match lingua:
            case 'pt':
                dicionarioAlfabeto = frequenciaPortugues
            case 'en':
                dicionarioAlfabeto = frequenciaIngles
            case _:
                raise ValueError("Linguagem selecionada não suportada ou incorreta")
        
        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        menorValor = float('inf') # Começa com "infinito" para garantir que o primeiro valor será menor
        melhor_deslocamento = 0


        # Converte a stream para porcentagens:
        total = sum(streamFrequency.values())
        streamFrequency = {k: (v / total) * 100 for k, v in streamFrequency.items()}

        #Testa os 26 deslocamentos possíveis (0 a 25)
        for deslocamento in range(26):
            
            # Loop 2: O somatório do Qui-Quadrado comprimido em uma única linha
            valorAtual = sum(
                ((streamFrequency.get(alfabeto[i], 0) - dicionarioAlfabeto[alfabeto[(i - deslocamento) % 26]]) ** 2) 
                / dicionarioAlfabeto[alfabeto[(i - deslocamento) % 26]]
                for i in range(26)
            )

            # Verifica se este deslocamento é o vencedor
            if valorAtual < menorValor:
                menorValor = valorAtual
                melhor_deslocamento = deslocamento
        
        # Retorna a letra correspondente ao melhor deslocamento (ex: 3 vira 'd')
        return alfabeto[melhor_deslocamento]

    def conversor_A1Z26(self, chave: str) -> Union[list[int],int]:
            if len(chave) > 1:
                listaNumerica = []
                for caractere in chave:
                    listaNumerica.append(dicionarioA1Z26[caractere])
                return listaNumerica
            else:
                return [dicionarioA1Z26[caractere] for caractere in chave]

    def decifraMeOuTeDevoro(self, ciphertext1, ciphertext2):
        vigenere = Vigenere()

        print()
        print(" ATAQUE - MENSAGEM 1 (PT)")

        ciphertext1ORIGINAL = ciphertext1
        
        ciphertext1 = ciphertext1.lower().replace(" ", "")
        listaDePossiveisTamanhosPT = self.kasiski(ciphertext1)
        
        # Se a lista vier vazia, injetamos a força bruta nela mesma
        if not listaDePossiveisTamanhosPT:
            print("Kasiski não encontrou padrões. Tentando Bruteforce de 2 a 10...")
            listaDePossiveisTamanhosPT = [2, 3, 4, 5, 6, 7, 8, 9, 10]
            input("Pressione enter para tentar bruteforce")
        else:
            listaDePossiveisTamanhosPT = listaDePossiveisTamanhosPT[:5]
            print(f"O Kasiski sugeriu os tamanhos: [{', '.join(map(str, listaDePossiveisTamanhosPT))}, ...]")

        senhas_candidatas_PT = []

        # Único loop que varre toda a lista (seja a do Kasiski ou a do Bruteforce)
        for tamanho in listaDePossiveisTamanhosPT:
            senhaPT = ''
            listaDeStreams = self.criarStreams(ciphertext1, tamanho)
            
            for i in range(tamanho):
                listaDeFrequencias = self.frequencia(listaDeStreams[i])
                senhaPT += self.mapeamento(listaDeFrequencias, 'pt')
            
            senhas_candidatas_PT.append(senhaPT)


        print()
        print(" ATAQUE - MENSAGEM 2 (EN)")
        
        ciphertext2ORIGINAL = ciphertext2

        ciphertext2 = ciphertext2.lower().replace(" ", "")
        listaDePossiveisTamanhosEN = self.kasiski(ciphertext2)
        
        # Repetimos a lógica limpa para o inglês
        if not listaDePossiveisTamanhosEN:
            print("Kasiski não encontrou padrões. Tentando Bruteforce de 2 a 10...")
            listaDePossiveisTamanhosEN = [2, 3, 4, 5, 6, 7, 8, 9, 10]
            input("Pressione enter para tentar bruteforce")
        else:
            listaDePossiveisTamanhosEN = listaDePossiveisTamanhosEN[:5]
            print(f"O Kasiski sugeriu os tamanhos: [{', '.join(map(str, listaDePossiveisTamanhosEN))}, ...]")
            

        senhas_candidatas_EN = []

        for tamanho in listaDePossiveisTamanhosEN:
            senhaEN = ''
            listaDeStreams = self.criarStreams(ciphertext2, tamanho)
            
            for i in range(tamanho):
                listaDeFrequencias = self.frequencia(listaDeStreams[i])
                senhaEN += self.mapeamento(listaDeFrequencias, 'en') # Usando 'en' corretamente
            
            senhas_candidatas_EN.append(senhaEN)

        return (senhas_candidatas_PT,senhas_candidatas_EN)

    def decifrador(self, chave, criptograma):
        mensagem = ''
        criptograma = criptograma.lower()
        criptogramaOriginal = criptograma #armazenar os indexes de espaços para depois
        criptograma = criptograma.replace(" ", "")
        criptograma = unidecode(criptograma)
        tamanho = len(criptograma)  
        chaveExtendida = (chave * (tamanho // len(chave) + 1)) [:tamanho] #Repete a chave tamanho vezes e remove o texto extra que ultrapassa o tamanho do criptograma
        
        # chaveExtendida e Criptograma tem o mesmo tamanho
        
        # Converter chaveExtendida para lista de números (1 a 26)
        chaveNumerica = self.conversor_A1Z26(chaveExtendida)
        for index, char in enumerate(criptograma):
            pos_cifra = dicionarioA1Z26[char] - 1
            pos_key = chaveNumerica[index] - 1
            deslocamento = ((pos_cifra - pos_key) % 26) + 1
            mensagem += dicionarioA1Z26_invertido[deslocamento]

        # Colocar os espaços novamente no criptograma
        mensagemChars= iter(mensagem)
        mensagem = "".join(
            char if char == " " else next(mensagemChars)
            for char in criptogramaOriginal
        )
        return mensagem

    def checagem(self, resultados,criptogramaPT,criptogramaEN,senha1,senha2): #Assumindo valores fixos de senha para simplicidade
        if "senha" in resultados[0] and "password" in resultados[1]:
            print("O atacante encontrou ambas as senhas, aqui estão os textos decifrados:")
            print()
            print(self.decifrador("senha",criptogramaPT))
            print()
            print(self.decifrador("password",criptogramaEN))
            print()
        elif "senha" in resultados[0] or "password" in resultados[1]:
            if "senha" in resultados[0]:
                print("O atacante só foi capaz de encontrar a senha da mensagem 1, aqui está o texto decifrado:")
                print(self.decifrador("senha",criptogramaPT))
            else:
                print("O atacante só foi capaz de encontrar a senha da mensagem 2, aqui está o texto decifrado:")
                print(self.decifrador("password",criptogramaEN))
        else:
                print("O atacante não foi capaz de encontrar nenhuma das senhas")
    
        

### Debug:
vigenere = Vigenere()
atacante = Atacante()
cipherPT = "uyvkavs pvm g lbtee uhl fspn joe ef tagw"
cipherEN = "qeosns fi ihw ewb kkpt khasbv lilz dwj kpnvk"
mensagemPT = "Cuidado com o homem que fala com as mãos"
mensagemEN = "Beware of the man that speeks with his hands"
print()
print("Abaixo temos as mensagens cifradas e decifradas com a classe Vigenère (que assume que sabemos a chave)")
print()
print("Portugues:")
print(vigenere.cifrador("senha",mensagemPT))
print(vigenere.decifrador("senha",cipherPT))
print()
print("Inglês:")
print(vigenere.cifrador("password",mensagemEN))
print(vigenere.decifrador("password",cipherEN))

print()
print("Abaixo temos a mesma mensagem tentando ser decifrada com a classe Atacante (que tenta assumir qual a chave)")
print()


resultados = atacante.decifraMeOuTeDevoro(cipherPT,cipherEN)
atacante.checagem(resultados,cipherPT,cipherEN,"senha","password")


print()
print("Para mensagens muito curtas, a análise de frequência tende a falhar mizerávelmente, devido a falta de repetições no texto")
print()
print("Abaixo temos uma mensagem maior decifrada com a classe Atacante:")
print()
print("Primeiro, codificamos uma mensagem usando o vigenere")

with open("mensagemLongaEN.txt", "r", encoding="utf-8") as arquivoEN, open('mensagemLongaPT.txt', 'r') as arquivoPT:
    print()
    print("Temos então os seguinte ciphertext (PT-BR e ENG respectivamente):")
    print()

    arquivoPTtxt = " ".join(arquivoPT.read().split())
    arquivoENtxt = " ".join(arquivoEN.read().split())

    criptogramaPT = vigenere.cifrador("senha", arquivoPTtxt)
    criptogramaEN = vigenere.cifrador("password", arquivoENtxt)
    
    print(criptogramaEN)
    print("\n\n\n")
    print(criptogramaPT)
    print()
    print("Vamos ver como o atacante se sai:")
    print()

    resultados = atacante.decifraMeOuTeDevoro(criptogramaPT,criptogramaEN)
    print()

    atacante.checagem(resultados,criptogramaPT,criptogramaEN,"senha","password")

