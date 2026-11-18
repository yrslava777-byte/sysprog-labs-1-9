import sys
import threading
import time


def work(count):
    for _ in range(count):
        pass


print(f"Python {sys.version.split()[0]}, GIL {'on' if sys._is_gil_enabled() else 'off'}", flush=True)
for workers in (1, 2, 4):
    start = time.perf_counter()
    threads = [threading.Thread(target=work, args=(200_000_000 // workers,))
               for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"{workers}: {time.perf_counter() - start:.3f} s", flush=True)
