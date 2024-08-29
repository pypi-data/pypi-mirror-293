import cProfile
import pstats
import io
import traceback

def profile(func):
    def wrapper(*args, **kwargs):
        print(f"Profiler: Starting to profile {func.__name__}")
        pr = cProfile.Profile()
        pr.enable()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred in {func.__name__}:")
            print(traceback.format_exc())
            result = None
        finally:
            pr.disable()
            print(f"Profiler: Finished profiling {func.__name__}")
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(20)  # Print top 20 time-consuming functions
            print("Profiler results:")
            print(s.getvalue())
        return result
    return wrapper