# UFSC-INE5421-EI2
Trabalho 2 - INE5421: Linguagens Formais e Compiladores

# Descrição da Atividade
Nesta atividade, você deverá implementar um programa em Python para transformar expressões regulares (ER) em autômatos finitos determinísticos (AFD) e realizar a união de dois autômatos finitos. A tarefa consiste em converter duas ERs em seus respectivos AFDs e, posteriormente, unir esses AFDs em um único autômato.

# Formato de Entrada
A entrada do programa será uma string que representa duas expressões regulares separadas por um ">" e no seguinte formato:
<expressão regular 1><expressão regular 2>

# Formato de Saída
A saída do programa deve ser uma string no seguinte formato:
<AFD 1><AFD 2><União dos AFDs>

Cada autômato deve ser representado no formato especificado abaixo (o mesmo formato usado nas outras atividades):
<número de estados>;<estados finais>;{<conjunto de estados>};{<alfabeto>};<transições>

Cada parte da string de entrada é descrita a seguir:
<número de estados>: Um inteiro representando a quantidade de estados do autômato.
<estado inicial>: O estado inicial do autômato. Ex.: {A} ou {AD}
{<estados finais>}: Um conjunto de estados finais. Ex.: {{A}} ou {{AD}} ou {{A},{AD},...}
{<alfabeto>}: Um conjunto de símbolos do alfabeto. Ex.: {a} ou {a,b} ou {0,1,2}
<transições>: Conjunto de transições no formato {estado de origem},{símbolo},{estado de destino}.Ex.:  {A},a,{AB};

# Exemplo de Entrada e Saída
Entrada:
<(&|b)(ab)*(&|a)><&|b|a|bb*a>

Saída:
<3;{1,2,4,5};{{1,2,4,5},{3,5},{2,4,5}};{a,b};{1,2,4,5},a,{3,5};{1,2,4,5},b,{2,4,5};{3,5},b,{2,4,5};{2,4,5},a,{3,5}>

<4;{1,2,3,6};{{1,2,3,6},{6},{4,5,6}};{a,b};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}>

<7;{q0};{{{1,2,4,5}},{{3,5}},{{2,4,5}},{{1,2,3,6}},{{6}},{{4,5,6}}};{a,b};{q0},&,{{1,2,4,5}};{q0},&,{{1,2,3,6}};{1,2,4,5},a,{3,5};{1,2,4,5},b,{2,4,5};{3,5},b,{2,4,5};{2,4,5},a,{3,5};{1,2,3,6},a,{6};{1,2,3,6},b,{4,5,6};{4,5,6},a,{6};{4,5,6},b,{4,5};{4,5},a,{6};{4,5},b,{4,5}>

# Instruções
Arquivo Principal: Todo o código deve estar presente no arquivo main.py, que será fornecido a você. Certifique-se de que todas as funções e lógica necessárias para realizar a determinização e minimização estejam contidas neste arquivo. Junto ao arquivo principal tem uma estrutura recomendada para a função main.

# Formato da Saída
Mantenha a saída no formato especificado, mas não se preocupe com a ordem dos elementos dentro dos conjuntos { }. Por exemplo, {a,b,c} é equivalente a {b,c,a}. No entanto, a ordem dos elementos dentro de cada transição deve ser preservada, pois qualquer mudança na ordem dos elementos dentro de uma transição altera o significado do estado de origem, símbolo e estado de destino. Entretanto, a ordem em que cada transição aparece é irrelevante, contanto que todas apareçam na saída. Transições para estados mortos devem ser omitidas.

# Observações
Novo Estado na União: Ao realizar a união dos dois AFDs, o novo estado criado deve ser nomeado como q0 por padrão.

# Observações
Colaborações devem ser devidamente mencionadas e o código deve refletir o esforço individual de cada aluno.

Os nomes dos alunos são:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)

