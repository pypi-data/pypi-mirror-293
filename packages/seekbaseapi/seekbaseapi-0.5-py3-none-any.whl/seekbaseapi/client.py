import re
import json
import urllib3
import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from typing import List, Dict, Set, Any
from tenacity import retry, wait_fixed, stop_after_attempt
from pydantic import BaseModel, EmailStr

__all__ = ["SeekApiClient"]

urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ExtractedInfo(BaseModel):
    emails: List[EmailStr]
    phones: List[str]
    fivem_licenses: List[str]
    steam_ids: List[str]
    ips: List[str]


class SeekApiClient:
    def __init__(self, api_key: str):
        """
        Initialise le client SeekBase avec la clé API.

        :param api_key: La clé API pour accéder à SeekBase.
        """
        self._host = "api.seekbase.shop"
        self._api_key = api_key
        self.client = self._create_client()

    def _create_client(self) -> Elasticsearch:
        """
        Crée une instance du client SeekBase.

        :return: Instance du client SeekBase.
        :raises ValueError: Si la clé API n'est pas fournie.
        """
        if not self._api_key:
            raise ValueError("Please provide an API key!")
        return Elasticsearch(
            [f"https://{self._host}:9200"],
            api_key=self._api_key,
            verify_certs=False,
        )

    @staticmethod
    def _filter_infos(
        response: Dict[str, Any], include_filename: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Filtre les résultats de la requête API en fonction des éléments de la BLACKLIST et
        inclut ou non le nom du fichier selon le paramètre `include_filename`.

        :param response: Résultat de la requête SeekBase.
        :param include_filename: Booléen pour indiquer si le nom du fichier doit être inclus.
        :return: La liste des résultats filtrés sous forme de dictionnaires.
        """

        results: List[Dict[str, Any]] = []

        for result in response.get("hits", {}).get("hits", []):
            source = result.get("_source", {})
            content = source.get("content", "")
            filename = source.get("filename", "")

            result_dict = {"content": content}
            if include_filename:
                result_dict["filename"] = filename

            results.append(result_dict)

        return results

    @retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
    def search_documents(
        self, search_string: str, display_filename: bool = False, size: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Recherche des documents dans SeekBase en fonction de la chaîne de recherche fournie.

        :param search_string: La chaîne de recherche à utiliser dans la requête.
        :param display_filename: Affiche le nom du fichier si True.
        :param size: Le nombre de résultats à retourner.
        :return: Liste des documents trouvés.
        """
        search_query = {
            "size": size,
            "query": {
                "bool": {
                    "must": {"match_phrase": {"content": search_string}},
                    "must_not": [
                        {"match_phrase": {"content": "</code>"}},
                        {"match_phrase": {"content": "</script>"}},
                    ],
                }
            },
        }

        if display_filename:
            search_query["_source"] = ["filename", "content"]

        try:
            response = self.client.search(index="searcher", body=search_query)
            return self._filter_infos(response, include_filename=display_filename)
        except RequestError as e:
            logging.error(f"Request error: {e.info}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return []

    @staticmethod
    def _format_phone_number(number: str) -> str:
        """
        Formate un numéro de téléphone au format (XXX) XXX-XXXX.

        :param number: Le numéro de téléphone à formater.
        :return: Le numéro de téléphone formaté.
        """
        digits = re.sub(r"\D", "", number)
        if len(digits) != 10:
            return number
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    @staticmethod
    def _extract_information(text: str) -> Dict[str, Set[str]]:
        """
        Extrait les informations spécifiques (emails, numéros de téléphone, identifiants Steam, licences FiveM et adresses IP) à partir du texte.

        :param text: Contenu du texte à analyser.
        :return: Dictionnaire contenant les e-mails, numéros de téléphone, identifiants Steam, licences FiveM, et adresses IP trouvés.
        """
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_pattern = r"\+?\d{1,4}?[\d\s-]{8,}\d"
        ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

        emails = set(re.findall(email_pattern, text))
        phones = set(re.findall(phone_pattern, text))
        ips = set(re.findall(ip_pattern, text))

        steam_ids = set()
        fivem_licenses = set()

        steam_pattern = r"steam:([A-Za-z0-9]+)"
        license_pattern = r"license\d*:(\w{32,})"

        steam_ids.update(re.findall(steam_pattern, text))
        fivem_licenses.update(re.findall(license_pattern, text))

        return {
            "emails": emails,
            "phones": phones,
            "steam_ids": steam_ids,
            "fivem_licenses": fivem_licenses,
            "ips": ips,
        }

    def extracted_search(self, documents: List[Dict[str, Any]]) -> ExtractedInfo:
        """
        Traite les résultats de la recherche pour extraire les informations spécifiques.

        :param documents: Liste des documents trouvés, chaque document contenant le contenu et le nom de fichier.
        :return: Dictionnaire contenant les e-mails, numéros de téléphone, identifiants Steam, licences FiveM, et adresses IP trouvés.
        """
        all_info: Dict[str, Set[str]] = {
            "emails": set(),
            "phones": set(),
            "fivem_licenses": set(),
            "steam_ids": set(),
            "ips": set(),
        }

        for doc in documents:
            content = doc.get("content", "")

            info = self._extract_information(content)
            all_info["emails"].update(info["emails"])
            all_info["phones"].update(info["phones"])
            all_info["steam_ids"].update(info["steam_ids"])
            all_info["fivem_licenses"].update(info["fivem_licenses"])
            all_info["ips"].update(info["ips"])

        formatted_phones = [
            self._format_phone_number(phone) for phone in all_info["phones"]
        ]

        return ExtractedInfo(
            emails=list(all_info["emails"]),
            phones=formatted_phones,
            fivem_licenses=list(all_info["fivem_licenses"]),
            steam_ids=list(all_info["steam_ids"]),
            ips=list(all_info["ips"]),
        )
