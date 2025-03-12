import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs) 
        end_time = time.time()
        execution_time = end_time - start_time 
        print(f"TIME: [{func.__name__}] executed in {execution_time:.6f} seconds.")
        return result
    return wrapper

