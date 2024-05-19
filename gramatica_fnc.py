import re

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
                # expressió regular filtra -> i |, strip() elimina espais
                line = re.split(r"\s*->\s*|\s*\|\s*", line.strip())
                self.grammar[line[0]] = line[1:]
                for i in line:
                    for j in i:
                        # Si és majúscula, el símbol és no terminal. Si és minúscula, és terminal
                        if j.isupper():
                            self.N.add(j)
                        else:
                            self.Σ.add(j)
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

    def get_N(self):
        # Retorna els símbols no-terminals (en majúscula) de la gramàtica
        return self.N

    def get_Σ(self):
        # Retorna els símbols terminals (en minúscula) de la gramàtica
        return self.Σ

    def CKY_det(self, cadena: str):
        """
        Input: tira de caràcters (string)
        Output: True si la tira de caràcters pertany a la llengua de la gramàtica, False en cas contrari
        """
        n = len(cadena)
        if n == 0:
            # la paraula buida només es pot generar en un CFG en FNC si es genera per l'element d'entrada (S)
            return 'S' in self.grammar and '' in self.grammar['S']

        # Creem la taula triangular superior per el CKY
        table = [[set() for _ in range(n - i)] for i in range(n)]

        # Omplim la taula (diagonal)
        for i in range(n):
            for nt in self.grammar:
                for elem in self.grammar[nt]:
                    if elem == cadena[i]:
                        table[i][0].add(nt)

        # Apliquem l'algorisme CKY
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for k in range(1, length):
                    j = length - 1  # La longitud del segment actual
                    for nt in self.grammar:
                        for elem in self.grammar[nt]:
                            if len(elem) == 2:
                                B, C = elem
                                if B in table[i][k - 1] and C in table[i + k][j - k]:
                                    table[i][j].add(nt)
        print(cadena)
        self.print_table(table)
        return 'S' in table[0][n - 1]

    def print_table(self, table):
        """
        Imprimeix la taula CKY en format ASCII ben formatejada.
        """
        n = len(table)
        # Per a cada nou element, afegim 3 espais ("X, " ocupa 3 caràcters)
        mida_tab = max(len(elem) for subllista in table for elem in subllista) * 3

        for i in range(n):
            for j in range(i + 1):
                cel·la = str(table[j][i - j]) if table[j][i - j] else ""
                cel·la = re.sub(r"[{}']", '', cel·la)
                cel·la = f"[{cel·la.center(mida_tab)}]"
                print(cel·la, end="")
            print(" " * mida_tab)
        print()

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


cnf_grammar = Gramatica_FNC('g2.txt')

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
