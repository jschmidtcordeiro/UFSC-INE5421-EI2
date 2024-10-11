""" 
========= INSTRUÇÕES ========= 
    - Todo o código deve estar contido no arquivo main.py
    - O arquivo main.py deve conter uma função main que será chamada pelo VPL,
      essa função deve conter uma linha de código que recebe a string de entrada do VPL.
      Um exemplo de como isso pode ser feito está no arquivo main.py fornecido.
    - Você pode criar funções fora da main se preferir, mas se certifique de que a main chama essas funções.
    - Caso você prefira fazer o exercício em uma IDE e quiser testar o código localmente, 
    é só passar a string de entrada como argumento na hora de executar o código. 
        Exemplo: python3 main.py "<(&|b)(ab)*(&|a)><&|b|a|bb*a>"
"""

"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""

from sys import argv
import re

class Automato:
    def __init__(self, entrada=None):
        if entrada is not None:
            self.gerar_automato(entrada)
        else:
            self.num_estados = 0
            self.estado_inicial = None
            self.estados_finais = set()
            self.alfabeto = set()
            self.transicoes = set()
            self.estados = set()
            self.tabela_transicoes = {}
    
    def gerar_automato(self, entrada):
        informacoes = entrada.strip('<>').split(';')
        self.num_estados = informacoes[0]
        self.estado_inicial = informacoes[1]
        self.estados_finais = set("{"+s+"}" for s in informacoes[2].strip("{}").split("},{"))
        self.alfabeto = set(informacoes[3].strip('{}').split(','))
        self.transicoes = set(
            tuple(re.findall(r'\{[^}]*\}|[^,]+', transicao)) for transicao in informacoes[4:]
        )

        # Gerar set de estados para usar na tabela de transicoes
        self.estados = set()
        for transicao in self.transicoes:
            self.estados.add(transicao[0])
            self.estados.add(transicao[2])

        # Gerar tabela de transicoes
        self.tabela_transicoes = {
            estado: {simbolo: set() for simbolo in self.alfabeto}
            for estado in self.estados
        }
        for qi, a, qj in self.transicoes:
            self.tabela_transicoes[qi][a].add(qj)
    
    def adicionar_estado(self, estado):
        self.estados.add(estado)
        self.num_estados += 1
    
    def adicionar_transicao(self, qi, simbolo, qj):
        self.transicoes.add(tuple([qi,simbolo,qj]))
    
    def get_estado_inicial(self):
        return self.estado_inicial

    def get_estados_finais(self):
        return self.estados_finais
    
    def get_estados(self):
        return self.estados

    def get_alfabeto(self):
        return self.alfabeto
    
    def get_transicoes(self):
        return self.transicoes
    
    def set_alfabeto(self, alfabeto):
        self.alfabeto = alfabeto

    def set_estado_inicial(self, estado):
        self.estado_inicial = estado
    
    def set_estados_finais(self, estados_finais):
        self.estados_finais = estados_finais
    
    def set_tabela_transicoes(self, tabela):
        self.tabela_transicoes = tabela
    
######################################################################
## Expressoes Regulares (ER) para Automato Finito Deterministico (AFD)
######################################################################




####################
## Uniao de dois AFD
####################

def uniao_automatos(afd1, afd2):
    automato_uniao = Automato()
    
    # Definir estado inicial do novo automato
    automato_uniao.set_estado_inicial("{q0}")
    automato_uniao.adicionar_estado("{q0}")

    # Unir os alfabetos dos automatos para ser o alfabeto do novo automato
    alfabeto = set()
    alfabeto.update(afd1.get_alfabeto())
    alfabeto.update(afd2.get_alfabeto())
    automato_uniao.set_alfabeto(alfabeto)

    # Definir estados finais
    estados_finais = set()
    estados_finais.update(afd1.get_estados_finais())
    estados_finais.update(afd2.get_estados_finais())
    automato_uniao.set_estados_finais(estados_finais)

    # Adicionar estados dos automatos
    for estado in afd1.get_estados():
        if estado not in automato_uniao.get_estados():
            automato_uniao.adicionar_estado(estado)
    for estado in afd2.get_estados():
        if estado not in automato_uniao.get_estados():
            automato_uniao.adicionar_estado(estado)
    
    # Gerar tabela de transicoes vazia
    tabela_transicoes = {
        estado : {simbolo: set() for simbolo in automato_uniao.get_alfabeto()} 
        for estado in automato_uniao.get_estados()
    }

    # Adicionar transicoes dos automatos originais
    for (qi, simbolo, qj) in afd1.get_transicoes():
        tabela_transicoes[qi][simbolo].add(qj)
        automato_uniao.adicionar_transicao(qi, simbolo, qj)
    for (qi, simbolo, qj) in afd2.get_transicoes():
        tabela_transicoes[qi][simbolo].add(qj)
        automato_uniao.adicionar_transicao(qi, simbolo, qj)
    
    # Adicionar epsilon-transicoes do q0 para os estados iniciais originais
    tabela_transicoes['{q0}']['&'] = set()
    tabela_transicoes['{q0}']['&'].add(afd1.get_estado_inicial())
    tabela_transicoes['{q0}']['&'].add(afd2.get_estado_inicial())

    automato_uniao.adicionar_transicao('{q0}', '&', afd1.get_estado_inicial())
    automato_uniao.adicionar_transicao('{q0}', '&', afd2.get_estado_inicial())

    automato_uniao.set_tabela_transicoes(tabela_transicoes)

    return automato_uniao


#########################
## Funcoes de Auxiliarres
#########################

def print_automato_uniao(automato_uniao):
    pass



def main():
    
    #vpl_input = argv[1] # **Não remover essa linha**, ela é responsável por receber a string de entrada do VPL
    
    """ 
        Seu código para resolver o exercício e printar a saída. 
        Você pode fazer funções foras da main se preferir. 
        Essa é apenas uma sugestão de estruturação.
        [...]
    """

    input1 = "<(&|b)(ab)*(&|a)><&|b|a|bb*a>"
    input1_afd1 = "<3;{1,2,4,5};{{1,2,4,5},{3,5},{2,4,5}};{a,b};{1,2,4,5},a,{3,5};{1,2,4,5},b,{2,4,5};{3,5},b,{2,4,5};{2,4,5},a,{3,5}>" 
    input1_afd2 = "<4;{1,2,3,6};{{1,2,3,6},{6},{4,5,6}};{a,b};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}>"

    input2 = "<aa*(bb*aa*b)*><a(a|b)*a>"
    input2_afds = "<5;{1};{{2,3,8},{3,8}};{a,b};{1},a,{2,3,8};{2,3,8},a,{2,3,8};{2,3,8},b,{4,5};{4,5},a,{6,7};{4,5},b,{4,5};{6,7},a,{6,7};{6,7},b,{3,8};{3,8},b,{4,5}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input3 = "<a(a|b)*a><a(a|b)*a>"
    input3_afds = "<3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input4 = "<a(a*(bb*a)*)*|b(b*(aa*b)*)*><a(a|b)*a>"
    input4_afds = "<5;{1,6};{{2,3,11},{7,8,11}};{a,b};{1,6},a,{2,3,11};{1,6},b,{7,8,11};{2,3,11},a,{2,3,11};{2,3,11},b,{4,5};{7,8,11},a,{9,10};{7,8,11},b,{7,8,11};{4,5},a,{2,3,11};{4,5},b,{4,5};{9,10},a,{9,10};{9,10},b,{7,8,11}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input5 = "<&|b|a|bb*a><a(a|b)*a>"
    input5_afds = "<4;{1,2,3,6};{{1,2,3,6},{6},{4,5,6}};{a,b};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    afd1 = Automato(input1_afd1)
    afd2 = Automato(input1_afd2)

    automato_uniao = uniao_automatos(afd1, afd2)
    print()

    # output = <7;{q0};{{{1,2,4,5}},{{3,5}},{{2,4,5}},{{1,2,3,6}},{{6}},{{4,5,6}}};{a,b};{q0},&,{{1,2,4,5}};{q0},&,{{1,2,3,6}};{1,2,4,5},a,{3,5};{1,2,4,5},b,{2,4,5};{3,5},b,{2,4,5};{2,4,5},a,{3,5};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}>

if __name__ == "__main__":
    main()