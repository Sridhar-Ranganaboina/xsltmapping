import time
from multiprocessing import Process, freeze_support
# import logging

from windowsservice import BaseService, utils
from service_logic import ServiceLogic

# logging.basicConfig(filename='windowsservice.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# logger=logging.getLogger(__name__)
# def stub_server():
#     """
#     A function that simulates a server process hosted by the Windows service.

#     This function logs a message every 5 seconds for a total of 100 times.
#     """
#     for _ in range(100):
#         # logger.log("Hello from a process hosted by a Windows service...")
#         time.sleep(5)

serviceLogic=ServiceLogic()
class ExampleService(BaseService):
    """Example Windows service in Python."""

    _svc_name_ = "PythonTest"
    _svc_display_name_ = "PythonTest"
    _svc_description_ = "PythonTest Example Windows service in Python"

    def start(self):
        # logger.log("Service Started")
        
        self.server_process = Process(target=serviceLogic.stub_server)

    def main(self):
        self.server_process.start()
        self.server_process.join()

    def stop(self):
        if self.server_process:
            self.server_process.terminate()


if __name__ == "__main__":
    try:
        freeze_support()
        ExampleService.parse_command_line()
    except Exception as e:
        pass
        
    