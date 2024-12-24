import requests
import json

def get_contacts(company_name, country="chile"):
    """Retrieves contact information from the specified API."""

    base_url = "http://167.172.209.162:81/search"  # API Endpoint
    positions = ["vicepresidente", "jefe", "chief", "gerente", "director"]
    all_contacts = []

    for position in positions:
        # Prepare the request payload
        empresa = company_name.replace(" S.A.S.", "").replace(" S.A.S", "").replace(" S A S", "").replace(" SAS", "").replace(" S.A.C.", "").replace(" S.A.C", "").replace(" S C S", "").replace(" SCS", "").replace(" S.C.S.", "").replace(" S.C.S", "").replace(" S.A.", "").replace(" S.A", "").replace(" S A", "").lower()
        query = f"allintitle:{position} {empresa} linkedin"
        payload = {
            "company_name": empresa,
            "country": country,
            "general_position": position,
            "keywords": "linkedin",
            "operator": "allintitle:",
            "pages": 1,
            "validate": False,
            "extra_configs": {
                "gl": "cl",
                "cr": "cl",
                "hl": "es",
                "lr": "lang_es",
                "location": country,  # Use the provided country
                "google_domain": "google.cl",
                "device": "desktop",
                "include_answer_box": "true",
                "safe": "off",
                "filter": "0",
                "nfpr": "1",
                "tbs": "sbd:0",
                "num": 100
            },
            "query": query
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(base_url, json=payload, headers=headers, timeout=10)  # Added timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            all_contacts.extend(data.get("micro_contacts", []))
            all_contacts.extend(data.get("macro_contacts", []))

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None  # Or handle the error as needed

    return all_contacts


if __name__ == "__main__":
    company_name = "Empresa ABC S.A."  # Example company name
    contacts = get_contacts(company_name)

    if contacts:
        print(json.dumps(contacts, indent=4))
    else:
        print("No contacts found or an error occurred.")

