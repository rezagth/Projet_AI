from googlesearch import search

class IAJuridiqueWeb:
    def __init__(self):
        self.sources = {
            "Legifrance": "https://www.legifrance.gouv.fr",
            "Chambre nationale des commissaires de justice": "https://commissaire-justice.fr",
            "Service-Public": "https://www.service-public.fr",
        }

    def recherche_google(self, mot_cle):
        """Recherche sur Google avec des sites spécifiques"""
        resultats = []
        requetes = [
            f"site:legifrance.gouv.fr {mot_cle}",
            f"site:commissaire-justice.fr {mot_cle}",
            f"site:service-public.fr {mot_cle}",
        ]
        for requete in requetes:
            try:
                # Effectuer la recherche Google pour chaque requête
                for url in search(requete, num_results=3):  # Limiter à 3 résultats pour chaque site
                    resultats.append(f"🔍 {url}")
            except Exception as e:
                print(f"Erreur Google pour '{requete}': {e}")

        return resultats if resultats else ["Aucun lien pertinent trouvé."]

    def generer_reponse(self, mot_cle):
        """Appel de la recherche Google pour obtenir les liens"""
        resultats = self.recherche_google(mot_cle)
        if resultats:
            return "\n".join(resultats)
        else:
            return f"\n===== Résultats pour : '{mot_cle}' =====\nAucun résultat trouvé."
