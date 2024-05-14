class Gramatica_FNC:
    """def __init__(self, raw_text):
        self.raw = raw_text
        # Llegim el arxiu de text
        text = open(raw_text, 'r')
        lines = text.readlines()

        # Separem el tokens de cada frase
        splitted = []
        for line in lines:
            aux = line.split()
            splitted.append(aux)
        print(splitted)

        # Eliminem els simbols: -, >, |, ...
        simbols = ['-', '>', '->', '|']
        cleaned = []
        for line in splitted:
            for word in line:
                if word in simbols:
                    aux = line.remove(word)
            cleaned.append(aux)"""

    def __init__(self, file):
        """
        Input: file (string) amb el nom del fitxer que conté la gramàtica
        """
        self.grammar = {}
        with open(file) as f:
            for line in f:
                line = line.split()
                # el primer element és el símbol no terminal i a partir del segon,
                # cada dos (obviem el |) són els predicats
                left, right = line[0], line[2::2]
                self.grammar[left] = right
        print(self.grammar)

    def CKY_det(self, tira: str):
        """
        Input: tira de caràcters (string)
        Output: True si la tira de caràcters pertany a la llengua de la gramàtica, False en cas contrari
        """
        # for s in range(len(tira)):

Gramatica_FNC("g2.txt")
