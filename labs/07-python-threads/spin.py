import os
import threading
import time


def spin():
    end = time.time() + 15
    while time.time() < end:
        pass


print("pid", os.getpid(), flush=True)
threads = [threading.Thread(target=spin) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
