from gramatica_fnc import Gramatica_FNC

def proves_internes():
        print("Proves de la Gramàtica 'g1.txt':")

        cnf_grammar = Gramatica_FNC('g1.txt')

        proves_g1 = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaaa', 'b', 'bb', 'bbb', 'bbbb',
             'bbbbb', 'ab', 'aab', 'aaab', 'aaaab', 'aaaaaab', 'abab', 'aba', 'abaa',
             'abaaa', 'abaab', 'bbbaaa', 'aabaaaa']

        labels_g1 = [True, False, False, True, False, True, True, False, False, False, False, False,
                    False, True, False, True, False, False, True, False, False, False, True]

        predicted_g1 = []
        for elem in proves_g1:
            predicted_g1.append(cnf_grammar.CKY_det(elem))

        if predicted_g1 == labels_g1:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g1_prob.txt':")

        cnf_grammar = Gramatica_FNC('g1_prob.txt', pcky=True)

        proves_g1 = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaaa', 'b', 'bb', 'bbb', 'bbbb',
                    'bbbbb', 'ab', 'aab', 'aaab', 'aaaab', 'aaaaaab', 'abab', 'aba', 'abaa',
                    'abaaa', 'abaab', 'bbbaaa', 'aabaaaa']

        labels_g1 = [True, False, False, True, False, True, True, False, False, False, False, False,
                            False, True, False, True, False, False, True, False, False, False, True]

        predicted_g1 = []
        for elem in proves_g1:
            if cnf_grammar.CKY_prob(elem) > 0:
                predicted_g1.append(True)
            else:
                predicted_g1.append(False)

        if predicted_g1 == labels_g1:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g3.txt':")
        cnf_grammar = Gramatica_FNC('g3.txt', to_fnc=True)

        proves_g3 = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaaa', 'b', 'bb', 'bbb', 'bbbb',
                    'bbbbb', 'ab', 'aab', 'aaab', 'aaaab', 'aaaaaab', 'abab', 'aba', 'abaa',
                    'abaaa', 'abaab', 'bbbaaa', 'aabaaaa']

        labels_g3 = [False, False, False, False, False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False, False, False, False]

        predicted_g3 = []
        for elem in proves_g3:
            predicted_g3.append(cnf_grammar.CKY_det(elem))

        if predicted_g3 == labels_g3:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g3_prob.txt':")

        cnf_grammar = Gramatica_FNC('g3_prob.txt', to_fnc=True, pcky=True)

        proves_g3 = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaaa', 'b', 'bb', 'bbb', 'bbbb',
                    'bbbbb', 'ab', 'aab', 'aaab', 'aaaab', 'aaaaaab', 'abab', 'aba', 'abaa',
                    'abaaa', 'abaab', 'bbbaaa', 'aabaaaa']

        labels_g3 = [False, False, False, False, False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False, False, False, False]

        predicted_g3 = []
        for elem in proves_g3:
            if cnf_grammar.CKY_prob(elem) > 0:
                predicted_g3.append(True)
            else:
                predicted_g3.append(False)

        if predicted_g3 == labels_g3:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g4.txt':")
        cnf_grammar = Gramatica_FNC('g4.txt', to_fnc=True)

        proves_g4 = ['aaa','bbb', 'aba', 'aababaa', 'aaaaaa', 'baba', 'bbbbbabbbbb', 'a', 'b']

        labels_g4 = [True, True, True, True, False, False, True, True, True]

        predicted_g4 = []
        for elem in proves_g4:
            predicted_g4.append(cnf_grammar.CKY_det(elem))

        if predicted_g4 == labels_g4:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g4_prob.txt':")

        cnf_grammar = Gramatica_FNC('g4_prob.txt', to_fnc=True, pcky=True)

        proves_g4 = ['aaa','bbb', 'aba', 'aababaa', 'aaaaaa', 'baba', 'bbbbbabbbbb', 'a', 'b']

        labels_g4 = [True, True, True, True, False, False, True, True, True]

        predicted_g4 = []
        for elem in proves_g4:
            if cnf_grammar.CKY_prob(elem) > 0:
                predicted_g4.append(True)
            else:
                predicted_g4.append(False)

        if predicted_g4 == labels_g4:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print(predicted_g4)
        print(cnf_grammar.probabilities)

proves_internes()