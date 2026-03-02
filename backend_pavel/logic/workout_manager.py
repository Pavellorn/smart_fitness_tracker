from datetime import datetime
from logic.storage_manager import StorageManager

class WorkoutManager:
    def __init__(self, storage):
        self.storage = storage    
    
    
    def start(self, duration: int):
        if current["is_active"]:
            return
        current = self.storage.get_current_workout()
        current["is_active"] = True
        current["selected_duration"] = duration
        current["started_at"] =  datetime.now().isoformat()
        current["paused_at"] =  None
        self.storage.update_current_workout(current)
        
        


