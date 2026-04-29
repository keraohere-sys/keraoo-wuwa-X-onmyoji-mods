
import pyautogui
import random
import time
import sys
import math

# ===== CONFIG =====
WINDOW_OFFSET_X = 0
WINDOW_OFFSET_Y = 0

CLICK_STEPS = [
    {"name": "Step1: Challenge button", "x": 1310, "y": 790, "rand": 10, "delay_after": (0.5, 1.2), "repeat": (1, 3)},
    {"name": "Step2: Battle button", "x": 1330, "y": 770, "rand": 20, "delay_after": (12, 17), "repeat": (1, 2)},
    {"name": "Step3: Confirm result", "x": 1050, "y": 600, "rand": 8, "delay_after": (0.8, 2), "repeat": (1, 3)},
    # {"name": "Step4: Exitbattle result", "x": 1000, "y": 650, "rand": 20, "delay_after": (0.5, 2), "repeat": (1, 2)},
]

TOTAL_ROUNDS = random.randint(25, 50)

EXTRA_DELAY_MIN = 0.4
EXTRA_DELAY_MAX = 2.0

pyautogui.FAILSAFE = True

TOTAL_ROUNDS = random.randint(25, 50)

EXTRA_DELAY_MIN = 0.2
EXTRA_DELAY_MAX = 1.2

pyautogui.FAILSAFE = True


def human_like_move(x, y):
    start_x, start_y = pyautogui.position()

    dist = math.hypot(x - start_x, y - start_y)
    duration = max(0.08, min(0.25, dist / 3500))

    cp1 = (
        start_x + random.randint(-100, 100),
        start_y + random.randint(-100, 100)
    )
    cp2 = (
        x + random.randint(-100, 100),
        y + random.randint(-100, 100)
    )

    steps = random.randint(15, 25)
    start_time = time.time()

    for i in range(steps):
        t = i / steps
        t = t * t * (3 - 2 * t)

        xt = (1 - t)**3 * start_x \
           + 3 * (1 - t)**2 * t * cp1[0] \
           + 3 * (1 - t) * t**2 * cp2[0] \
           + t**3 * x

        yt = (1 - t)**3 * start_y \
           + 3 * (1 - t)**2 * t * cp1[1] \
           + 3 * (1 - t) * t**2 * cp2[1] \
           + t**3 * y

        xt += random.uniform(-1.2, 1.2)
        yt += random.uniform(-1.2, 1.2)

        pyautogui.moveTo(xt, yt)

        elapsed = time.time() - start_time
        remaining = duration - elapsed
        if remaining > 0:
            time.sleep(remaining / (steps - i))


def random_click(x, y, rand=10):
    rx = x + WINDOW_OFFSET_X + random.randint(-rand, rand)
    ry = y + WINDOW_OFFSET_Y + random.randint(-rand, rand)

    human_like_move(rx, ry)

    if random.random() < 0.25:
        pyautogui.moveRel(random.randint(-4, 4), random.randint(-4, 4), duration=0.04)

    time.sleep(random.uniform(0.02, 0.08))
    pyautogui.click()

    print("clicked: ({}, {})".format(rx, ry))


def run():
    print("Script starting in 3 seconds... switch to emulator now!")
    time.sleep(3)

    round_count = 0

    while True:
        round_count += 1

        if TOTAL_ROUNDS > 0 and round_count > TOTAL_ROUNDS:
            print("Done! {} rounds completed.".format(TOTAL_ROUNDS))
            break

        print("\nRound {}".format(round_count))

        for step in CLICK_STEPS:
            print(" -> {}".format(step["name"]))

            times = random.randint(step["repeat"][0], step["repeat"][1])

            for t in range(times):
                random_click(step["x"], step["y"], step["rand"])

                if t == times - 2 and random.random() < 0.35:
                    idle = random.uniform(0.4, 1.6)
                    print(f"   thinking pause {idle:.2f}s")
                    time.sleep(idle)

                if t < times - 1:
                    time.sleep(random.uniform(0.08, 0.35))

            d = step["delay_after"]
            wait = random.uniform(d[0], d[1]) + random.uniform(0.2, 1.2)

            time.sleep(wait)

            print("clicked {} time(s)".format(times))

        print("Round {} done.".format(round_count))


if __name__ == "__main__":
    try:
        run()
    except pyautogui.FailSafeException:
        print("Failsafe triggered. Exiting.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("Interrupted. Exiting.")
        sys.exit(0)