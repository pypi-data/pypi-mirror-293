from .ran_jit import apply_jit_to_all_functions, optimize_system_resources, RanLib

# Automatically apply JIT to all functions in the module's global scope
apply_jit_to_all_functions(globals())

# Optimize system resources for the current process
optimize_system_resources()

# Add the discord boosting function to the module's namespace
discord = RanLib.discord
