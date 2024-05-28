import re
import copy


class Gramatica_FNC:
    """
    Processa els textos en format igual a l'exemple "g1.txt" o "g2.txt".

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

        assert all((len(s) == 1 and s.islower() or len(s) == 2 and s.isupper() for s in x) for x in self.grammar.values()), 'La gramàtica no està en FNC'

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

        self.print_grammar()
        print('N:', self.N)
        print('Σ:', self.Σ)

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
        n = len(cadena)
        if n == 0:
            # la paraula buida només es pot generar en un CFG en FNC si es genera per l'element d'entrada (Z)
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

        # print(cadena)
        # self.print_taula(taula)
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

    def print_grammar(self):
        """
        Imprimeix la gramàtica en format ASCII ben formatejada.
        """
        for esq, dre in self.grammar.items():
            print(f"{esq} -> {' | '.join(dre)}")
        print()

    def CKY_prob(self, cadena: str):
        """
        Input: tira de caràcters (string).
        Output: probabilitat que la tira de caràcters pertanyi a la llengua de la gramàtica.
        """
        pass

    def treure_epsilon(self):
        """
        Elimina les regles de la forma A -> ε.
        """
        self.epsilon = False
        for esq, dre in self.grammar.items():
            if 'ε' in dre:
                self.epsilon = True
                self.grammar[esq].remove('ε')


    def CFG_a_CNF(self):
        """
        Transforma la gramàtica de CFG a CNF.
        """
        símbols_usats = set()
        for regla in self.grammar:
            for elem in self.grammar[regla]:
                símbols_usats.add(regla)
                for literal in elem:
                    símbols_usats.add(literal)

        nt_disponibles = [x for x in 'ωψφχτπξμλκθηζδβΩΨΦΣΠΞΛΘΔΓZYXWVUTSRQPONMLKJIHGFEDCBA' if x not in símbols_usats]
        t_disponibles  = [x for x in 'ωψφχτπξμλκθηζδβzyxwvutsrqponmlkjihgfedcba' if x not in símbols_usats]

        substitucions = {}  # Clau: símbols antics, Valor: símbols nous
        self.print_grammar()
        # Pas 1: Regles híbrides
        for regla in list(self.grammar):
            for idx in range(len(self.grammar[regla])):
                # Si la regla té més de 2 símbols i algun és terminal
                if len(self.grammar[regla][idx]) >= 2 and any(map(str.islower, self.grammar[regla][idx])):
                    for símbol in self.grammar[regla][idx]:
                        if símbol.islower():
                            if símbol not in substitucions:
                                # Guardem la substitució per a futur ús en altres regles (consistència)
                                substitucions[símbol] = nt_disponibles.pop()
                            self.grammar[regla][idx] = self.grammar[regla][idx].replace(símbol, substitucions[símbol])
                            self.grammar[substitucions[símbol]] = [símbol]
        self.print_grammar()
        # Pas 2: Regles unitàries
        for _ in range(len(list(self.grammar))**2):
            for regla in list(self.grammar):
                if regla not in self.grammar:
                    continue
                for idx in range(len(self.grammar[regla])):
                    if self.grammar[regla][idx] in self.grammar and len(self.grammar[regla][idx]) == 1:
                        print(regla, self.grammar[regla][idx])
                        clau_tmp = self.grammar[regla][idx]
                        self.grammar[clau_tmp] = [s.replace(clau_tmp, regla) for s in self.grammar[clau_tmp]]
                        self.grammar[regla].remove(self.grammar[regla][idx])
                        self.grammar[regla].extend(self.grammar[clau_tmp])
                        # Eliminar regla unitària (clau regla)
                        del self.grammar[clau_tmp]
                        break
                    elif self.grammar[regla][idx] in substitucions:
                        self.grammar[regla][idx] = substitucions[self.grammar[regla][idx]]
            if all(len(s) == 1 or len(s) == 2 for s in self.grammar.values()):
                print("Breaking...")
                # break

        self.print_grammar()
        # Pas 3: Regles de més de 2 símbols no terminals
        for _ in range(len(list(self.grammar))**2):
            for regla in list(self.grammar):
                for idx in range(len(self.grammar[regla])):
                    for j in range(len(self.grammar[regla][idx]) - 2):
                        if not self.grammar[regla][idx][j:j + 2].isupper():
                            continue
                        if self.grammar[regla][idx][j:j + 2] not in substitucions:
                            substitucions[self.grammar[regla][idx][j:j + 2]] = nt_disponibles.pop()

                        self.grammar[substitucions[self.grammar[regla][idx][j:j + 2]]] = [self.grammar[regla][idx][j:j + 2]]
                        self.grammar[regla][idx] = self.grammar[regla][idx].replace(self.grammar[regla][idx][j:j + 2], substitucions[self.grammar[regla][idx][j:j + 2]], 1)
            if all(len(s) <= 2 for s in self.grammar.values()):
                print("Breaking...")
                # break


cnf_grammar = Gramatica_FNC('g3.txt')

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
