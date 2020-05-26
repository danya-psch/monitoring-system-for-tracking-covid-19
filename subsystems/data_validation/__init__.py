class DataValidationSystem(object):
    def __init__(self):
        self._prev = {}

    def validate_data(self, type, data: dict) -> list:
        switcher = {
            'get_countries': self._countries_validator,
            'get_summary': self._countries_summary_validator,
            'get_daily_for_country': self.daily_for_country,
            'get_total_for_country': self._total_for_country,
        }
        func = switcher.get(type)
        return func(data) if func is not None else []

    def _countries_validator(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    validated_data.append(item.get('Country'))
        return validated_data

    def _countries_summary_validator(self, data) -> list:
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

    def _total_for_country(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if isinstance(item, dict):
                    new_item = [f"total:{item.get('Country')}:{self._validate_date(item.get('Date'))}", {
                        'Confirmed': item.get('Confirmed'),
                        'Deaths': item.get('Deaths'),
                        'Recovered': item.get('Recovered')
                    }]
                    validated_data.append(new_item)
        return validated_data

    def daily_for_country(self, data) -> list:
        validated_data = []
        if data is not None:
            for item in data:
                if item.get('Country') not in self._prev:
                    self._prev[item.get('Country')] = (0, 0, 0)
                if isinstance(item, dict):
                    prev_confirmed, prev_deaths, prev_recovered = self._prev[item.get('Country')]
                    confirmed = item.get('Confirmed') - prev_confirmed \
                        if item.get('Confirmed') - prev_confirmed > 0 else 0
                    deaths = item.get('Deaths') - prev_deaths \
                        if item.get('Deaths') - prev_deaths > 0 else 0
                    recovered = item.get('Recovered') - prev_recovered \
                        if item.get('Recovered') - prev_recovered > 0 else 0
                    new_item = (f"{item.get('Country')}:{self._validate_date(item.get('Date'))}", {
                        'Confirmed': confirmed,
                        'Deaths': deaths,
                        'Recovered': recovered
                    })

                    self._prev[item.get('Country')] = (item.get('Confirmed'), item.get('Deaths'), item.get('Recovered'))
                    # print(f"item: [c:{str(item.get('Confirmed'))}, d:{str(item.get('Deaths'))}, r:{str(item.get('Recovered'))}], confirmed:{confirmed}, deaths:{deaths}, recovered:{recovered}"
                    #       f" prev_confirmed:{prev_confirmed}, prev_deaths:{prev_deaths}, prev_recovered:{prev_recovered}, {item.get('Country')}:{self._validate_date(item.get('Date'))}")
                    validated_data.append(new_item)


        return validated_data

    def _validate_date(self, date: str):
        return date[:-10]
