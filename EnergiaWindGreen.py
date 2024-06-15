import requests
import json

def main():
    tempo = input("Che intensità ha il vento oggi? (forte, medio, basso): ").strip().lower()

    if tempo == "forte":
        energia_green = 10
    elif tempo == "medio":
        energia_green = 5
    elif tempo == "basso":
        energia_green = 2
    else:
        print("Input non valido. Per favore inserisci 'forte', 'medio' o 'basso'.")
        return

    print(f"L'energia green prodotta dalle pale eoliche è: {energia_green} kw")

    token = input("Per favore, inserisci il token: ").strip()

    url_get_all = "https://1p2pfzcjua.execute-api.us-east-1.amazonaws.com/dev/api/v1/abitazione/getAll"

    try:
        response = requests.get(url_get_all)
        response.raise_for_status()
        abitazioni = response.json().get("list", [])
    except requests.exceptions.RequestException as e:
        print(f"Errore nel recupero delle abitazioni: {e}")
        return

    url_update_energy = "https://1p2pfzcjua.execute-api.us-east-1.amazonaws.com/dev/api/v1/abitazione/updateEnergy"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    for abitazione in abitazioni:
        if abitazione.get("energiaGreen").lower() == "eolico":
            payload = {
                "id": abitazione["id"],
                "ore": abitazione.get("ore") + 1,
                "kw": abitazione.get("kw") + energia_green
            }

            try:
                response = requests.put(url_update_energy, headers=headers, data=json.dumps(payload))
                response.raise_for_status()
                print(f"Aggiornamento riuscito per l'abitazione con ID: {abitazione['id']}")
            except requests.exceptions.RequestException as e:
                print(f"Errore nell'aggiornamento dell'abitazione con ID: {abitazione['id']}. Errore: {e}")


if __name__ == "__main__":
    main()
