import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

class GetSystemInfo:

    def __init__(self):

      self.temp_threshold = 85
      self.mem_proc_treshold = 85

    def cpu_temp(self) -> float:
        """
        Reads the CPU temperature from /sys/class/thermal/thermal_zone0/temp
        Returns the temperature or raises a FileNotFoundError
        """
        logging.info("Get temperature from RPI")
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
               return round(float(file.read()) / 1000, 1)
        except FileNotFoundError:
            logging.error("The temp file was not found")
            return ("Data not available")

    def mem_info(self) -> dict:
        """
        Retrieves memory information from /proc/meminfo
        Returns a dictionary with total, available, used memory in MB and percent used.
        """
        logging.info("Get memory from RPI")
        meminfo = {}
        try:
           with open('/proc/meminfo', 'r') as f:
                for line in f:
                   parts = line.split()
                   key = parts[0].strip(':') # remove final ':'
                   value = int(parts[1]) # by default in kb
                   meminfo[key] = value

           total_mem = meminfo.get("MemTotal", 0) / 1024 # convert to MB
           available_mem = meminfo.get("MemAvailable", 0) / 1024
           used_mem = total_mem - available_mem
           percent_used = (used_mem / total_mem) * 100 if total_mem >0 else 0

           return {
             "total_mem": total_mem,
             "available_mem": available_mem,
             "used_mem": used_mem,
             "percent_used": percent_used,
           }
        except Exception as e:
           logging.error("Unexpected error while processing memory")
           return {"Error": f"Unexpected error: {e}"}

    def mem_info_string(self) -> str:
        aux = self.mem_info()
        return (f"Memory info:\nTotal Memory: {aux['total_mem']:.2f} MB\n"
                f"Available Memory: {aux['available_mem']:.2f} MB\n"
                f"Used Memory: {aux['used_mem']:.2f} MB -- Percent used: {aux['percent_used']:.2f}%" )
    def check_temp(self) -> bool:
         """
         Check if the CPU temperature exceeds the threshold.
         Returns True if it does, Fals otherwise.
         """
         current_temp = self.cpu_temp()
         return current_temp > self.temp_threshold

    def check_memory(self) -> bool:
         """
         Check if the memory percent is above the threshold
         Return True if it is, Fals otherwise.
         """
         meminfo = self.mem_info()
         return meminfo.get("percent_used",0) > self.mem_proc_treshold
    
    def uptime(self) -> list:
        """
        Extract the system uptime from /proc/uptime and converts it into days, hours, minutes, seconds.
        Return a list of integers.
        """
        with open('/proc/uptime', 'r') as file:
            uptime_seconds = int(float(file.read().split()[0]))
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        return [days, hours, minutes, seconds]

    def uptime_string(self) -> str:
         """
         Return the system uptime in a human-readable format.
         """
         uptime_list = self.uptime()
         days, hours, minutes, seconds = uptime_list
         return (f"System Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")


if __name__ == "__main__":
    ### JUST FOR INTERN TESTS
    system_info = GetSystemInfo()
    memory_data = system_info.mem_info_string()
    print(memory_data)
#    print(
#            f"Memory info:\n"
#            f" Total Memory: {memory_data['total_mem']:.2f} MB\n"
#            f" Available Memory: {memory_data['available_mem']:.2f} MB\n"
#            f" Used Memory: {memory_data['used_mem']:.2f} MB -- "
#            f"Percent used: {memory_data['percent_used']:.2f}%"
#        )
    print(f"\nTemp: {system_info.cpu_temp()}C")
    print(f"\nCheck temp: {system_info.check_temp()}")

    print(f"\nCheck mem: {system_info.check_memory()}")
    print(system_info.uptime_string())

