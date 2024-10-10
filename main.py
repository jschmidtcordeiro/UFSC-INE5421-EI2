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


######################################################################
## Expressoes Regulares (ER) para Automato Finito Deterministico (AFD)
######################################################################




####################
## Uniao de dois AFD
####################




#########################
## Funcoes de Auxiliarres
#########################


def main():
    
    vpl_input = argv[1] # **Não remover essa linha**, ela é responsável por receber a string de entrada do VPL
    
    """ 
        Seu código para resolver o exercício e printar a saída. 
        Você pode fazer funções foras da main se preferir. 
        Essa é apenas uma sugestão de estruturação.
        [...]
    """

    input1 = "<(&|b)(ab)*(&|a)><&|b|a|bb*a>"
    input1_afds = "<3;{1,2,4,5};{{1,2,4,5},{3,5},{2,4,5}};{a,b};{1,2,4,5},a,{3,5};{1,2,4,5},b,{2,4,5};{3,5},b,{2,4,5};{2,4,5},a,{3,5}><4;{1,2,3,6};{{1,2,3,6},{6},{4,5,6}};{a,b};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}>"

    input2 = "<aa*(bb*aa*b)*><a(a|b)*a>"
    input2_afds = "<5;{1};{{2,3,8},{3,8}};{a,b};{1},a,{2,3,8};{2,3,8},a,{2,3,8};{2,3,8},b,{4,5};{4,5},a,{6,7};{4,5},b,{4,5};{6,7},a,{6,7};{6,7},b,{3,8};{3,8},b,{4,5}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input3 = "<a(a|b)*a><a(a|b)*a>"
    input3_afds = "<3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input4 = "<a(a*(bb*a)*)*|b(b*(aa*b)*)*><a(a|b)*a>"
    input4_afds = "<5;{1,6};{{2,3,11},{7,8,11}};{a,b};{1,6},a,{2,3,11};{1,6},b,{7,8,11};{2,3,11},a,{2,3,11};{2,3,11},b,{4,5};{7,8,11},a,{9,10};{7,8,11},b,{7,8,11};{4,5},a,{2,3,11};{4,5},b,{4,5};{9,10},a,{9,10};{9,10},b,{7,8,11}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"

    input5 = "<&|b|a|bb*a><a(a|b)*a>"
    input5_afds = "<4;{1,2,3,6};{{1,2,3,6},{6},{4,5,6}};{a,b};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}><3;{1};{{2,3,4,5}};{a,b};{1},a,{2,3,4};{2,3,4},a,{2,3,4,5};{2,3,4},b,{2,3,4};{2,3,4,5},a,{2,3,4,5};{2,3,4,5},b,{2,3,4}>"


if __name__ == "__main__":
    main()