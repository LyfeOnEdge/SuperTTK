import time
import signal
import argparse
import threading
import multiprocessing
from collections import deque


class Threader:
    def __init__(self, max_worker_threads: int = 3):
        self.queue = deque()
        self.threads = deque()
        self.soft_exit = True  # Var to keep track of soft or hard exit status, hitting ctrl+c once will allow builds to finish, hitting it again will result in a hard exit killing the spin threads
        self.kill_ran = False  # Var to keep track of if of thread kill has been run

        self.max_worker_threads = max_worker_threads
        self.watchdogrunning = True
        self.stopwatchdog = False  # Flag to stop the loop thread

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

        # Call mainloop
        self._update_running_threads()

    def add(self, callback, arglist: list = []):
        """Add a callback to be done as a thread with an optional arglist"""
        t = multiprocessing.Process(target=callback, args=arglist)
        # t.daemon = True
        self.queue.append(t)

    # Not to be called by user
    def _update_running_threads(self):
        if self.stopwatchdog:
            self.watchdogrunning = False
            return

        self.clear_dead_threads()

        while self.queue and len(self.threads) < self.max_worker_threads:
            t = self.queue.popleft()
            t.start()
            self.threads.append(t)

        if not self.stopwatchdog:
            self.watchdog = threading.Timer(
                0.1, self._update_running_threads
            )  # Runs every 100 milliseconds
            self.watchdog.start()

    def clear_dead_threads(self):
        if self.threads:
            for t in list(self.threads):
                if not t.is_alive():
                    self.threads.remove(t)

    def kill_threads(self):
        if not self.kill_ran:
            self.kill_ran = True
            print("Killing all worker threads.")
            if self.threads:
                for t in list(self.threads):
                    t.terminate()

    def exit(self, _=None, __=None):
        if self.soft_exit:
            # The first time through stop the watchdog which actually just prevents the watchdog thread from being respawning
            # This will allow the current watchdog thread to allow the currently running worker threads to complete
            # Calling this function again will cause a hard exit by killing the worker threads and raising KeyboardInterrupt
            self.soft_exit = False
            self.join()
            print("\nThreader Info - Stopping watchdog")
            self.stopwatchdog = True
            while self.watchdogrunning:
                time.sleep(0.5)
            print("Threader Info - Watchdog stopped")
        else:
            self.kill_threads()
            raise KeyboardInterrupt("Killed by user.")

    def join(self):
        for t in self.threads:
            t.join()
