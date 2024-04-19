import time
class ServiceLogic:
    def __init__(self) -> None:
        pass
    def write_to_log(self, message):
        """
        Write a message to the log file.
        """
        with open(r'C:\Users\siddu\source\repos\Test Windows Service\ServiceLogic.log', 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def stub_server(self):
      
         
        """
        A function that simulates a server process hosted by the Windows service.

        This function logs a message every 5 seconds for a total of 100 times.
        """
        for _ in range(100):
            
            self.write_to_log("Hello from a process hosted by a Windows service...")
            time.sleep(2)
            
