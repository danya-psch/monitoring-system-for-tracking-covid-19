from controller import Controller
from subsystems.data_generation import DataGenerationSystem

menu_list = {
    'Main menu': {
        # 'Subsystems settings': Controller.subsystems_settings,
        'Statistics total': Controller.statistics_total,
        'Statistics': Controller.statistics,
        'Regression': Controller.regression,
        'Countries statistics': Controller.countries_statistics,
        'Date statistics': Controller.day_statistics,
        'Generate data': Controller.generate_data,
        'Data backup': Controller.backup_data,
        'Data recovery': Controller.recovery_data,
        'Exit': Controller.stop_loop,
    },
    # 'Subsystems menu': {
    #     'Change status of data backup system': Controller.change_data_backup_status,
    #     'Back': Controller.back
    # }
}
