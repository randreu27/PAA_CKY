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
        Input: file (string) amb el nom del fitxer que conté la gramàtica.
        """
        self.grammar = {}  # Gramàtica (diccionari de llistes)
        self.Σ = set()     # Símbols terminals
        self.N = set()     # Símbols no terminals
        self.inv_Σ = {}
        self.inv_N = {}

        with open(file) as f:
            for line in f:
                # expressió regular filtra -> i |, strip() elimina espais
                line = re.split(r"\s*->\s*|\s*\|\s*", line.strip())
                self.grammar[line[0]] = line[1:]
                self.inv_Σ
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
        print('Grammar:', self.grammar)

        for esq, dre in self.grammar.items():
            terminals = [t for t in dre if len(t) == 1]
            no_terminals = [nt for nt in dre if len(nt) == 2]
            for t in terminals:
                if t not in self.inv_Σ:
                    self.inv_Σ[t] = [esq]
                else:
                    self.inv_Σ[t].append(esq)
            for nt in no_terminals:
                if esq not in self.inv_N:
                    self.inv_N[esq] = [nt]
                else:
                    self.inv_N[esq].append(nt)

        print('inv_Σ:', self.inv_Σ)
        print('inv_N', self.inv_N)

    def get_produccions(self, S):
        """
        Retorna una llista de Regles terminals i/o no terminals en forma d'string.
        Exemple: [ 'a' , '(X, A)' , '(A, X)' , 'b' ], sent les paraules majúscules no terminals,
        i les minúscules terminals.
        """
        return [nt for nt in self.grammar[S] if nt.isupper()]

    def get_N(self):
        """
        Retorna els símbols no-terminals (en majúscula) de la gramàtica.
        """
        return self.N

    def get_Σ(self):
        """
        Retorna els símbols terminals (en minúscula) de la gramàtica.
        """
        return self.Σ

    def CKY_det(self, cadena: str):
        """
        Input: tira de caràcters (string).
        Output: True si la tira de caràcters pertany a la llengua de la gramàtica, False en cas contrari.
        """
        print(cadena)
        n = len(cadena)
        if n == 0:
            # la paraula buida només es pot generar en un CFG en FNC si es genera per l'element d'entrada (S)
            return 'S' in self.grammar and '' in self.grammar['S']

        # Creem la taula triangular superior per el CKY
        table = [[set() for _ in range(i + 1)] for i in range(n)]

        # Omplim el cas base (línia de sota)
        for i in range(n):
            print(self.inv_Σ, cadena, i, cadena[i])
            for t in self.inv_Σ[cadena[i]]:
                table[-1][i].add(t)

        # Apliquem l'algorisme CKY
        m = 0
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for k in range(1, length):
                    for nt in self.grammar:
                        for elem in self.get_produccions(nt):
                            m += 1
                            if elem[0] in table[-k][i] and elem[1] in table[-(length - k)][i + k]:
                                table[-length][i].add(nt)
                                break
        print("M:", m)
        self.print_table(table)

        print('S' in table[-n][0])
        return 'S' in table[-n][0]

    def print_table(self, table):
        """
        Imprimeix la taula CKY en format ASCII ben formatejada.
        """
        # Per a cada nou element, afegim 3 espais ("X, " ocupa 3 caràcters) i en restem dos per les []
        mida_tab = max(len(elem) for subllista in table for elem in subllista) * 3 - 2

        for cel·la in table:
            for elem in cel·la:
                elem = str(elem) if elem != set() else ""
                elem = re.sub(r"[{}']", '', elem)
                print(f"[{elem.center(mida_tab)}]", end="")
            print()

    def CKY_prob(self, cadena: str):
        """
        Input: tira de caràcters (string).
        Output: probabilitat que la tira de caràcters pertanyi a la llengua de la gramàtica.
        """
        pass

    def CFG_a_CNF(self):
        """
        Transforma la gramàtica de CFG a CNF.
        """


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
