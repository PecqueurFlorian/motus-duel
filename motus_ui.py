import pygame

ROUGE = (255, 80, 80)
JAUNE = (255, 220, 100)
VERT = (100, 220, 100)
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
CASE_TAILLE = 60
MARGE = 10
class MotusUI:
    def __init__(self, screen, mot_secret, font):
        self.screen = screen
        self.mot_secret = mot_secret.upper()
        self.font = font
        self.input_box = pygame.Rect(100, 500, 300, 50)
        self.input_text = ""
        self.resultats = []

    def afficher_interface(self):
        self.screen.fill(BLANC)
        for ligne_index, ligne in enumerate(self.resultats):
            for lettre_index, (lettre, couleur) in enumerate(ligne):
                x = 100 + lettre_index * (CASE_TAILLE + MARGE)
                y = 50 + ligne_index * (CASE_TAILLE + MARGE)
                pygame.draw.rect(self.screen, couleur, (x, y, CASE_TAILLE, CASE_TAILLE))
                texte = self.font.render(lettre, True, NOIR)
                texte_rect = texte.get_rect(center=(x + CASE_TAILLE//2, y + CASE_TAILLE//2))
                self.screen.blit(texte, texte_rect)
        pygame.draw.rect(self.screen, GRIS, self.input_box)
        texte_input = self.font.render(self.input_text, True, NOIR)
        self.screen.blit(texte_input, (self.input_box.x + 5, self.input_box.y + 10))
        pygame.draw.rect(self.screen, NOIR, self.input_box, 2)

    def ajouter_tentative(self, proposition):
        ligne = []
        proposition = proposition.upper()
        mot_secret_temp = list(self.mot_secret)
        couleurs = [""] * len(self.mot_secret)
        for i in range(len(self.mot_secret)):
            if i < len(proposition) and proposition[i] == self.mot_secret[i]:
                couleurs[i] = "VERT"
                mot_secret_temp[i] = None
        for i in range(len(self.mot_secret)):
            if couleurs[i] == "":
                lettre = proposition[i] if i < len(proposition) else ""
                if lettre in mot_secret_temp:
                    couleurs[i] = "JAUNE"
                    mot_secret_temp[mot_secret_temp.index(lettre)] = None
                else:
                    couleurs[i] = "ROUGE"
        for i in range(len(self.mot_secret)):
            lettre = proposition[i] if i < len(proposition) else ""
            if couleurs[i] == "VERT":
                couleur = VERT
            elif couleurs[i] == "JAUNE":
                couleur = JAUNE
            else:
                couleur = ROUGE
            ligne.append((lettre, couleur))
        self.resultats.append(ligne)
        self.input_text = ""
