import requests
import json

# URL du point de terminaison de l'API
API_URL = "http://127.0.0.1:5000/scan"

# La donnée à envoyer (l'URL à analyser)
data = {
    "url": "https://www.scaleway.com" 
}

print(f"Envoi de la requête à l'API pour l'URL : {data['url']}")

try:
    # Envoi de la requête POST avec le JSON
    response = requests.post(
        API_URL, 
        json=data, 
        timeout=10 # Temps maximum pour la réponse
    )
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Afficher la réponse JSON formatée
        print("\n--- Réponse de l'API (Succès 200) ---")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        # Afficher l'erreur si la requête a échoué
        print(f"\n--- Erreur de l'API (Code {response.status_code}) ---")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("\nERREUR: Impossible de se connecter à l'API.")
    print("Veuillez vérifier que l'API est bien lancée dans l'autre terminal.")
except Exception as e:
    print(f"\nUne erreur inattendue est survenue : {e}")