class DataValidationSystem(object):
    def validate_data(self, type, data: dict) -> list:
        switcher = {
            'get_countries': self.__countries_validator,
            'get_summary': self.__countries_summary_validator,
            'get_total_day_one': self.__total_daily,
            'daily': self.__daily
        }
        func = switcher.get(type)
        return func(data)

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

    def __total_daily(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    new_item = [f"total:{item.get('Country')}:{self.__validate_date(item.get('Date'))}", {
                        'Confirmed': item.get('Confirmed'),
                        'Deaths': item.get('Deaths'),
                        'Recovered': item.get('Recovered'),
                        'Active': item.get('Active')
                    }]
                    validated_data.append(new_item)
        return validated_data

    def __daily(self, data) -> list:
        validated_data = []
        if data is not None:
            prev = {
                'Confirmed': 0,
                'Deaths': 0,
                'Recovered': 0
            }
            for item in data:
                if isinstance(item, dict):
                    new_item = [f"{item.get('Country')}:{self.__validate_date(item.get('Date'))}", {
                        'Confirmed': item.get('Confirmed') - prev.get('Confirmed'),
                        'Deaths': item.get('Deaths') - prev.get('Deaths'),
                        'Recovered': item.get('Recovered') - prev.get('Recovered')
                    }]
                    validated_data.append(new_item)
                    prev = item
        return validated_data


    def __validate_date(self, date: str):
        return date[:-10]
