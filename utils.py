import urllib
import requests


# Starting data to pull records
lastModifiedStartDate_date = urllib.parse.quote("1500-01-28T20:18:10Z")
API_KEY = "Yr0j8PyPyI2xPRhvpMP4Yy85HEaf7FVgGA3eNm2O"

shared_params = {
    "api_key": API_KEY,
}


def govinfo_download(url, params=None, as_json=True):
    combined_params = shared_params.copy()

    if params:
        combined_params.update(params)

    r = requests.get(url, params=combined_params)

    if not r.ok:
        print(url, combined_params)
        print(r.content)
        print(r.status_code)
        exit()

    if as_json:
        return r.json()

    return r.content


def get_collection_page(collection, offset):

    base_url = "https://api.govinfo.gov/collections"
    url = base_url + f"/{collection}/{lastModifiedStartDate_date}"

    return govinfo_download(url, {"offset": offset, "pageSize": 100})


def get_package_page(packageID):

    base_url = "https://api.govinfo.gov/packages"
    url = base_url + f"/{packageID}/summary"

    return govinfo_download(url)
