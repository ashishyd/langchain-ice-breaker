import os
import requests

from dotenv import load_dotenv

load_dotenv()


def scrap_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from linkedIn profiles.
    manually scrape in information from linkedIn"""

    if mock:
        linkedin_profile_url = (
            "https://gist.githubusercontent.com/ashishyd/40f449011005390991981dc59aafbaf4/raw"
            "/06fbdcf7d81f4f1b3817650695c90d3bf3ef89ee/ashishyd.json"
        )
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"linkedin_profile_url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data

