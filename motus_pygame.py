import pygame
import sys
from database import DatabaseManager
from motus_ui import MotusUI
from motus import MotusGame
pygame.init()
LARGEUR, HAUTEUR = 800, 600
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Motus Duel 🎯")
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (50, 130, 200)
VERT_FONCE = (0, 120, 0)
ROUGE = (200, 0, 0)
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
class Menu:
    def __init__(self):
        self.joueur1 = ""
        self.joueur2 = ""
        self.active_input1 = False
        self.active_input2 = False
        self.input_box1 = pygame.Rect(300, 200, 200, 50)
        self.input_box2 = pygame.Rect(300, 300, 200, 50)
        self.start_button = pygame.Rect(300, 400, 155, 50)
        self.db = DatabaseManager()

    def afficher(self):
        screen.fill(BLANC)
        titre = font.render("Motus Duel", True, NOIR)
        screen.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 50))
        txt_surface1 = small_font.render(self.joueur1, True, NOIR)
        pygame.draw.rect(screen, BLEU if self.active_input1 else NOIR, self.input_box1, 2)
        screen.blit(txt_surface1, (self.input_box1.x + 5, self.input_box1.y + 10))
        screen.blit(small_font.render("Nom Joueur 1 :", True, NOIR), (self.input_box1.x, self.input_box1.y - 30))
        txt_surface2 = small_font.render(self.joueur2, True, NOIR)
        pygame.draw.rect(screen, BLEU if self.active_input2 else NOIR, self.input_box2, 2)
        screen.blit(txt_surface2, (self.input_box2.x + 5, self.input_box2.y + 10))
        screen.blit(small_font.render("Nom Joueur 2 :", True, NOIR), (self.input_box2.x, self.input_box2.y - 30))
        pygame.draw.rect(screen, BLEU, self.start_button)
        screen.blit(small_font.render("Commencer", True, BLANC), (self.start_button.x + 10, self.start_button.y + 10))

    def gerer_evenements(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box1.collidepoint(event.pos):
                self.active_input1 = True
                self.active_input2 = False
            elif self.input_box2.collidepoint(event.pos):
                self.active_input2 = True
                self.active_input1 = False
            elif self.start_button.collidepoint(event.pos):
                if self.joueur1 and self.joueur2:
                    self.db.ajouter_joueur(self.joueur1)
                    self.db.ajouter_joueur(self.joueur2)
                    return True
        if event.type == pygame.KEYDOWN:
            if self.active_input1:
                if event.key == pygame.K_BACKSPACE:
                    self.joueur1 = self.joueur1[:-1]
                else:
                    self.joueur1 += event.unicode
            elif self.active_input2:
                if event.key == pygame.K_BACKSPACE:
                    self.joueur2 = self.joueur2[:-1]
                else:
                    self.joueur2 += event.unicode
        return False

def saisir_mot_secret(screen, font, joueur):
    clock = pygame.time.Clock()
    mot_cache = ""
    entrer = False
    input_box = pygame.Rect(200, 250, 400, 60)
    while not entrer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(mot_cache) >= 4:
                    entrer = True
                elif event.key == pygame.K_BACKSPACE:
                    mot_cache = mot_cache[:-1]
                elif event.unicode.isalpha() and len(mot_cache) < 8:
                    mot_cache += event.unicode.upper()
        screen.fill(BLANC)
        pygame.draw.rect(screen, NOIR, input_box, 2)
        texte_cache = "*" * len(mot_cache)
        texte_surface = font.render(texte_cache, True, NOIR)
        screen.blit(texte_surface, (input_box.x + 10, input_box.y + 10))
        titre = font.render(f"{joueur}, choisis un mot secret :", True, NOIR)
        screen.blit(titre, (150, 150))
        info = pygame.font.SysFont(None, 24).render("Appuie sur Entrée pour valider (min. 4 lettres)", True, (100, 100, 100))
        screen.blit(info, (200, 320))
        pygame.display.flip()
        clock.tick(30)
    return mot_cache

def main():
    clock = pygame.time.Clock()
    menu = Menu()
    dans_menu = True
    jeu = MotusGame(menu.joueur1, menu.joueur2)
    motus_ui = None
    mot_secret = ""
    fin_manche = False
    message_fin = ""
    afficher_bouton_suivant = False
    fin_du_jeu = False
    manche_actuelle = 1
    max_manches = 5
    joueur_actuel = 1
    score_j1 = 0
    score_j2 = 0
    bouton_suivant = pygame.Rect(300, 540, 200, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if dans_menu:
                if menu.gerer_evenements(event):
                    joueur_propose = menu.joueur1 if joueur_actuel == 1 else menu.joueur2
                    mot_secret = saisir_mot_secret(screen, font, joueur_propose)
                    jeu = MotusGame(menu.joueur1, menu.joueur2)
                    jeu.choisir_mot(mot_secret)
                    motus_ui = MotusUI(screen, mot_secret, font)
                    dans_menu = False
                    fin_manche = False
                    message_fin = ""
                    afficher_bouton_suivant = False
            elif not fin_manche and not fin_du_jeu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and motus_ui.input_text:
                        proposition = motus_ui.input_text
                        _, gagne = jeu.deviner(proposition)
                        motus_ui.ajouter_tentative(proposition)
                        if gagne:
                            message_fin = "Gagné !"
                            if joueur_actuel == 1:
                                score_j2 += 1
                            else:
                                score_j1 += 1
                            fin_manche = True
                            afficher_bouton_suivant = True
                        elif jeu.tentatives >= jeu.max_essais:
                            message_fin = f"Perdu ! Le mot était : {mot_secret}"
                            fin_manche = True
                            afficher_bouton_suivant = True
                    elif event.key == pygame.K_BACKSPACE:
                        motus_ui.input_text = motus_ui.input_text[:-1]
                    else:
                        if len(motus_ui.input_text) < len(mot_secret):
                            motus_ui.input_text += event.unicode.upper()
            elif fin_manche and event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_suivant.collidepoint(event.pos):
                    manche_actuelle += 1
                    joueur_actuel = 2 if joueur_actuel == 1 else 1
                    if manche_actuelle > max_manches:
                        fin_du_jeu = True
                        gagnant_final = "Égalité"
                        if score_j1 > score_j2:
                            gagnant_final = menu.joueur1
                        elif score_j2 > score_j1:
                            gagnant_final = menu.joueur2
                        menu.db.enregistrer_partie(menu.joueur1, menu.joueur2, score_j1, score_j2, gagnant_final)
                    else:
                        dans_menu = True
            elif fin_du_jeu and event.type == pygame.MOUSEBUTTONDOWN:
                quit_btn = pygame.Rect(LARGEUR // 2 - 100, 400, 200, 50)
                if quit_btn.collidepoint(event.pos):
                    running = False
        if dans_menu:
            menu.afficher()
        elif not fin_du_jeu:
            motus_ui.afficher_interface()
            manche_txt = small_font.render(f"Manche {manche_actuelle} / {max_manches}", True, NOIR)
            screen.blit(manche_txt, (20, 20))
            if fin_manche:
                texte_fin = font.render(message_fin, True, (255, 0, 0))
                screen.blit(texte_fin, (200, 480))
                if afficher_bouton_suivant:
                    pygame.draw.rect(screen, VERT_FONCE, bouton_suivant)
                    screen.blit(small_font.render("➡ Manche suivante", True, BLANC), (bouton_suivant.x + 20, bouton_suivant.y + 8))
        else:
            screen.fill(BLANC)
            titre = font.render("Résultat final", True, NOIR)
            screen.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 80))
            score_txt = f"{menu.joueur1} : {score_j1}    {menu.joueur2} : {score_j2}"
            score_surface = font.render(score_txt, True, NOIR)
            screen.blit(score_surface, (LARGEUR // 2 - score_surface.get_width() // 2, 200))
            if score_j1 > score_j2:
                msg = f"Victoire de {menu.joueur1} !"
            elif score_j2 > score_j1:
                msg = f"Victoire de {menu.joueur2} !"
            else:
                msg = "Match nul !"
            resultat = font.render(msg, True, VERT_FONCE)
            screen.blit(resultat, (LARGEUR // 2 - resultat.get_width() // 2, 300))
            quit_btn = pygame.Rect(LARGEUR // 2 - 100, 400, 200, 50)
            pygame.draw.rect(screen, ROUGE, quit_btn)
            screen.blit(small_font.render("Quitter", True, BLANC), (quit_btn.x + 50, quit_btn.y + 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
