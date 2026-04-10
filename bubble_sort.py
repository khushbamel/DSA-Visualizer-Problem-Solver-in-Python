import time
import os
import random

# ─────────────────────────────────────────
#  SETTINGS  — tweak these freely
# ─────────────────────────────────────────
ARRAY_SIZE   = 15       # how many elements
MAX_VALUE    = 30       # max bar height
SLEEP_TIME   = 0.15     # seconds between each step (lower = faster)
BAR_CHAR     = "█"      # character used to draw bars

# ─────────────────────────────────────────
#  ANSI colour codes
# ─────────────────────────────────────────
RED    = "\033[91m"   # currently comparing
GREEN  = "\033[92m"   # confirmed sorted
YELLOW = "\033[93m"   # just swapped
BLUE   = "\033[94m"   # normal unsorted
CYAN   = "\033[96m"   # headers / labels
BOLD   = "\033[1m"
RESET  = "\033[0m"


def clear():
    """Clear the terminal screen on any OS."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(comparisons, swaps, current_pass, total_passes):
    """Print the stats bar at the top of every frame."""
    print(f"{CYAN}{BOLD}{'─' * 50}{RESET}")
    print(f"{CYAN}{BOLD}  BUBBLE SORT VISUALIZER{RESET}")
    print(f"{CYAN}{'─' * 50}{RESET}")
    print(
        f"  {BOLD}Comparisons:{RESET} {comparisons:<6}"
        f"  {BOLD}Swaps:{RESET} {swaps:<6}"
        f"  {BOLD}Pass:{RESET} {current_pass} / {total_passes}"
    )
    print(f"{CYAN}{'─' * 50}{RESET}\n")


def print_array(arr, highlight1=None, highlight2=None, sorted_from=None):
    """
    Draw each element as a horizontal bar of block characters.

    highlight1 / highlight2 → shown in RED  (being compared)
    sorted_from onwards     → shown in GREEN (confirmed sorted)
    everything else         → shown in BLUE  (unsorted)
    """
    sorted_from = sorted_from if sorted_from is not None else len(arr)

    for i, val in enumerate(arr):
        if i == highlight1 or i == highlight2:
            color = RED
        elif i >= sorted_from:
            color = GREEN
        else:
            color = BLUE

        # index label | coloured bar | numeric value
        bar = BAR_CHAR * val
        print(f"  [{i:>2}]  {color}{bar:<{MAX_VALUE}}{RESET}  {val}")

    print()


def print_legend():
    """Show a colour legend at the bottom of every frame."""
    print(
        f"  {BLUE}█ unsorted{RESET}   "
        f"{RED}█ comparing{RESET}   "
        f"{YELLOW}█ swapped{RESET}   "
        f"{GREEN}█ sorted{RESET}"
    )
    print()


def bubble_sort(arr):
    """
    Bubble sort with:
      - full step-by-step visualisation
      - early-exit optimisation (best case O(n))
      - swap count and comparison count tracking
      - per-pass progress display
    """
    n            = len(arr)
    comparisons  = 0
    swaps        = 0
    total_passes = n - 1

    for i in range(n - 1):
        current_pass    = i + 1
        swapped_this_pass = False

        for j in range(n - i - 1):

            # ── STEP 1: show the comparison ──────────────────
            comparisons += 1
            clear()
            print_header(comparisons, swaps, current_pass, total_passes)
            print(f"  {CYAN}Comparing  index {j} ({arr[j]})  vs  index {j+1} ({arr[j+1]}){RESET}\n")
            print_array(arr, highlight1=j, highlight2=j+1, sorted_from=n - i)
            print_legend()
            time.sleep(SLEEP_TIME)

            # ── STEP 2: swap if out of order ─────────────────
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps            += 1
                swapped_this_pass = True

                clear()
                print_header(comparisons, swaps, current_pass, total_passes)
                print(f"  {YELLOW}Swapped!   index {j} ↔ index {j+1}{RESET}\n")
                print_array(arr, highlight1=j, highlight2=j+1, sorted_from=n - i)
                print_legend()
                time.sleep(SLEEP_TIME)

        # ── after each pass: one element is confirmed sorted ─
        clear()
        print_header(comparisons, swaps, current_pass, total_passes)
        print(f"  {GREEN}Pass {current_pass} complete  —  rightmost {i+1} element(s) sorted{RESET}\n")
        print_array(arr, sorted_from=n - i - 1)
        print_legend()
        time.sleep(SLEEP_TIME * 2)

        # ── early exit optimisation ───────────────────────────
        if not swapped_this_pass:
            clear()
            print_header(comparisons, swaps, current_pass, total_passes)
            print(f"  {GREEN}{BOLD}Early exit! No swaps in pass {current_pass}.{RESET}")
            print(f"  {CYAN}Array is already sorted — no more passes needed.{RESET}\n")
            print_array(arr, sorted_from=0)
            print_legend()
            time.sleep(SLEEP_TIME * 3)
            break

    return comparisons, swaps


def print_final(arr, comparisons, swaps, elapsed):
    """Display the final sorted result with a summary."""
    clear()
    print(f"{CYAN}{BOLD}{'─' * 50}{RESET}")
    print(f"{GREEN}{BOLD}  SORTING COMPLETE!{RESET}")
    print(f"{CYAN}{'─' * 50}{RESET}\n")
    print_array(arr, sorted_from=0)
    print(f"{CYAN}{'─' * 50}{RESET}")
    print(f"  {BOLD}Total comparisons :{RESET} {comparisons}")
    print(f"  {BOLD}Total swaps       :{RESET} {swaps}")
    print(f"  {BOLD}Time taken        :{RESET} {elapsed:.2f} seconds")
    print(f"  {BOLD}Array size        :{RESET} {len(arr)}")
    print(f"{CYAN}{'─' * 50}{RESET}\n")


# ─────────────────────────────────────────
#  MAIN — entry point
# ─────────────────────────────────────────
def main():
    # generate a random array
    arr = [random.randint(1, MAX_VALUE) for _ in range(ARRAY_SIZE)]

    # show the unsorted array first
    clear()
    print(f"{CYAN}{BOLD}{'─' * 50}{RESET}")
    print(f"{CYAN}{BOLD}  BUBBLE SORT VISUALIZER{RESET}")
    print(f"{CYAN}{'─' * 50}{RESET}\n")
    print(f"  {BOLD}Unsorted array:{RESET}\n")
    print_array(arr)
    print_legend()
    print(f"  Press ENTER to start sorting...")
    input()

    # run the sort and time it
    start_time              = time.time()
    comparisons, swaps      = bubble_sort(arr)
    elapsed                 = time.time() - start_time

    # show the final summary
    print_final(arr, comparisons, swaps, elapsed)


if __name__ == "__main__":
    main()
