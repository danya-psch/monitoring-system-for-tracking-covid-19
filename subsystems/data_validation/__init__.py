class DataValidationSystem(object):
    def validate_data(self, type, data: dict) -> list:
        switcher = {
            'get_countries': self.__countries_validator,
            'get_summary': self.__countries_summary_validator,
            'get_total_for_country': self.__total_for_country,
            'get_daily_for_country': self.__daily_for_country
        }
        func = switcher.get(type)
        return func(data) if func is not None else []

    def __countries_validator(self, data) -> list:

        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    validated_data.append(item.get('Country'))
        return validated_data

    def __countries_summary_validator(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    new_item = [f"country:{item.get('Country')}", {
                        'CountryCode': item.get('CountryCode'),
                        'Slug': item.get('Slug'),
                        'NewConfirmed': item.get('NewConfirmed'),
                        'TotalConfirmed': item.get('TotalConfirmed'),
                        'NewDeaths': item.get('NewDeaths'),
                        'TotalDeaths': item.get('TotalDeaths'),
                        'NewRecovered': item.get('NewRecovered'),
                        'TotalRecovered': item.get('TotalRecovered'),
                        'Date': item.get('Date'),
                    }]
                    validated_data.append(new_item)
        return validated_data

    def __total_for_country(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    new_item = [f"total:{item.get('Country')}:{self.__validate_date(item.get('Date'))}", {
                        'Confirmed': item.get('Confirmed'),
                        'Deaths': item.get('Deaths'),
                        'Recovered': item.get('Recovered')
                    }]
                    validated_data.append(new_item)
        return validated_data

    def __daily_for_country(self, data) -> list:
        validated_data = []
        if data is not None:
            prev = {
                'Confirmed': 0,
                'Deaths': 0,
                'Recovered': 0
            }
            for item in data:
                if isinstance(item, dict):
                    confirmed = item.get('Confirmed') - prev.get('Confirmed') if item.get('Confirmed') - prev.get('Confirmed') > 0 else 0
                    deaths = item.get('Deaths') - prev.get('Deaths') if item.get('Deaths') - prev.get('Deaths') > 0 else 0
                    recovered = item.get('Recovered') - prev.get('Recovered') if item.get('Recovered') - prev.get('Recovered') > 0 else 0

                    new_item = [f"{item.get('Country')}:{self.__validate_date(item.get('Date'))}", {
                        'Confirmed': confirmed,
                        'Deaths': deaths,
                        'Recovered': recovered
                    }]
                    validated_data.append(new_item)
                    prev = {
                        'Confirmed': item.get('Confirmed'),
                        'Deaths': item.get('Deaths'),
                        'Recovered': item.get('Recovered')
                    }
        return validated_data

    def __validate_date(self, date: str):
        return date[:-10]
