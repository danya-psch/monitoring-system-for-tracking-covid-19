from controller import Controller

menu_list = {
    'Main menu': {
        'Subsystems settings': Controller.subsystems_settings,
        'Exit': Controller.stop_loop,
    }
}
