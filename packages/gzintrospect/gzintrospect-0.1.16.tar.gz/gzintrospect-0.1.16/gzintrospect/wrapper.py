import time


def timeit(fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("[timeit] start running function [%s]" % fn.__name__)
        output = fn(*args, **kwargs)
        print("[timeit] finish running function [%s], time elapsed = %.3f secs" %
                        (fn.__name__, time.time() - start_time))
        return output
    return wrapper


