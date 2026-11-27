import time

def set_timer(function, interval=1.0, count : int = 10):
    for _ in range(count):
        function()
        time.sleep(interval)

    return function()

def pr():
    print("ef")

set_timer(pr, 1, 5)