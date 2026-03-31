from typing import Union
from unidecode import unidecode
"""
Parte I: cifrador/decifrador
O cifrador recebe uma senha e uma mensagem que é cifrada segundo a cifra de Vigenère,
gerando um criptograma, enquanto o decifrador recebe uma senha e um criptograma que
é decifrado segundo a cifra de Vigenère, recuperando uma mensagem. Os primeiros
usuários da cifra de Vigenère utilizavam um “quadrado de Vigenère” (como mostrado na
Figura 1) para descobrir rapidamente qual letra do texto cifrado usar, dado um texto 
plano e fluxo de teclas específicos.
"""

"""
Funcionamento do Vigenère:
- Assuma uma "senha" e uma "mensagem"
- Repita a senha em padrão cíclico até que ela seja do tamanho da mensagem
- Converta cada letra da senha para um número de 1 a 26 usando A1Z26
- Para encriptar: Para cada index da string de palavras (excluindo "espaço"), 
  desloque o caractere para a direita do alfabeto o exato número de vezes determinado 
  pelo index da chave
- Para decriptar: Faça o exato mesmo com o ciphertext, mas desloque para a esquerda
"""

class Vigenere:
    def __init__(self):
        self.dicionarioA1Z26 = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
        self.dicionarioA1Z26_invertido = {value: key for key, value in self.dicionarioA1Z26.items()}
        
    def conversor_A1Z26(self, senha: str) -> Union[list[int],int]:
        if len(senha) > 1:
            listaNumerica = []
            for caractere in senha:
                listaNumerica.append(self.dicionarioA1Z26[caractere])
            return listaNumerica
        else:
            return self.dicionarioA1Z26[caractere]
        pass    

    def cifrador(self, senha, mensagem):
        criptograma = ''
        mensagem = mensagem.lower()
        mensagemOriginal = mensagem #armazenar os indexes de espaços para depois
        mensagem = mensagem.replace(" ", "")
        mensagem = unidecode(mensagem)
        tamanho = len(mensagem)  
        senhaExtendida = (senha * (tamanho // len(senha) + 1)) [:tamanho] #Repete a senha tamanho vezes e remove o texto extra que ultrapassa o tamanho da mensagem
        
        # SenhaExtendida e Mensagem tem o mesmo tamanho
        
        # Converter senhaExtendida para lista de números (1 a 26)
        senhaNumerica = self.conversor_A1Z26(senhaExtendida)
        for index, char in enumerate(mensagem):
            deslocamento = senhaNumerica[index] + self.dicionarioA1Z26[char] - 1
            while deslocamento > 26: deslocamento -= 26
            criptograma += self.dicionarioA1Z26_invertido[deslocamento]
            
        # Colocar os espaços novamente no criptograma
        criptogramaChars= iter(criptograma)
        criptograma = "".join(
            char if char == " " else next(criptogramaChars)
            for char in mensagemOriginal
        )

        return criptograma


    def decifrador(self, senha, criptograma):
        mensagem = ''
        criptograma = criptograma.lower()
        criptogramaOriginal = criptograma #armazenar os indexes de espaços para depois
        criptograma = criptograma.replace(" ", "")
        criptograma = unidecode(criptograma)
        tamanho = len(criptograma)  
        senhaExtendida = (senha * (tamanho // len(senha) + 1)) [:tamanho] #Repete a senha tamanho vezes e remove o texto extra que ultrapassa o tamanho do criptograma
        
        # SenhaExtendida e Criptograma tem o mesmo tamanho
        
        # Converter senhaExtendida para lista de números (1 a 26)
        senhaNumerica = self.conversor_A1Z26(senhaExtendida)
        for index, char in enumerate(criptograma):
            deslocamento = self.dicionarioA1Z26[char] - senhaNumerica[index] + 1
            while deslocamento < 1: deslocamento += 26
            mensagem += self.dicionarioA1Z26_invertido[deslocamento]

        # Colocar os espaços novamente no criptograma
        mensagemChars= iter(mensagem)
        mensagem = "".join(
            char if char == " " else next(mensagemChars)
            for char in criptogramaOriginal
        )

        return mensagem

### Debug:
vigenere = Vigenere()
print(vigenere.cifrador("senha","Cuidado com o homem que fala com as mãos"))
print(vigenere.decifrador("senha","uyvkavs pvm g lbtee uhl fspn joe ef tagw"))


"""
Parte II: ataque de recuperação de senha por análise de frequência
Serão fornecidas duas mensagens cifradas (uma em português e outra em inglês)
com senhas diferentes. Cada uma das mensagens deve ser utilizada para 
recuperar a senha geradora do keystream usado na cifração e então decifradas.
Para as frequências das letras use: 
https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras

"""

def atacante(mensagem1, mensagem2):
    pass
    # Mensagem 1 é gerada pela senha 1
    # Mensagem 2 é gerada pela senha 2
    # para encontrar as senhas
    