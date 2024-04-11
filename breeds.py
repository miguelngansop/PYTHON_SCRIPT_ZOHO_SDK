import requests
import os
from zohocrmsdk.src.com.zoho.api.authenticator import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api import Initializer, HeaderMap
from zohocrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zohocrmsdk.src.com.zoho.crm.api.record import RecordOperations, BodyWrapper, Record, Field
from zohocrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
from zohocrmsdk.src.com.zoho.crm.api.record import SearchRecordsParam
from dotenv import load_dotenv
import concurrent.futures

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser les variables d'environnement
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_GRANT_TOKEN = os.getenv("ZOHO_GRANT_TOKEN")

class ZohoCRMContactCreator:
    @staticmethod
    def initialize_zoho_crm():
        # Initialise l'environnement et le token OAuth pour Zoho CRM
        environment = USDataCenter.PRODUCTION()
        token = OAuthToken(client_id=ZOHO_CLIENT_ID, client_secret=ZOHO_CLIENT_SECRET, grant_token=ZOHO_GRANT_TOKEN)
        Initializer.initialize(environment, token)

    @staticmethod
    def create_contact_if_not_exists(breed):
        try:
            # Vérifie si le contact existe déjà dans Zoho CRM
            param_instance = ParameterMap()
            param_instance.add(SearchRecordsParam.email, breed.replace(" ", "_") + "@gmail.com")
            response = RecordOperations("Contacts").search_records(param_instance)
            if response is not None:
                response_object = response.get_object()
                if response_object is not None:
                    record_list = response_object.get_data()
                    if record_list and len(record_list) > 0:
                        print("Le contact {} existe déjà dans Zoho CRM.".format(breed))
                        return

            # Crée le contact dans Zoho CRM
            record_operations = RecordOperations("Contacts")
            request = BodyWrapper()
            record = Record()
            record.add_field_value(Field.Contacts.first_name(), breed)
            record.add_field_value(Field.Contacts.last_name(), breed)
            record.add_field_value(Field.Contacts.email(), breed.replace(" ", "_") + "@gmail.com")
            request.set_data([record])
            header_instance = HeaderMap()
            response = record_operations.create_records(request, header_instance)
            if response is not None:
                print("Contact {} créé avec succès dans Zoho CRM.".format(breed))
        except Exception as e:
            print(f"Une erreur s'est produite pour le contact {breed}: {e}")

def main():
    # Initialisation de Zoho CRM
    ZohoCRMContactCreator.initialize_zoho_crm()

    # Appel de l'API Catfact pour obtenir la liste des races de chats
    response = requests.get("https://catfact.ninja/breeds")
    if response.status_code == 200:
        breeds = response.json()
        if breeds and "data" in breeds:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(ZohoCRMContactCreator.create_contact_if_not_exists, (breed["breed"] for breed in breeds["data"] if "origin" in breed and breed["origin"] == "Natural"))
    else:
        print("Erreur lors de l'appel de l'API Catfact.")

if __name__ == "__main__":
    main()
