import time


class TimerCore:
    def __init__(self, on_tick, on_finish):
        self.on_tick = on_tick
        self.on_finish = on_finish

        self._duration = 0
        self._remaining = 0
        self._running = False
        self._start_time = None

    def start(self, duration: int):
        self._duration = duration
        self._remaining = duration
        self._start_time = time.time()
        self._running = True

    def stop(self):
        self._running = False

    def reset(self):
        self._remaining = self._duration
        self._start_time = time.time()

    def update(self):
        if not self._running:
            return

        elapsed = int(time.time() - self._start_time)
        self._remaining = max(self._duration - elapsed, 0)

        if self._remaining == 0:
            self._running = False
            self.on_finish()
        else:
            self.on_tick(self._remaining)

    def is_running(self):
        return self._running