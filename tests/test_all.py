# test_iajuridique.py
import pytest
from unittest.mock import patch
from iajuridique import IAJuridiqueWeb

# Test de la méthode recherche_google
@patch('googlesearch.search')  # On simule l'appel à search
def test_recherche_google(mock_search):
    # Créer une instance de la classe
    ia_juridique = IAJuridiqueWeb()

    # Simuler des résultats pour chaque site
    mock_search.return_value = [
        "https://www.legifrance.gouv.fr/decision1",
        "https://www.legifrance.gouv.fr/decision2",
        "https://www.service-public.fr/information"
    ]

    # Tester la méthode recherche_google
    resultats = ia_juridique.recherche_google("liquidation judiciaire")

    # Vérifier les résultats obtenus
    assert len(resultats) == 3
    assert "🔍 https://www.legifrance.gouv.fr/decision1" in resultats
    assert "🔍 https://www.service-public.fr/information" in resultats
    assert "🔍 https://www.legifrance.gouv.fr/decision2" in resultats


# Test de la méthode generer_reponse
@patch('googlesearch.search')  # On simule l'appel à search
def test_generer_reponse(mock_search):
    # Créer une instance de la classe
    ia_juridique = IAJuridiqueWeb()

    # Simuler des résultats pour chaque site
    mock_search.return_value = [
        "https://www.legifrance.gouv.fr/decision1",
        "https://www.legifrance.gouv.fr/decision2",
        "https://www.service-public.fr/information"
    ]

    # Tester la méthode generer_reponse
    reponse = ia_juridique.generer_reponse("liquidation judiciaire")

    # Vérifier que la réponse contient les bons résultats
    assert "🔍 https://www.legifrance.gouv.fr/decision1" in reponse
    assert "🔍 https://www.service-public.fr/information" in reponse
    assert "🔍 https://www.legifrance.gouv.fr/decision2" in reponse

    # Tester un cas avec aucun résultat
    mock_search.return_value = []
    reponse_vide = ia_juridique.generer_reponse("mot clé inexistant")

    # Vérifier que le message "Aucun résultat trouvé" est dans la réponse
    assert "Aucun résultat trouvé" in reponse_vide
