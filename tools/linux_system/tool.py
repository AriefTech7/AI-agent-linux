from .service import LinuxSystem
from langchain_core.tools import tool
service_linux = LinuxSystem()

@tool()
def get_cpu_info():
    """
    Retrieves CPU information 
    such as model, number of cores, threads, and architecture.

    Returns:
        dict: CPU information in a structured format.
    """
    return service_linux.get_cpu_info()
@tool()
def get_hostname():
    """
    Get the hostname of a Linux computer.

    Returns:
        dict: hostname information in a structured format.
    """
    return service_linux.get_hostname()
@tool()
def get_kernel_info():
    """
    Gets the version and information of the currently running Linux kernel.

    Returns:
        dict: kernel information in a structured format.
    """    
    return service_linux.get_kernel_info()
@tool()
def get_os_info():
    """
    Identify 
    Linux distributions, distro versions, 
    and operating system information.

    Returns:
        dict: OS information in a structured format.
    """
    return service_linux.get_os_info()
@tool()
def get_disk_usage():
    """
    Gets total capacity, usage, and free space of the filesystem.

    Returns:
        dict: Disk information in a structured format.
    """
    return service_linux.get_disk_usage()
@tool()
def get_memory_usage():
    """
    Gets the current percentage or state of RAM usage.

    Returns:
        dict: Memory information in a structured format.
    """
    return service_linux.get_memory_usage()
@tool()
def get_uptime():
    """
    Gets the length of time the 
    system has been running since the last boot.

    Returns:
        dict: Uptime information in a structured format.
    """
    return service_linux.get_uptime()
@tool()
def get_system_info():
    """
    Retrieves general Linux system information, 
    such as hostname, kernel, architecture, and OS version.

    Returns:
        dict: System information in a structured format.
    """
    return service_linux.get_system_info()