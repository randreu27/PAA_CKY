class Gramatica_FNC:
    """
    Processa els textos en format igual a l'exemple "g1.txt" o "g2.txt". \n
    Es pot accedir a les regles donada una altra regla no terminal,
    per més informació consulta la descripcció del mètode get_rule().

    Regles de format:
        Terminals en minúscules.
        No terminals en majúscules.
        Els símbols han de tenir mida 1. Si en volguéssim tenir més per representar frases com a PLH,
        hauríem de separar els símbols d'alguna manera, que en general no hem fet a PAA. Per tant, hem decidit
        mantenir el format de classe (ex: S -> aSb).
    """
    def __init__(self, file):
        """
        Input: file (string) amb el nom del fitxer que conté la gramàtica
        """
        self.grammar = {}
        self.Σ = set()  # Símbols terminals
        self.N = set()  # Símbols no terminals
        with open(file) as f:
            for line in f:
                line = line.split()
                # el primer element és el símbol no terminal
                # el tercer (idx 2) és la primera producció i si n'hi ha més, apareixen cada dos (idx 4, 6, ...)
                left, right = line[0], line[2::2]
                for i in range(len(right)):
                    # Suposem que els símbols no terminals estan en majúscula
                    if right[i].isupper():
                        right[i] = tuple(right[i])
                        self.N.add(right[i][0])
                        self.N.add(right[i][1])
                    else:
                        self.Σ.add(right[i])
                self.grammar[left] = right
        assert 'S' in self.grammar, 'La gramàtica no té símbol inicial (ha de ser S)'
        # print('N:', self.N)
        # print('Σ:', self.Σ)
        # print('Grammar:', self.grammar)

    def get_rule(self, S):
        """
        Retorna una llista de Regles terminals i/o no terminals en forma d'string
        Exemple: [ 'a' , '(X, A)' , '(A, X)' , 'b' ], sent les paraules majúscules no terminals,
        i les minúscules terminals.
        """
        return self.grammar[S]

    def CKY_det(self, cadena: str):
        """
        Input: tira de caràcters (string)
        Output: True si la tira de caràcters pertany a la llengua de la gramàtica, False en cas contrari
        """
        # N: conjunt de no terminals
        # Σ: conjunt de terminals
        # grammar: regles de la gramàtica (llista de tuples (antecedent, precedent))
        # cadena: tira de caràcters
        pass

    def CKY_prob(self, cadena: str):
        """
        Input: tira de caràcters (string)
        Output: probabilitat que la tira de caràcters pertanyi a la llengua de la gramàtica
        """
        pass

    def CFG_a_CNF(self):
        """
        Transforma la gramàtica de CFG a CNF
        """
        pass


cnf_grammar = Gramatica_FNC('g1.txt')
print(cnf_grammar.get_rule('R'))
