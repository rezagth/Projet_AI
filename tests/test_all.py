import pytest
from unittest.mock import patch
from ia_jurisite import IAJuridiqueWeb  # Modifie si le nom de ton fichier est différent

# Constantes pour les tests
URLS_LEGIFRANCE = [
    "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356/",
    "https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070719/"
]
URLS_COMMISSAIRE_JUSTICE = [
    "https://www.commissaire-justice.fr/actualites/fiche/nomination-nouveaux-commissaires"
]
URLS_SERVICE_PUBLIC = [
    "https://www.service-public.fr/professionnels-entreprises/vosdroits/F31228"
]
# Mise à jour pour résoudre l'erreur
MESSAGE_AUCUN_RESULTAT = "Aucun lien pertinent trouvé"

# Fonction utilitaire pour créer une instance de IAJuridiqueWeb
def creer_instance_ia():
    """Créer une instance de l'objet IAJuridiqueWeb."""
    return IAJuridiqueWeb()


# Test de la méthode recherche_google avec de vrais liens simulés
@patch('ia_jurisite.search')  # Patch la fonction là où elle est importée dans le code
def test_recherche_google(mock_search):
    """
    Teste que la méthode recherche_google retourne les bons résultats simulés pour chaque domaine.
    """
    ia_juridique = creer_instance_ia()

    # Simuler les résultats de recherche
    mock_search.side_effect = [
        URLS_LEGIFRANCE,
        URLS_COMMISSAIRE_JUSTICE,
        URLS_SERVICE_PUBLIC,
    ]

    mot_cle = "saisie"
    resultats = ia_juridique.recherche_google(mot_cle)

    assert len(resultats) == 4, "Le nombre de résultats retournés est incorrect."
    assert any("legifrance.gouv.fr" in url for url in resultats), "Le domaine legifrance.gouv.fr est manquant."
    assert any("commissaire-justice.fr" in url for url in resultats), "Le domaine commissaire-justice.fr est manquant."
    assert any("service-public.fr" in url for url in resultats), "Le domaine service-public.fr est manquant."
    for url in resultats:
        assert url.startswith("🔍 http"), "Chaque URL doit commencer par '🔍 http'."


# Test de la méthode generer_reponse avec des résultats simulés
@patch('ia_jurisite.search')
def test_generer_reponse(mock_search):
    """
    Teste que generer_reponse retourne une réponse contenant les liens simulés.
    """
    ia_juridique = creer_instance_ia()

    # Simuler les résultats de recherche
    mock_search.side_effect = [
        [URLS_LEGIFRANCE[0]],
        [URLS_COMMISSAIRE_JUSTICE[0]],
        [URLS_SERVICE_PUBLIC[0]],
    ]

    reponse = ia_juridique.generer_reponse("vente aux enchères")

    assert "https://www.legifrance.gouv.fr" in reponse, "Le lien du domaine legifrance.gouv.fr est absent."
    assert "https://www.commissaire-justice.fr" in reponse, "Le lien du domaine commissaire-justice.fr est absent."
    assert "https://www.service-public.fr" in reponse, "Le lien du domaine service-public.fr est absent."


# Test pour vérifier le comportement sans résultats
@patch('ia_jurisite.search')
def test_aucun_resultat(mock_search):
    """
    Teste que generer_reponse retourne un message approprié lorsqu'aucun résultat n'est trouvé.
    """
    ia_juridique = creer_instance_ia()
    
    # Simuler aucun résultat pour tous les sites
    mock_search.side_effect = [[], [], []]

    reponse = ia_juridique.generer_reponse("terme inexistant improbable")

    assert MESSAGE_AUCUN_RESULTAT in reponse, f"Le message attendu '{MESSAGE_AUCUN_RESULTAT}' est absent."