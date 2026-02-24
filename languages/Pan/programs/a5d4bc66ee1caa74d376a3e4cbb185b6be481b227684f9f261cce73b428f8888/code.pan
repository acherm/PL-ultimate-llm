# Pan configuration language example
# Demonstrates template structure and configuration tree manipulation

object template example_node;

# Node hardware configuration
variable HOSTNAME = 'node01.example.org';
variable NUM_CPUS = 4;
variable MEM_MB = 8192;

# Populate the configuration tree
'/system/hostname' = HOSTNAME;
'/hardware/cpu/count' = NUM_CPUS;
'/hardware/memory/total_mb' = MEM_MB;

# Compute derived values
'/hardware/memory/swap_mb' = MEM_MB / 2;

# Function to build a package entry
function make_pkg = {
    dict('version', ARGV[0], 'arch', 'x86_64');
};

# Software configuration
'/software/packages/{bash}' = make_pkg('5.1');
'/software/packages/{vim}' = make_pkg('8.2');
'/software/packages/{git}' = make_pkg('2.34');

# System description using format
'/system/description' = format(
    '%s: %d CPUs, %d MB RAM', HOSTNAME, NUM_CPUS, MEM_MB
);
