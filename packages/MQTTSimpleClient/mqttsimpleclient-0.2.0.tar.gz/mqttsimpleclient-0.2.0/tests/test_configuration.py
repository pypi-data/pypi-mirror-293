import unittest
import os
from MQTTSimpleClient.configuration import Configuration


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        # Creare una configurazione di test
        conf_content = '''<config>
            <log>
                <folder>
                    <path type="string">./logs</path>
                    <name type="string">app.log</name>
                </folder>
                <formatter type="string">%(asctime)s - %(name)s - %(levelname)s - %(message)s</formatter>
                <RotatingFileHandler>
                    <file_size type="int">10485760</file_size>
                    <backup_count type="int">5</backup_count>
                </RotatingFileHandler>
            </log>
            <test_values>
                <int_value type="int">123</int_value>
                <float_value type="float">123.456</float_value>
                <string_value type="string">test_string</string_value>
                <bool_value type="bool">True</bool_value>
            </test_values>
        </config>'''
        os.makedirs('./test_cfg', exist_ok=True)
        conf_path = './test_cfg/test_conf.xml'
        with open(conf_path, 'w') as f:
            f.write(conf_content)

        self.config = Configuration(custom_conf_path=conf_path)

    def tearDown(self):
        # Pulire i file di configurazione creati durante i test
        if os.path.exists('./test_cfg/test_conf.xml'):
            os.remove('./test_cfg/test_conf.xml')
        if os.path.exists('./test_cfg'):
            os.rmdir('./test_cfg')

    def test_read_configuration(self):
        parameters = self.config.parameters
        self.assertEqual(parameters['log']['folder']['path'], './logs')
        self.assertEqual(parameters['log']['folder']['name'], 'app.log')
        self.assertEqual(parameters['log']['formatter'], '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(parameters['log']['RotatingFileHandler']['file_size'], 10485760)
        self.assertEqual(parameters['log']['RotatingFileHandler']['backup_count'], 5)

    def test_data_formats(self):
        parameters = self.config.parameters
        self.assertEqual(parameters['test_values']['int_value'], 123)
        self.assertEqual(parameters['test_values']['float_value'], 123.456)
        self.assertEqual(parameters['test_values']['string_value'], 'test_string')
        self.assertTrue(parameters['test_values']['bool_value'])


if __name__ == '__main__':
    unittest.main()
