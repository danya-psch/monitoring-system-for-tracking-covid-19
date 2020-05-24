import requests

url = 'https://api.covid19api.com'


def get(local_url):
    return requests.get(url=local_url).json()


# Get List Of Countries
def get_countries():
    local_url = url + '/countries'
    return get(local_url)


# Get List Of Cases Per Country Per Province By Case Type From The First Recorded Case
def get_day_one(country):
    local_url = url + f"/dayone/country/{country}"
    return get(local_url)


# Get List Of Cases Per Country By Case Type From The First Recorded Case
def get_total_day_one(country):
    local_url = url + f"/total/dayone/country/{country}"
    return get(local_url)


# Get List Of Cases Per Country Per Province By Case Type
def get_country(country):
    local_url = url + f"/country/{country}"
    return get(local_url)


# Get List Of Cases Per Country Per Province By Case Type From The First Recorded Case, updated with latest live count
def get_country_status_day_one_live(country, status):
    local_url = url + f"/dayone/country/{country}/status/{status}/live"
    return get(local_url)


# Get List Of Cases Per Country Per Province By Case Type From The First Recorded Case
def get_country_status_day_one(country, status):
    local_url = url + f"/dayone/country/{country}/status/{status}"
    return get(local_url)


# Get List Of Cases Per Country By Case Type From The First Recorded Case
def get_country_status_day_one_total(country, status):
    local_url = url + f"/total/dayone/country/{country}/status/{status}"
    return get(local_url)


# Daily list of cases per Country per Province by Case Type, updated with latest live count
def get_status_live(country, status):
    local_url = url + f"/country/{country}/status/{status}/live"
    return get(local_url)


# Get List Of Cases Per Country Per Province By Case Type
def get_status(country, status):
    local_url = url + f"/country/{country}/status/{status}"
    return get(local_url)


# Get List Of Cases Per Country By Case Type
def get_status_total(country, status):
    local_url = url + f"/total/country/{country}/status/{status}"
    return get(local_url)


# Get List Of Cases Per Country By Case Type
def get_total(country):
    local_url = url + f"/total/country/{country}"
    return get(local_url)


# Get Live List Of Cases Per Country Per Province By Case Type
def get_live_country(country):
    local_url = url + f"/live/country/{country}"
    return get(local_url)


# Get a Time Series Of Cases Per Country Per Province By Case Type After A Date
def get_live_country_status_after_date(country, date):
    local_url = url + f"/live/country/{country}/status/:status/date/{date}"
    return get(local_url)


# Get a time series Of Cases Per Country Per Province By Case Type
def get_live_country_status(country, status):
    local_url = url + f"/live/country/{country}/status/{status}"
    return get(local_url)


# Summary of new and total cases per country
def get_summary() -> list:
    local_url = url + '/summary'
    return get(local_url).get('Countries')

