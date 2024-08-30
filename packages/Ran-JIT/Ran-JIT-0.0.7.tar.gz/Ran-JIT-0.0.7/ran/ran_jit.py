import numba
import numpy as np
import inspect
import os
import psutil
import platform
from concurrent.futures import ThreadPoolExecutor

# Cache for storing results of process_chunk
cache = {}

@numba.njit
def chunk_data(data, chunk_size):
    """
    Splits data into chunks of specified size.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def process_chunk(chunk):
    """
    Process a chunk of data. This function should contain the actual computation logic.
    Uses manual caching to avoid reprocessing the same chunk multiple times.
    """
    # Convert chunk to a tuple so it can be used as a key in the cache
    chunk_key = tuple(chunk)
    if chunk_key in cache:
        return cache[chunk_key]
    
    result = sum(chunk)  # Example operation
    
    # Store the result in the cache
    cache[chunk_key] = result
    return result

def threaded_processing(data, chunk_size=100, max_workers=4):
    """
    Process data in parallel using threads, by splitting the data into chunks.
    """
    data = np.asarray(data)  # Ensure data is a NumPy array
    chunks = list(chunk_data(data, chunk_size))  # JIT-compiled function
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_chunk, chunks))
    return results

def apply_jit_to_all_functions(module_globals):
    """
    Apply JIT compilation to user-defined functions selectively, only if they benefit from JIT.
    """
    for name, obj in module_globals.items():
        if inspect.isfunction(obj) and name != 'apply_jit_to_all_functions':
            if name in ['optimize_system_resources', 'threaded_processing']:
                print(f"RAN LIB : Skipping JIT for {name} as it uses unsupported constructs.")
                continue

            try:
                source_code = inspect.getsource(obj)
                num_loops = source_code.count('for ') + source_code.count('while ')
                
                # Apply JIT if the function has loops or numpy operations
                if num_loops > 0 or 'np.' in source_code:
                    print(f"RAN LIB : JIT applied to {name}.")
                    module_globals[name] = numba.njit(obj, cache=True)
                else:
                    print(f"RAN LIB : Skipping JIT for {name} due to low complexity.")
            except Exception as e:
                print(f"RAN LIB : Skipping JIT for {name}: {e}")

def optimize_system_resources():
    """
    Adjusts system resources to give the process more priority, 
    potentially improving performance for CPU-bound tasks.
    """
    p = psutil.Process(os.getpid())
    system_platform = platform.system()

    try:
        if system_platform == "Windows":
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("RAN LIB : Process priority set to high (Windows).")
        else:
            p.nice(-10)  # Unix systems: -20 is highest priority, 19 is lowest
            print("RAN LIB : Process priority increased (Unix).")
    except AttributeError:
        print("RAN LIB : Unable to set high priority, feature not supported.")
    except psutil.AccessDenied:
        print("RAN LIB : Permission denied. Unable to change process priority. Try running as an administrator.")
    except Exception as e:
        print(f"RAN LIB : Failed to optimize system resources: {e}")

def ran():
    """
    Function to trigger JIT application and system resource optimization.
    """
    apply_jit_to_all_functions(globals())
    optimize_system_resources()
