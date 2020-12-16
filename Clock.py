import time


class Clock:
    def __init__(self):
        self.is_running = False
        self.stop_time = 0

    # makes time flowing
    def start(self, period):
        """
        :param period: update time
        """
        self.is_running = True
        self.stop_time = time.time() + period

    # stops time flowing
    def update(self):
        if time.time() > self.stop_time:
            self.is_running = False