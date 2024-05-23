import servicemanager
import win32event
import win32service
import win32serviceutil
import logging
import json
import portalocker
import time

class MailProcessorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MailProcessorService"
    _svc_display_name_ = "Mail Processor Service"
    _svc_description_ = "Processes mail items from a JSON file."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._get_logger()
        self._keep_running = True
        self.json_file_path = 'C:\\mail_items.json'

    def _get_logger(self):
        logger = logging.getLogger('[MailProcessorService]')
        handler = logging.FileHandler('C:\\MailProcessorService.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)-7.7s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def SvcStop(self):
        self.logger.info('Service is stopping...')
        self._keep_running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.logger.info('Service is starting...')
        self.main()

    def main(self):
        while self._keep_running:
            self.process_mail_items()
            time.sleep(60)  # Check every minute

    def process_mail_items(self):
        with portalocker.Lock(self.json_file_path, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                self.logger.info('No mail items to process.')
                return

            items_to_process = [item for item in data if not item.get('processed', False)]

            if not items_to_process:
                self.logger.info('No unprocessed mail items to process.')
                return

            for item in items_to_process:
                self.logger.info(f'Processing mail item: {item}')
                self.process_item(item)

            unprocessed_items = [item for item in data if not item.get('processed', False)]
            file.seek(0)
            json.dump(unprocessed_items, file, indent=4)
            file.truncate()
        self.logger.info('Processed mail items removed from file.')

    def process_item(self, item):
        # Implement your item processing logic here
        item['processed'] = True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MailProcessorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MailProcessorService)
