class DataValidationSystem(object):
    def __init__(self):
        print("DataValidationSystem")

    def validate_data(self, type, data: dict) -> list:
        switcher = {
            'generate_countries': self.__countries_validator,
            'generate_total_days': self.__total_days_validator
        }
        func = switcher.get(type)
        return func(data)

    def __countries_validator(self, data) -> list:
        validated_data = []
        for item in data:
            validated_data.append(item.get('Country'))
        return validated_data

    def __total_days_validator(self, data) -> list:
        validated_data = []
        for item in data:
            print("!" + str(item) + "!" + str(data) + "!")
            new_item = {
                'Confirmed': item.get('Confirmed'),
                'Deaths': item.get('Deaths'),
                'Recovered': item.get('Recovered'),
                'Active': item.get('Active'),
                'Date': item.get('Date')
            }
            validated_data.append(new_item)
        return validated_data
