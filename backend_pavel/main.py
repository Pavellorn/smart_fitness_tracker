from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from logic.storage_manager import StorageManager
from logic.workout_manager import WorkoutManager
from logic.stats_manager import StatsManager
from logic.settings_manager import SettingsManager



class MainScreen(Screen):
    pass


class StatsScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class SmartFitnessApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_manager = StorageManager()
        self.workout_manager = WorkoutManager()
        self.stats_manager = StatsManager()
        self.settings_manager = SettingsManager()
    
    
    def build(self):
        Builder.load_file("kv_files/main_screen.kv")
        Builder.load_file("kv_files/settings_screen.kv")
        Builder.load_file("kv_files/stats_screen.kv")
        
        screen = ScreenManager()
        screen.add_widget(MainScreen(name="main"))
        screen.add_widget(StatsScreen(name="stats"))
        screen.add_widget(SettingsScreen(name="settings"))
        
        
        return screen


if __name__ == "__main__":
    SmartFitnessApp().run()