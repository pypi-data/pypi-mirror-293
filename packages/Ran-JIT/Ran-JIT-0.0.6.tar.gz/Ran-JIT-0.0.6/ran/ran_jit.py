import numba
import inspect
import os
import psutil
import platform

def apply_jit_to_all_functions(module_globals):
    """
    Apply JIT compilation to user-defined functions selectively, only if they benefit from JIT.
    """
    for name, obj in module_globals.items():
        if inspect.isfunction(obj) and name != 'apply_jit_to_all_functions':
            if name == 'optimize_system_resources':
                print(f"RAN LIB : Skipping JIT for {name} as it handles system resources.")
                continue
            
            try:
                source_code = inspect.getsource(obj)
                num_loops = source_code.count('for ') + source_code.count('while ')
                
                if num_loops > 0 or 'np.' in source_code:
                    print(f"RAN LIB : JIT applied to {name}.")
                    module_globals[name] = numba.njit(obj, nopython=True, cache=True)
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

if __name__ != "__main__":
    apply_jit_to_all_functions(globals())
    optimize_system_resources()
