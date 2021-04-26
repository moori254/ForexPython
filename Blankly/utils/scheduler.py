"""
    Class for the creation of a scheduler in main.
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from Blankly.utils.time_builder import time_interval_to_seconds
import threading
import time
import traceback


class Scheduler:
    def __init__(self, function, interval):
        """
        Wrapper for functions that run at a set interval
        Args:
            function: Function reference to create the scheduler on ex: self.price_event
            interval: int of delay between calls in seconds, or a string that takes units s, m, h, d w, M, y (second,
            minute, hour, day, week, month, year) after a magnitude. Examples: "4s", "6h", "10d":
        """
        if isinstance(interval, str):
            interval = time_interval_to_seconds(interval)

        self.thread = threading.Thread(target=self.threading_wait, args=(function, interval,))
        self.thread.start()

        # Stop flag
        self.stop = False

        # This can be used for a statically typed, single-process bot decorator.
        # Leaving this because it probably will be used soon

        # def decorator(function):
        #     @functools.wraps(function)
        #     def wrapper():
        #         thread = threading.Thread(target=threading_wait, args=(function, interval,))
        #         thread.start()
        #     wrapper()
        # return decorator

    def threading_wait(self, func, interval):
        """
        This function is used with the scheduler decorator
        """
        while True:
            time.sleep(interval)
            # The downside of this is that it keeps the thread running while waiting to stop
            # It's dependent on delay if its more efficient to just check more
            if self.stop:
                break
            try:
                func()
            except Exception:
                traceback.print_exc()

    def kill_scheduler(self):
        self.stop = True