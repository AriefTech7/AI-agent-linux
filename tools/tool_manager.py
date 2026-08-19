from tools.filesystem.tool import *
from tools.web_search.tool import *
from tools.linux_system.tool import *

tools = [
    filesystem_read_file, filesystem_delete_file, filesystem_move_file, filesystem_copy_file, filesystem_rename_file,
    filesystem_create_file, filesystem_find_file, filesystem_create_folder, filesystem_read_folder, filesystem_get_folder_size,
    web_search_basic, web_search_advanced,
    get_disk_usage, get_cpu_info,get_hostname,get_os_info,get_kernel_info,get_memory_usage,get_uptime,get_system_info
]