class Gramatica_FNC:
    """
    Processa els textos en format igual a l'exemple "g1.txt" o "g2.txt". \n
    Es pot accedir a les regles donada un altre regle no terminal, 
    per més informació consulta la descripcció del mètode get_rule().

    Mètode 
    """
    def __init__(self, raw_text):
        self.raw = raw_text
        # Llegim el arxiu de text
        text = open(raw_text, 'r')
        lines = text.readlines()

        # Separem el tokens de cada frase
        splitted = []
        for line in lines:
            aux = line.split()
            splitted.append(aux)

        # Eliminem els simbols: -, >, |, ...
        simbols = ['-', '>', '->', '|']
        for line in splitted:
            for word in line:
                if word in simbols:
                    line.remove(word)
        
        # Asignem el resultat
        self.rules = splitted

    def get_rule(self, S):
        """
        Retorna una llista de Regles terminals i/o no terminals en forma d'string
        Exemple: [ 'a' , 'XA' , 'AX' , 'b' ], sent les paraules majuscules no terminals,
        i les minuscules terminals.
        """
        for rule in self.rules:
            if S == rule[0]:
                return rule[1::]
        print('La regla no existeix!')
        raise(IndexError)

grammar = Gramatica_FNC('g1.txt')
print(grammar.get_rule('S'))