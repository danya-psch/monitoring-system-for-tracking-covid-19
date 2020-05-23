from redis_server import RedisServer
from subsystems.data_backup import DataBackupSystem
from subsystems.data_generation import DataGenerationSystem
from subsystems.data_recovery import DataRecoverySystem
from subsystems.data_validation import DataValidationSystem


class SubSystemsController(object):
    def __init__(self, redis_server: RedisServer):
        self.__rserver = redis_server

        self.__data_backup_system = DataBackupSystem()
        self.__rserver.set_data_backup_system(self.__data_backup_system)

        self.__data_generation_system = DataGenerationSystem(self.__rserver)
        self.__data_recovery_system = DataRecoverySystem()
        self.__data_validation_system = DataValidationSystem()

        # test actions
        self.generate_data()

    @property
    def dbs(self) -> DataBackupSystem:
        return self.__data_backup_system

    @property
    def dgs(self) -> DataGenerationSystem:
        return self.__data_generation_system

    @property
    def drs(self) -> DataRecoverySystem:
        return self.__data_recovery_system

    @property
    def dvs(self) -> DataValidationSystem:
        return self.__data_validation_system

    @property
    def data_backup_system_activity(self) -> bool:
        return self.__data_backup_system.active

    @data_backup_system_activity.setter
    def data_backup_system_activity(self, value: bool):
        self.__data_backup_system.active = value

    def generate_data(self):
        validated_data = self.__data_validation_system.validate_data(
            **self.__data_generation_system.generate_countries()
        )
        for country in validated_data:
            self.generate_days_for_country(country)

    def generate_days_for_country(self, country):
        days = self.__data_validation_system.validate_data(
            **self.__data_generation_system.generate_total_days(country)
        )
        for day in days:
            date = day['Date'][:-10]
            del day['Date']
            self.__rserver.write_down([
                f"{country}:{date}",
                day
            ])

    def generate_countries(self):
        generated_data = self.__data_generation_system.generate_summary()
        validated_data = self.__data_validation_system.validate_data('type', generated_data)
        # for data_item in validated_data:
        # action = lambda item: [
        #     f"country:{item['Country']}",
        #     {
        #         'country_code': item['CountryCode'],
        #         'slug': item['Slug'],
        #         'new_confirmed': item['NewConfirmed'],
        #         'total_confirmed': item['TotalConfirmed'],
        #         'new_deaths': item['NewDeaths'],
        #         'total_deaths': item['TotalDeaths'],
        #         'new_recovered': item['NewRecovered'],
        #         'total_recovered': item['TotalRecovered'],
        #         'date': item['Date']
        #     }
        # ]
        # action = self.__make_action(data_item)
        # self.__rserver.write_down(action, data_item)
        #     self.__data_backup_system.write_down(validated_data)
