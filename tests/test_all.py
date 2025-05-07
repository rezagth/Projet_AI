import pytest
from unittest.mock import patch
from ia_jurisite import IAJuridiqueWeb  # Modifie si le nom de ton fichier est différent

# Test de la méthode recherche_google avec de vrais liens simulés
@patch('ia_jurisite.search')  # Patch la fonction là où elle est importée dans ton code
def test_recherche_google(mock_search):
    ia_juridique = IAJuridiqueWeb()

    # Simuler les résultats de recherche pour chaque domaine
    mock_search.side_effect = [
        [  # Résultats pour legifrance
            "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356/",
            "https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070719/"
        ],
        [  # Résultats pour commissaire-justice.fr
            "https://www.commissaire-justice.fr/actualites/fiche/nomination-nouveaux-commissaires"
        ],
        [  # Résultats pour service-public.fr
            "https://www.service-public.fr/professionnels-entreprises/vosdroits/F31228"
        ]
    ]

    mot_cle = "saisie "
    resultats = ia_juridique.recherche_google(mot_cle)

    assert len(resultats) == 4
    assert any("legifrance.gouv.fr" in url for url in resultats)
    assert any("commissaire-justice.fr" in url for url in resultats)
    assert any("service-public.fr" in url for url in resultats)
    for url in resultats:
        assert url.startswith("🔍 http")


# Test de la méthode generer_reponse avec des résultats simulés
@patch('ia_jurisite.search')
def test_generer_reponse(mock_search):
    ia_juridique = IAJuridiqueWeb()

    mock_search.side_effect = [
        ["https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356/"],
        ["https://www.commissaire-justice.fr/actualites/fiche/nomination-nouveaux-commissaires"],
        ["https://www.service-public.fr/professionnels-entreprises/vosdroits/F31228"]
    ]

    reponse = ia_juridique.generer_reponse("vente aux enchères")

    assert "https://www.legifrance.gouv.fr" in reponse
    assert "https://www.commissaire-justice.fr" in reponse
    assert "https://www.service-public.fr" in reponse


# Test pour vérifier le comportement sans résultats
@patch('ia_jurisite.search')
def test_aucun_resultat(mock_search):
    ia_juridique = IAJuridiqueWeb()
    
    # Simuler aucun résultat pour tous les sites
    mock_search.side_effect = [[], [], []]

    reponse = ia_juridique.generer_reponse("terme inexistant improbable")

    assert "Aucun résultat trouvé" in reponse
