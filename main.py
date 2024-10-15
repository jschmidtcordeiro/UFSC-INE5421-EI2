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

class Node:
    def __init__(self, value, left=None, right=None, node_id=None):
        self.value = value  # Stores the operation or symbol
        self.left = left    # Left child
        self.right = right  # Right child
        self.id = node_id   # Unique identifier for the node
        self.nullable = False  # Indicates if the node can derive the empty string
        self.firstpos = set()  # Set of first positions
        self.lastpos = set()   # Set of last positions

    def __repr__(self, level=0, prefix="Root: "):
        result = "\t" * level + prefix + repr(self.value) + f" (ID: {self.id})\n"
        if self.left:
            result += self.left.__repr__(level + 1, "L--- ")
        if self.right:
            result += self.right.__repr__(level + 1, "R--- ")
        return result

    def calculate_followpos(self):
        followpos = {}
        self._calculate_followpos_recursive(followpos)
        return followpos

    def _calculate_followpos_recursive(self, followpos):
        if self.left:
            self.left._calculate_followpos_recursive(followpos)
        if self.right:
            self.right._calculate_followpos_recursive(followpos)

        if self.value == '.':
            # Concatenation: add lastpos of left to firstpos of right
            for pos in self.left.lastpos:
                if pos not in followpos:
                    followpos[pos] = set()
                followpos[pos].update(self.right.firstpos)
        elif self.value == '*':
            # Star operation: add lastpos to firstpos
            for pos in self.lastpos:
                if pos not in followpos:
                    followpos[pos] = set()
                followpos[pos].update(self.firstpos)

    def get_max_node_id(self):
        max_id = self.id if self.id is not None else 0  # Start with current node's id
        if self.left:
            max_id = max(max_id, self.left.get_max_node_id())  # Check left child
        if self.right:
            max_id = max(max_id, self.right.get_max_node_id())  # Check right child
        return max_id  # Return the maximum id found


def parse_regex(expr):
    def parse_expression(i, node_id=0):
        nodes = []
        while i < len(expr):
            if expr[i] == '(':
                # Parse a subexpression
                subexpr, i = parse_expression(i + 1, node_id)
                nodes.append(subexpr)
            elif expr[i] == ')':
                # End of a subexpression
                break
            elif expr[i] == '*':
                # Apply star operation to the last node
                last_node = nodes.pop()
                node = Node('*', left=last_node)
                node.nullable = True
                node.firstpos = last_node.firstpos
                node.lastpos = last_node.lastpos
                nodes.append(node)
            elif expr[i] == '|':
                # Union operation (needs two children)
                left = Node('|', left=nodes.pop())
                subexpr, i = parse_expression(i + 1, node_id)
                left.right = subexpr
                left.nullable = left.left.nullable or left.right.nullable
                left.firstpos = left.left.firstpos.union(left.right.firstpos)
                left.lastpos = left.left.lastpos.union(left.right.lastpos)
                nodes.append(left)
            elif expr[i] == '&':
                # Append symbol (concatenation handled later)
                node = Node(expr[i])
                node.nullable = True
                node.firstpos = set()
                node.lastpos = set()
                nodes.append(node)
            else:
                # Append symbol (concatenation handled later)
                node_id += 1
                node = Node(expr[i], node_id=node_id)
                node.nullable = False
                node.firstpos = {node_id}
                node.lastpos = {node_id}
                nodes.append(node)
            i += 1
        
        # Now handle concatenation
        while len(nodes) > 1:
            left = nodes.pop(0)
            right = nodes.pop(0)
            concat_node = Node('.', left, right)
            # Update nullable, firstpos, lastpos for concatenation
            concat_node.nullable = left.nullable and right.nullable
            concat_node.firstpos = left.firstpos.union(right.firstpos) if left.nullable else left.firstpos
            concat_node.lastpos = right.lastpos.union(left.lastpos) if right.nullable else right.lastpos
            nodes.insert(0, concat_node)
        
        return nodes[0], i



    root, _ = parse_expression(0)
    return root

def calculate_followpos(root):
    # Calculate followpos
    followpos = root.calculate_followpos()
        
    # Add # to followpos of the last positions
    node_id = root.get_max_node_id() + 1
    for pos in root.lastpos:
        if pos not in followpos:
            followpos[pos] = set()
        followpos[pos].add(node_id)
    print("Followpos:", followpos)
    return followpos

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

def gerar_automato_from_followpos(tree, followpos):
    automato = Automato()
    alfabeto = set()
    node_id_alfabeto = dict()
    def traverse(node):
        if node:
            if node.value not in {'|', '.', '*', '&'}:
                alfabeto.add(node.value)
                node_id_alfabeto[node.id] = node.value
            traverse(node.left)
            traverse(node.right)
    traverse(tree)
    automato.set_alfabeto(alfabeto)

    # Adicionar o estado final especial '#'
    estado_final = tree.get_max_node_id() + 1
    
    # O estado inicial 
    if tree.nullable:
        estado_inicial = frozenset(tree.firstpos).union({estado_final})
    else:
        estado_inicial = frozenset(tree.firstpos)
    print(estado_inicial)
    estados = [estado_inicial]
    estados_nao_marcados = [estado_inicial]
    
    # Mapeamento de conjuntos de estados para IDs únicos
    estado_para_id = {estado_inicial: 1}
    proximo_id = 2

    ## Ate aqui esta certo
    ## Falta somente adicionar as informacoes no automato com a formatacao correta

    while estados_nao_marcados:
        estado_atual = estados_nao_marcados.pop(0)
        for simbolo in alfabeto:
            proximo_estado = frozenset()
            for pos in estado_atual:
                if pos != estado_final and node_id_alfabeto[pos] == simbolo:
                    proximo_estado |= followpos.get(pos, set())
            
            if proximo_estado:
                if proximo_estado not in estados:
                    estados.append(proximo_estado)
                    estados_nao_marcados.append(proximo_estado)
                    estado_para_id[proximo_estado] = proximo_id
                    proximo_id += 1
                
                automato.adicionar_transicao(
                    f"{estado_atual}",
                    simbolo,
                    f"{proximo_estado}"
                )

    # Definir estado inicial e estados finais
    automato.set_estado_inicial(estado_inicial)
    estados_finais = {f"{estado}" for estado in estados if estado_final in estado}
    automato.set_estados_finais(estados_finais)

    return automato

def main():
    
    #vpl_input = argv[1] # **Não remover essa linha**, ela é responsável por receber a string de entrada do VPL
    
    """ 
        Seu código para resolver o exercício e printar a saída. 
        Você pode fazer funções foras da main se preferir. 
        Essa é apenas uma sugestão de estruturação.
        [...]
    """

    # Test the code with a regular expression
    regex = "aa*((b|b*)aa*b)*"
    regex = "aa*"
    regex = "&|b|a|bb*a"
    regex = "&|a|bb*"
    tree = parse_regex(regex)
    print(tree)
    followpos = calculate_followpos(tree)

    # Gerar automato a partir do followpos
    automato = gerar_automato_from_followpos(tree, followpos)





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