import random
class MotusGame:
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.mot_secret = ""
        self.tentatives = 0
        self.max_essais = 5
    def choisir_mot(self, mot):
        self.mot_secret = mot.upper()
        self.tentatives = 0
    def deviner(self, proposition):
        self.tentatives += 1
        proposition = proposition.upper()
        resultat = []
        for i in range(len(self.mot_secret)):
            if i < len(proposition):
                if proposition[i] == self.mot_secret[i]:
                    resultat.append("V")
                elif proposition[i] in self.mot_secret:
                    resultat.append("J")
                else:
                    resultat.append("R")
            else:
                resultat.append("V")
        gagne = (proposition == self.mot_secret)
        return resultat, gagne