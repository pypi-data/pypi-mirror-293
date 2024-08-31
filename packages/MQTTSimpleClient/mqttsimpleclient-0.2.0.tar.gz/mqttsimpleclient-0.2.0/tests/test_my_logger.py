import unittest
import os
import logging
from MQTTSimpleClient.my_logger import Logger
from MQTTSimpleClient.configuration import Configuration


class TestLogger(unittest.TestCase):
    def setUp(self):
        # Creare una configurazione di test per evitare di sporcare la configurazione reale
        conf_content = '''<config>
            <log>
                <folder>
                    <path type="string">./test_logs</path>
                    <name type="string">test.log</name>
                </folder>
                <formatter type="string">%(asctime)s - %(name)s - %(levelname)s - %(message)s</formatter>
                <RotatingFileHandler>
                    <file_size type="int">1048576</file_size>
                    <backup_count type="int">1</backup_count>
                </RotatingFileHandler>
            </log>
        </config>'''

        os.makedirs('./test_logs', exist_ok=True)
        conf_path = './test_logs/test_conf.xml'
        with open(conf_path, 'w') as f:
            f.write(conf_content)

        # Inizializzare la configurazione con il file di test
        self.config = Configuration(custom_conf_path=conf_path)
        self.logger = Logger('test_script')

    def tearDown(self):
        # Pulire i file di log creati durante i test
        if os.path.exists('./test_logs/test.log'):
            os.remove('./test_logs/test.log')
        if os.path.exists('./test_logs/test_conf.xml'):
            os.remove('./test_logs/test_conf.xml')
        if os.path.exists('./test_logs'):
            os.rmdir('./test_logs')

    def test_logger_levels(self):
        logger = self.logger.get_logger()
        logger.debug('This is a debug message')
        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a critical message')

        logger.handlers[0].flush()  # Ensure all log messages are flushed to the file

        with open('./test_logs/test.log', 'r') as f:
            log_content = f.read()
            self.assertIn('This is a debug message', log_content)
            self.assertIn('This is an info message', log_content)
            self.assertIn('This is a warning message', log_content)
            self.assertIn('This is an error message', log_content)
            self.assertIn('This is a critical message', log_content)

    def test_logger_script_name(self):
        logger = self.logger.get_logger()
        logger.info('Test script name')

        logger.handlers[0].flush()  # Ensure all log messages are flushed to the file

        with open('./test_logs/test.log', 'r') as f:
            log_content = f.read()
            self.assertIn('test_script', log_content)


if __name__ == '__main__':
    unittest.main()
