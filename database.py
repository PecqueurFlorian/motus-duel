import mysql.connector
class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            port=8889,
            user="root",
            password="root",
            database="motus_duel"
        )
        self.cursor = self.connection.cursor()

    def ajouter_joueur(self, nom):
        query = "INSERT INTO joueurs (nom) VALUES (%s)"
        self.cursor.execute(query, (nom,))
        self.connection.commit()

    def maj_score(self, nom, score, gagne):
        if gagne:
            query = """
                UPDATE joueurs
                SET score_total = score_total + %s, parties_gagnees = parties_gagnees + 1
                WHERE nom = %s
            """
        else:
            query = """
                UPDATE joueurs
                SET score_total = score_total + %s, parties_perdues = parties_perdues + 1
                WHERE nom = %s
            """
        self.cursor.execute(query, (score, nom))
        self.connection.commit()

    def enregistrer_partie(self, joueur1, joueur2, score1, score2, gagnant):
        requete = """
        INSERT INTO partie (joueur1, joueur2, score_joueur1, score_joueur2, gagnant)
        VALUES (%s, %s, %s, %s, %s)
        """
        valeurs = (joueur1, joueur2, score1, score2, gagnant)
        self.cursor.execute(requete, valeurs)
        self.connection.commit()

    def fermer_connexion(self):
        self.cursor.close()
        self.connection.close()
