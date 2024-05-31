from gramatica_fnc import Gramatica_FNC

def proves_internes():
        print("Proves de la Gramàtica 'g2.txt':")

        cnf_grammar = Gramatica_FNC('g2.txt')

        proves_g2 = ['a', 'aaa', 'aaaa', 'aaaab', 'aaaaaabbbbbb', 'ab', 'abb', 'abab', 'ababb', 'ababbaaa', 'abababab', 'bbbbbbbbb',
                     'bbbbbbbbba', 'bbb', 'bbbaa', 'bbbabbb']

        labels_g2 = [False, False, False, False, True, True, False, True, False, False, True, True, True, True, False, True]

        predicted_g2 = []
        for elem in proves_g2:
            predicted_g2.append(cnf_grammar.CKY_det(elem))

        if predicted_g2 == labels_g2:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

        print('\n')
        print('\n')
        print("Proves de la Gramàtica 'g2_prob.txt':")

        cnf_grammar = Gramatica_FNC('g2_prob.txt', pcky=True)

        proves_g2 = ['a', 'aaa', 'aaaa', 'aaaab', 'aaaaaabbbbbb', 'ab', 'abb', 'abab', 'ababb', 'ababbaaa', 'abababab', 'bbbbbbbbb',
                     'bbbbbbbbba', 'bbb', 'bbbaa', 'bbbabbb']

        labels_g2 = [False, False, False, False, True, True, False, True, False, False, True, True, True, True, False, True]

        predicted_g2 = []
        for elem in proves_g2:
            if cnf_grammar.CKY_prob(elem) > 0:
                predicted_g2.append(True)
            else:
                predicted_g2.append(False)

        if predicted_g2 == labels_g2:
            print("La gramàtica s'ha identificat corectament!")
        else:
            print("La gramàtica NO s'ha identificat corectament")

proves_internes()