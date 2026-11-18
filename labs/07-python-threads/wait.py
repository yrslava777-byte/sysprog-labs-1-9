import threading
import time


for workers in (1, 4):
    start = time.perf_counter()
    threads = [threading.Thread(target=time.sleep, args=(2,)) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"{workers}: {time.perf_counter() - start:.3f} s", flush=True)
