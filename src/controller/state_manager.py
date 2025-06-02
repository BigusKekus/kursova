class StateManager:
    def __init__(self):
        self.current_state = "menu"

    def set_main_menu(self):
        self.current_state = "menu"

    def is_main_menu(self):
        return self.current_state == "menu"

    def set_playing(self):
        self.current_state = "play"

    def is_playing(self):
        return self.current_state == "play"

    def set_paused(self):
        self.current_state = "pause"

    def is_paused(self):
        return self.current_state == "pause"

    def set_game_over(self):
        self.current_state = "game_over"

    def is_game_over(self):
        return self.current_state == "game_over"

    def set_guide(self):
        self.current_state = "guide"

    def is_guide(self):
        return self.current_state == "guide"

    def set_next_level(self):
        self.current_state = "next_level"

    def is_next_level(self):
        return self.current_state == "next_level"

