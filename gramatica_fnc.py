class Gramatica_FNC:
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
        cleaned = []
        for line in splitted:
            for word in line:
                if word in simbols:
                    aux = line.remove(word)
            cleaned.append(aux)
        
        