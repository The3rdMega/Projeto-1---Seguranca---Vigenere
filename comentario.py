
        # Ciphertext 1 é gerado pela chave 1
        # Ciphertext 2 é gerado pela chave 2
        # Ciphertext 1 é gerado por uma mensagem em português
        # Ciphertext 1 é gerado por uma mensagem em inglês
        # Objetivo: Encontrar as chaves
        # Método: Análise de Frequência
        # Usar como base "https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras"

        # Para simplicidade, esse atacante utilizará apenas a frequência geral das letras em palavras,
        # sem levar em consideração a posição da letra na palavra ou frase

"""
        Passo a Passo da quebra da Cifra de Vigenère de acordo com Charles Babbage:
        1. Primeiro, tentamos encontrar o >> tamanho << da chave:
            - Exame de Kasiski:
                - Encontre padrões de 3 letras repetidos no ciphertext e veja a distância entre as duas instâncias
                - Marque esta distância como possível tamanho da chave ou múltiplo do tamanho da chave
                - O número de espaçamento com mais ocorrências tem mais chance de ser o tamanho da chave
            - Escolhendo um tamanho da chave "chute", separar o ciphertext em "streams" de trechos do tamanho escolhido
            - Em teoria, cada "stream" foi criptografado pela mesma letra da chave
        2. Teste de deslocamento (descobrir os caracteres da chave):
            - A ideia é simples. Se o tamanho esperado é "9" e a chave é "blueberry",
            toda letra do 1º stream foi encriptado pela letra "b" da chave e logo foi deslocado 2 para a direita
            - Mas não sabemos a chave, então assumimos chave "#########" e comparamos a frequência de letras em um stream
            com a frequência de letras do alfabeto alvo, calculando o erro entre cada comparação em 26 comparações de frequência
            - O menor erro médio tem a maior chance de ser o mapeamento correto 

            - Dado um tamanho escolhido da chave e os grupos de ciphertext, realizar teste Qui-Quadrado
            - a Fórmula: x^2=sum{(O_i-E_i)^2/E_i} -> usamos para testar todos os i=(0,...,26) possíveis deslocamentos
            e pegamos o de maior semelhança
                - O_i: É a frequência observada da letra no subtexto cifrado.
                - E_i: É a frequência esperada daquela letra na língua (baseada na tabela de porcentagens da língua dada pela professora).
            - O menor valor de X^2 é estatisticamente a mais provável letra da chave naquela posição (coluna da stream)
            - Ou seja, repetimos a fórmula para cada stream e posição da chave correspondente
"""

"""
        Ok, passo a passo da implementação:
            1. Criar uma função auxiliar "kasiski()" que recebe um ciphertext e retorna uma lista ordenada de tamanhos de chave possíveis
            do mais provável para o menos provável:
                - Para fazer isso, assumir como ordem a distância entre termos de 3 letras iguais mais frequente
            2. Criar uma função auxiliar "criarStreams()" que recebe o ciphertext e um valor inteiro "m" e separa o 
            ciphertext em listas de chars de tamanho m (o ciphertext não deve conter espaços e devemos restaurá-los depois)
            (não devemos nos preucupar com acentuação, pois estamos assumindo que o ciphertext não codifica acentuação)
            3. Criar uma função auxiliar "frequencia()" que recebe uma stream e retorna um dicionário(26 chaves) da frequência de cada letra
            4. Criar uma função auxiliar "mapeamento()" que recebe uma stream que aplica a função Qui-Quadrado na stream / alfabeto em todas as
            possíveis permutações da stream, retornando o menor valor obtido pela função após as 26 permutações
"""