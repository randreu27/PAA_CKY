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
        self.grammar = {}   # Gramàtica (diccionari de llistes)
        self.N = {}         # No terminals (claus: 2 símbols no terminals, vals: regles que les referencien)
        self.Σ = {}         # Terminals (claus: 1 símbol terminal, vals: llistes de 1 símbol no terminal)

        with open(file) as f:
            for line in f:
                # expressió regular filtra -> i |, strip() elimina espais
                line = re.split(r"\s*->\s*|\s*\|\s*", line.strip())
                self.grammar[line[0]] = line[1:]

        assert 'S' in self.grammar, 'La gramàtica no té símbol inicial (ha de ser S)'
        self.CFG_a_CNF()

        for esq, dre in self.grammar.items():
            terminals = [t for t in dre if len(t) == 1]
            no_terminals = [nt for nt in dre if len(nt) == 2]
            for t in terminals:
                if t not in self.Σ:
                    self.Σ[t] = [esq]
                else:
                    self.Σ[t].append(esq)
            for nt in no_terminals:
                if nt not in self.N:
                    self.N[nt] = [esq]
                else:
                    self.N[nt].append(esq)

        # print('Grammar:', self.grammar)
        # print('N:', self.N)
        # print('Σ:', self.Σ)

    def get(self, S):
        """
        S és un signe no terminal
        Retorna els símbols terminals produïts per S.
        Exemple:
        Input: S
        Output: ['a', 'XA', 'AX', 'b']
        """
        return self.grammar[S]

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
        taula = [[set() for _ in range(i + 1)] for i in range(n)]

        # Omplim el cas base (línia de sota)
        for i in range(n):
            taula[-1][i].update(self.Σ[cadena[i]])

        # Apliquem l'algorisme CKY
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for k in range(1, length):
                    for nt in self.N:
                        B, C = nt
                        if B in taula[-k][i] and C in taula[-(length - k)][i + k]:
                            taula[-length][i].update(self.N[nt])

        self.print_taula(taula)
        return 'S' in taula[-n][0]

    def print_taula(self, taula):
        """
        Imprimeix la taula CKY en format ASCII ben formatejada.
        """
        # Per a cada nou element, afegim 3 espais ("X, " ocupa 3 caràcters) i en restem dos per les []
        mida_tab = max(len(elem) for subllista in taula for elem in subllista) * 3 - 2

        for cel·la in taula:
            print(" " * (len(taula) - len(cel·la)) * (mida_tab + 2), end="")
            for elem in cel·la:
                elem = str(elem) if elem != set() else ""
                elem = re.sub(r"[{}']", '', elem)
                print(f"[{elem.center(mida_tab)}]", end="")
            print()
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
        # Pas 1: Eliminar regles unitàries
        # Pas 2: Eliminar no terminals amb 3 o més símbols
        # Pas 3: Eliminar regles ε
        # Pas 4: Eliminar regles amb barreja de terminals i no-terminals

        for regla in self.grammar:
            nou_conjunt_regles = self.get(regla)
            for elem in self.get(regla):
                nova_regla = elem
                # Eliminar regles ε
                if elem == 'ε':
                    self.grammar.update()
                    break
                
                # Eliminar regles amb barreja de terminals i no-terminals
                if any(map(str.isupper, nova_regla)) and any(map(str.islower, nova_regla)):
                    for literal in nova_regla:
                        if literal.islower():
                            pass
                        if literal.isupper():
                            pass
                # Eliminar regles unitàries
                # Eliminar no terminals amb 3 o més símbols
                

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
