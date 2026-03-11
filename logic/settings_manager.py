class SettingsManager:
    def __init__(self, storage):
        self.storage = storage
    
    def get_settings(self):
        """Получить настройки"""
        return self.storage.get_settings()
    
    def update_settings(self, new_settings):
        """Обновить настройки"""
        self.storage.update_settings(new_settings)
        self.storage.save()
    
    def reset_to_defaults(self):
        """Сбросить к настройкам по умолчанию"""
        default = {
            "weekly_goal": 200,
            "notifications": True,
            "theme": "light"
        }
        self.storage.update_settings(default)
        self.storage.save()