import argparse
import time

def waste_time(n):
    time.sleep(n)
    print(f"Congratulations, you wasted {n} seconds!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Waster")
    parser.add_argument('-t', '--time', help="amount of time to waste", type=int, required=True)
    pargs = parser.parse_args()

    waste_time(pargs.time)