import cProfile
import pstats
import log

def main():
    for x in range(10000):

        log.debug(x)


if __name__ == "__main__":
    profiler = cProfile.Profile()

    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('tottime')
    stats.print_stats(30)
