import subprocess
from typing import Dict, Any


class LinuxSystem():
    def __init__(self):
        pass

    def get_cpu_info(self) -> Dict[str, Any]:
        result = subprocess.run(["lscpu"],
                                shell=False,
                                capture_output=True,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_hostname(self) -> Dict[str, Any]:
        result = subprocess.run(["hostname"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_kernel_info(self) -> Dict[str, Any]:
        result = subprocess.run(["uname", "-a"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_os_info(self) -> Dict[str, Any]:
        result = subprocess.run(["cat", "/etc/os-release"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_disk_usage(self) -> Dict[str, Any]:
        result = subprocess.run(["df", "-h"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_memory_usage(self) -> Dict[str, Any]:
        result = subprocess.run(["free", "-h"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }

    def get_uptime(self) -> Dict[str, Any]:
        result = subprocess.run(["uptime"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }
        
    def get_system_info(self) -> Dict[str, Any]:
        result = subprocess.run(["hostnamectl"],
                                capture_output=True,
                                shell=False,
                                check=True,
                                text=True,
                                timeout=0.4)
        return {
            "output": result.stdout,
            "output_error": result.stderr
        }
        
    