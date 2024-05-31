import re
import copy
from collections import defaultdict


class Gramatica_FNC():
    def __init__(self, file, to_fnc = False, pcky = False):
        """
    Processa els textos en format igual a l'exemple "g1.txt" o "g2.txt".

    Regles de format:\n
        · Terminals en minúscules.\n
        · No terminals en majúscules.\n
        · Els símbols han de tenir mida 1.\n
        · Si en volguéssim tenir més per representar frases com a PLH, hauríem de separar els símbols d'alguna manera, que en general no hem fet a PAA. \n
        · Per tant, hem decidit mantenir el format de classe (ex: S -> aSb).

--------------------------------------------------------------------------------
    Paràmetre: file    (string)    : Nom del arxiu amb la gramàtica, és obligatori. \n
    Exemple del contingut:

    S -> a | XA | AX | b \n
    A -> RB \n
    B -> AX | b | a \n
    X -> a \n
    R -> XB \n

--------------------------------------------------------------------------------

    Paràmetre: to_fnc  (boolean)   : Obligatori possar True si la gramatica no esta en FNC. \n
    Exemple del contingut:

    S -> aSa | bSb | a | b

--------------------------------------------------------------------------------

    Paràmetre: pcky    (boolean)   : Si la gramàtica és probabilista, és obligatori possar True. \n
    Cal aclarir que l'algorisme de la classe permet usar el CKY No Probabilísta i la CKY Probabilísta per aquest tipus de gramàtiques.\n
    Exemple del contingut:

    S -> a | XA | AX | b    [0.1 0.4 0.4 0.1] \n
    A -> RB                 [1] \n
    B -> AX | b | a         [0.5 0.25 0.25] \n
    X -> a                  [1] \n
    R -> XB                 [1]
    """
        
        self.grammar = {}           # Gramàtica (diccionari de llistes)
        self.probabilities = {}     # Probabilitats de les regles
        self.N = {}                 # No terminals (claus: 2 símbols no terminals, vals: regles que les referencien)
        self.Σ = {}                 # Terminals (claus: 1 símbol terminal, vals: llistes de 1 símbol no terminal)

        if pcky == False:
            with open(file) as f:
                for line in f:
                    # expressió regular filtra -> i |, strip() elimina espais
                    line = re.split(r"\s*->\s*|\s*\|\s*", line.strip())
                    self.grammar[line[0]] = line[1:]

            assert 'S' in self.grammar, 'La gramàtica no té símbol inicial (ha de ser S)'

            # Conversió a CNF si és necessari
            if to_fnc == True:
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

        elif pcky == True:
            # Gestiona les probabilitats de la gramàtica
            with open(file) as f:
                for line in f:
                    line = line.strip().split('->')
                    lhs = line[0].strip()
                    rhs_prob = re.split(r'\s*\[\s*|\s*\]\s*', line[1].strip())
                    rhs = rhs_prob[0].strip().split(' | ')
                    probs = list(map(float, rhs_prob[1].strip().split()))
                    self.grammar[lhs] = rhs
                    self.probabilities[lhs] = probs

            # Conversió a CNF si és necessari
            if to_fnc:
                self.CFG_a_CNF_prob()

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
        n = len(cadena)
        if n == 0:
            return float('S' in self.grammar and '' in self.grammar['S'])

        # Creem la taula triangular superior per el CKY
        taula = [[defaultdict(float) for _ in range(i + 1)] for i in range(n)]

        # Omplim el cas base
        for i in range(n):
            for nt in self.Σ[cadena[i]]:
                idx = self.grammar[nt].index(cadena[i])
                taula[-1][i][nt] = self.probabilities[nt][idx]

        # Apliquem l'algorisme CKY
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for k in range(1, length):
                    for nt in self.N:
                        B, C = nt
                        prob_B = taula[-k][i].get(B, 0)
                        prob_C = taula[-(length - k)][i + k].get(C, 0)
                        if prob_B > 0 and prob_C > 0:
                            for rule in self.N[nt]:
                                idx = self.grammar[rule].index(nt)
                                taula[-length][i][rule] += self.probabilities[rule][idx] * prob_B * prob_C

        return taula[-n][0].get('S', 0.0)

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

        substitucions = {}  # Clau: símbols antics, Valor: símbols nous
        self.print_grammar()

        # Pas 1: Regles híbrides
        for regla in list(self.grammar):
            for idx in range(len(self.grammar[regla])):
                # Si la regla té 2 o més símbols i algun és terminal
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
                        clau_unitària = self.grammar[regla][idx]
                        if clau_unitària not in substitucions:
                            substitucions[regla] = clau_unitària
                        self.grammar[regla].extend(self.grammar[clau_unitària])
                        self.grammar[regla].remove(clau_unitària)
                        # Eliminar regla unitària (clau regla)
                        del self.grammar[clau_unitària]
                    elif regla in substitucions and substitucions[regla] in self.grammar[regla][idx]:
                        self.grammar[regla][idx] = self.grammar[regla][idx].replace(substitucions[regla], regla)
        self.print_grammar()

        # Pas 3: Regles de més de 2 símbols no terminals
        for _ in range(len(list(self.grammar))**2):
            for regla in list(self.grammar):
                for idx in range(len(self.grammar[regla])):
                    if len(self.grammar[regla][idx]) > 2:
                        while len(self.grammar[regla][idx]) > 2:
                            if self.grammar[regla][idx][:2] not in substitucions:
                                substitucions[self.grammar[regla][idx][:2]] = nt_disponibles.pop()
                            self.grammar[regla].append(substitucions[self.grammar[regla][idx][:2]])
                            self.grammar[substitucions[self.grammar[regla][idx][:2]]] = [self.grammar[regla][idx][:2]]
                            self.grammar[regla][idx] = substitucions[self.grammar[regla][idx][:2]] + self.grammar[regla][idx][2:]
        self.print_grammar()

        # Ajustaments finals al diccionaris N i Σ
        self.N = {}
        self.Σ = {}
        for esq, dre in self.grammar.items():
            terminals = [t for t in dre if len(t) == 1 and t.islower()]
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

    def CFG_a_CNF_prob(self):
        """
        Transforma la gramàtica probabilista de CFG a CNF.
        """
        símbols_usats = set()
        for regla in self.grammar:
            for elem in self.grammar[regla]:
                símbols_usats.add(regla)
                for literal in elem:
                    símbols_usats.add(literal)
        nt_disponibles = [x for x in 'ωψφχτπξμλκθηζδβΩΨΦΣΠΞΛΘΔΓZYXWVUTSRQPONMLKJIHGFEDCBA' if x not in símbols_usats]

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
                        clau_unitària = self.grammar[regla][idx]
                        if clau_unitària not in substitucions:
                            substitucions[regla] = clau_unitària
                        self.grammar[regla].extend(self.grammar[clau_unitària])
                        self.grammar[regla].remove(clau_unitària)
                        # Eliminar regla unitària (clau regla)
                        del self.grammar[clau_unitària]
                    elif regla in substitucions and substitucions[regla] in self.grammar[regla][idx]:
                        self.grammar[regla][idx] = self.grammar[regla][idx].replace(substitucions[regla], regla)
        self.print_grammar()
        # Pas 3: Regles de més de 2 símbols no terminals
        for _ in range(len(list(self.grammar))**2):
            for regla in list(self.grammar):
                for idx in range(len(self.grammar[regla])):
                    if len(self.grammar[regla][idx]) > 2:
                        while len(self.grammar[regla][idx]) > 2:
                            if self.grammar[regla][idx][:2] not in substitucions:
                                substitucions[self.grammar[regla][idx][:2]] = nt_disponibles.pop()
                            self.grammar[regla].append(substitucions[self.grammar[regla][idx][:2]])
                            self.grammar[substitucions[self.grammar[regla][idx][:2]]] = [self.grammar[regla][idx][:2]]
                            self.grammar[regla][idx] = substitucions[self.grammar[regla][idx][:2]] + self.grammar[regla][idx][2:]
        self.print_grammar()
        new_probabilities = {}
        for lhs, rhs_list in self.grammar.items():
            if lhs in self.probabilities:
                probabilities = self.probabilities[lhs]
            else:
                probabilities = [1] * len(rhs_list)  # Si no hi han probabilitats definides asignem 1 a les produccions
            new_prob_list = []
            for idx, rhs in enumerate(rhs_list):
                # Calculem la probabilitat per a la nova producció, si n'hi ha una existent
                if lhs in self.probabilities and idx < len(self.probabilities[lhs]):
                    new_prob = self.probabilities[lhs][idx] / len(rhs_list)
                else:
                    new_prob = 1 / len(rhs_list)  # Si no hi ha probabilitat definida, distribuïm igualment
                new_prob_list.append(new_prob)
            new_probabilities[lhs] = new_prob_list

        # Assignem les noves probabilitats al diccionari de probabilitats
        self.probabilities = new_probabilities

        # Ajustaments finals al diccionaris N i Σ
        self.N = {}
        self.Σ = {}
        for esq, dre in self.grammar.items():
            terminals = [t for t in dre if len(t) == 1 and t.islower()]
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
