# 1º Relatóio: Etapa AI-a (Analisador Léxico e Sintático)

1. Qual é o nome do relator?

    > MATHEUS ANDRADE NAVARRO DE OLIVEIRA 

2. A etapa foi completamente ou parcialmente concluída?

    > Parcialmente

3. No caso de parcialmente concluída, o que não foi concluído?

    > Não conseguimos rodar os testes localmente e estava dando erro no CI do github, dessa forma ficou inconclusivo o programa

4. O programa passa nos testes automatizados?
    
    > Não

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Foi encontrado 5 falhas e 1 erro pelo teste: https://github.com/CC20221/PyMJCG15/runs/6062859585?check_suite_focus=true.
    
    1. ```
       FAIL: test_number_of_dot (test_lexer.LexerTest)
       ----------------------------------------------------------------------
       Traceback (most recent call last):
         File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_lexer.py", line 224, in test_number_of_dot
           self.assertEqual(actual, expected)
       AssertionError: 53 != 15
       ```
    2. ```
       FAIL: test_number_of_id (test_lexer.LexerTest)
       ----------------------------------------------------------------------
       Traceback (most recent call last):
        File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_lexer.py", line 56, in test_number_of_id
         self.assertEqual(actual, expected)
       AssertionError: 197 != 140
       ```
    3. ```
       FAIL: test_number_of_minus (test_lexer.LexerTest)
       ----------------------------------------------------------------------
       Traceback (most recent call last):
       File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_lexer.py", line 212, in test_number_of_minus
        self.assertEqual(actual, expected)
       AssertionError: 1 != 0
       ```
    4. ```
       FAIL: test_number_of_print (test_lexer.LexerTest)
       ----------------------------------------------------------------------
       Traceback (most recent call last):
       File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_lexer.py", line 62, in test_number_of_print
        self.assertEqual(actual, expected)
       AssertionError: 0 != 19
       ```
    5. ```
       FAIL: test_number_of_tokens (test_lexer.LexerTest)
       ----------------------------------------------------------------------
       Traceback (most recent call last):
       File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_lexer.py", line 50, in test_number_of_tokens
        self.assertEqual(actual, expected)
       AssertionError: 725 != 649
       ```
    6. ```
       ERROR: test_parser (unittest.loader._FailedTest)
       ----------------------------------------------------------------------
       ImportError: Failed to import test module: test_parser
       Traceback (most recent call last):
         File "/opt/hostedtoolcache/Python/3.10.0/x64/lib/python3.10/unittest/loader.py", line 436, in _find_test_path
           module = self._get_module_from_name(name)
         File "/opt/hostedtoolcache/Python/3.10.0/x64/lib/python3.10/unittest/loader.py", line 377, in _get_module_from_name
           __import__(name)
         File "/home/runner/work/PyMJCG15/PyMJCG15/tests/test_parser.py", line 6, in <module>
           from pymjc.front.parser import MJParser
         File "/home/runner/work/PyMJCG15/PyMJCG15/pymjc/front/parser.py", line 4, in <module>
           class MJParser(Parser):
         File "/home/runner/work/PyMJCG15/PyMJCG15/.venv/lib/python3.10/site-packages/sly/yacc.py", line 1774, in __new__
           cls._build(list(attributes.items()))
         File "/home/runner/work/PyMJCG15/PyMJCG15/.venv/lib/python3.10/site-packages/sly/yacc.py", line 1968, in _build
           cls.__build_grammar(rules)
         File "/home/runner/work/PyMJCG15/PyMJCG15/.venv/lib/python3.10/site-packages/sly/yacc.py", line 1914, in __build_grammar
           raise YaccError('Unable to build grammar.\n'+errors)
       sly.yacc.YaccError: Unable to build grammar.
       ```

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Problemas relacionados aos testes

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Matheus foi o principal responsável pelo lexer e o Luan e Vinicius foram os principais responsáveis pelo parser


# 2º Relatóio: Etapa AI-b (Árvores Sintática Abstrata e Análise Semântica)

1. Qual é o nome do relator?

    > Luan Carvalho

2. A etapa foi completamente ou parcialmente concluída?

    > Completamente (O erro que está dando, acredito que seja na implementacao do Professor)

3. No caso de parcialmente concluída, o que não foi concluído?

    > Erro no test_semantic.SemanticTest

4. O programa passa nos testes automatizados?
    
    > Passa completamente no parser, mas nao passa no erro do teste semantico: 

Parser debugging for MJParser written to parser.out

======================================================================
ERROR: setUpClass (test_semantic.SemanticTest)

   Traceback (most recent call last):
     File "/home/lcarvalho/Documents/PyMJC-15/tests/test_semantic.py", line 52, in setUpClass
       symbol_table_creator.visit_program(program)
     File "/home/lcarvalho/Documents/PyMJC-15/pymjc/front/visitor.py", line 630, in visit_program
       value.accept(self)
   AttributeError: 'NoneType' object has no attribute 'accept'
   
   
   Ran 46 tests in 0.080s


5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Nao

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Erros dos testes durante a execucao e lentidao da equipe no entendimento do código.

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Luan responsável completamente pelos ajustes no parser para a AST e trabalho conjunto nos vistors com supervisão minha

# 3º Relatóio: Etapa AI-c (Tradução para o Código Intermediário)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui


# 4º Relatóio: Etapa AI-d (Seleção de Instruções)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui


# 5º Relatóio: Etapa AI-e (Alocação de Registradores)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui


# 6º Relatóio: Etapa AI-f (Integração e Geração do Código Final)

1. Qual é o nome do relator?

    > Escreva sua resposta aqui

2. A etapa foi completamente ou parcialmente concluída?

    > Escreva sua resposta aqui

3. No caso de parcialmente concluída, o que não foi concluído?

    > Escreva sua resposta aqui

4. O programa passa nos testes automatizados?
    
    > Escreva sua resposta aqui

5. Algum erro de execução foi encontrado para alguma das entradas? Quais?
    
    > Escreva sua resposta aqui

6. Quais as dificuldades encontradas para realização da etapa do projeto?
    
    > Escreva sua resposta aqui

7. Qual a participação de cada membro da equipe na etapa de execução?
    
    > Escreva sua resposta aqui