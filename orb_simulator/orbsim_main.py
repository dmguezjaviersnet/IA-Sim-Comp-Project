from lexer.regex_grammar import regex_grammar
from parser.lr0_item import Lr0_item
from parser.lr1_item import Lr1_item
from parser.non_terminal import Non_terminal
from parser.terminal import Epsilon, Terminal
from orbsim_language.context import Scope
from lexer.regex_engine import Regex_Engine
from lexer import Lexer
from parser.own_token import Token_Type, Token
from automaton.state import State
from parser.lr1_parser import lr1_parse
from orbsim_language.orbsim_lexer import orbsim_lexer
from orbsim_language.orbsim_grammar import orbsim_grammar, orbsim_token_string
import random
from orbsim_language.type_collector import TypeCollector
from orbsim_language.type_builder import TypeBuilder
from orbsim_language.type_checker import TypeChecker
from orbsim_language.executor import Executor
from orbsim_ui import OrbisimUI
from orbsim_pygame import PygameHandler
from compile_and_execute import orbsim_compile_and_execute
# def test1():
#     regexengine = Regex_Engine('(a|b|c)?')
#     automaton = regexengine.automaton
#     automaton = State.from_old_model_to_new_model(automaton)
#     automaton = automaton.to_DFA()
#     print(automaton.match_from_dfa('aa'))
#     # assert automaton.match_from_dfa('bbb') == True
#     # assert automaton.match_from_dfa('') == True
#     # assert automaton.match_from_dfa('aaef') == False
    

# ('([a-z]|[A-Z]|[0-9]|\\! | \\@| \\# | \\$| \\%| \\^| \\&| \\*| \\( | \\) | \\~ | \\/  | \\- | \\+ )*', Token_Type.error)

def test_lexer():
    lex = Lexer([('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.mul),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('[0-9]+', Token_Type.int ),
    ('(\\ )+', Token_Type.space)],
     eof=Token_Type.eof)

    tokens = lex('aaaaaKoooo(3+5)*(4/(5-8) 124')
    
    # success, ast = lr1_parse(arth_grammar, tokens)
    
    for i in tokens:
        print(i)
    print(':)')
    

def debugging(handler: 'PygameHandler'):
    handler.generate_orbits(random.randint(1,1))
    # handler.generate_objects_in_orbits(random.randint(2,2))
    # handler.generate_random_collector()
    # handler.generate_orbits(random.randint(1,20))

    for i in range(20):
        handler.generate_new_random_space_debris()
    # handler.generate_objects_in_orbits(random.randint(1,1))
    # handler.generate_random_collector()
    # handler.start_pygame()

def main():
    
    ########### #################### Gramática de Regex #################################
    # re = Regex_Engine('(a|b)*')
    # test_lexer()
   
    pygame_handler = PygameHandler()
    
#     orbsim_compile_and_execute(
#     '''
#         show_orbits;
#     let Int counter = 0;
#     loop (counter < randint(2, 30) ){
#         counter = counter + 1;
#         let Orbit o1 = orbit;
#         o1.add_to_simulation();
#     };
    
#     counter = 0;
#     loop (counter < randint(2, 4) ){
#         counter = counter + 1;
#         let Satellite sat1 = satellite;
#         sat1.add_to_simulation();
#     };
    
#     counter = 0;
#     loop (counter < randint(2, 4) ){
#         counter = counter + 1;
#         let SpaceDebris sd1 = spacedebris;
#         sd1.add_to_simulation();
#     };
#     print(number_orbits());
#     print(number_satellites());
#     print(number_objects());
#     print(number_space_debris());
    
#     start;
# '''
# , pygame_handler)

# let Tuple size1 = tuple(10,10);
# let Tuple size2 = tuple(20,20);
# let Tuple rgb1 = tuple(randint(0,255), randint(0,255), randint(0,255));
# let Tuple rgb2 = tuple(randint(0,255), randint(0,255), randint(0,255));
# let SpaceDebris sp1 =  custom_space_debris(size1, rgb1);
# let SpaceDebris sp2 =  custom_space_debris(size2, rgb2);
# sp1.add_to_simulation();
# sp2.add_to_simulation();
# start;

#     ''', pygame_handler)
    ui = OrbisimUI(pygame_handler)
    
    # handler = Handler()
    # handler.start()
    # print(ui.code_text)
    # au = re.automaton
    # test_lexer()
    # test_lexer()
    
    # tokens = Regex_Engine.regexTokenizer('(a|b)*')
    # a1 = [t.token_type for t in tokens]
    # a2 = [t.lexeme for t in tokens]
    # print(a1)
    # print(a2)
    # for i in tokens:
    #     print(i)
    # test_lexer()
    # # print(parsed2)
    # # nfa = ast.eval()
    # # dfa = NFAtoDFA(nfa)
    # print(au.match('aaaaa'))
    # print(au.match('aaaaab'))
    # print(au.match(''))
    # print(au.match('ababbb'))
    # print(au.match('ababbb'))
    # print(dfa.match('abbbbed'))
    # print(dfa.match('aaed'))
    # print(dfa.match('ed'))
    # print(dfa.match('aaaaabbbbaaed'))
    # print(dfa.match('aaaaabbbba'))
    # print(dfa.match(''))

    # print('finished \n\n')
    # print(regex_grammar)
    # print(parsed2)
    # print(parsed)

    ############################### Probando parser LR(1) ##############################


    # Testeo Hashing
    # item1 = Lr1_item(Lr0_item(Non_terminal('P'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))
    # item2 = Lr1_item(Lr0_item(Non_terminal('E'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))

    # item3 = Lr1_item(Lr0_item(Non_terminal('P'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))
    # item4 = Lr1_item(Lr0_item(Non_terminal('E'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))

    # tup1 = (item1, item2)
    # tup2 = (item3, item4)

    # print(item1 == item2)
    # print(hash(item1) == hash(item3))

    # item1 = Lr1_item(Lr0_item(Non_terminal('E'), (Epsilon(), Non_terminal('X')), 0), frozenset({'$'}))
    # item2 = Lr1_item(Lr0_item(Non_terminal('P'), (Epsilon(), Non_terminal('X')), 0), frozenset({'$'}))
    # h1 = hash(item1)
    # h2 = hash(item2)
    

    # print(hash(tup1) == hash(tup2))
    # tokens, errs = orbsim_lexer(
    # ''' 
    #     let List a = [2+3, 1, 2];
    #     print(a);
    # '''
    # )
    
    # _, ast = lr1_parse(orbsim_grammar, tokens, orbsim_token_string)
    # print('\o/')
    # collector = TypeCollector()
    # collector.visit(ast)
    # builder = TypeBuilder(collector.context, collector.log)
    # builder.visit(ast)
    # checker =  TypeChecker(builder.context, builder.log)
    # checker.check(ast, Scope())
    # exe =  Executor(checker.context)
    # exe.execute(ast, Scope())
    # print('_o/ \o/  \o_')
    # a = (1, 2)
    # b = (2, 1)
    # print(hash(a) == hash(b))
    

if __name__ == '__main__':
    main()