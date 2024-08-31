import unittest
from unittest.mock import MagicMock, patch
from MQTTSimpleClient.MqttPubSub import MqttClient, MqttSubscriber
from time import sleep


class TestMqttClient(unittest.TestCase):
    def setUp(self):
        self.broker_host = '10.7.68.9'
        self.broker_port = 1883
        self.client_id = 'test_client'
        self.mqtt_client = MqttClient(self.broker_host, self.broker_port, self.client_id)

    @patch('MQTTSimpleClient.MqttPubSub.mqtt.Client')
    def test_connect(self, mock_mqtt):
        self.mqtt_client.connect()
        # self.mqtt_client.run()
        sleep(2)
        mock_mqtt().connect.assert_called_with(self.broker_host, self.broker_port, 60)

    # @patch('MQTTSimpleClient.MqttPubSub.mqtt.Client')
    # def test_publish(self, mock_mqtt):
    #     self.mqtt_client.connect()
    #     self.mqtt_client.publish('test/topic', 'test message')
    #     sleep(2)
    #     mock_mqtt().publish.assert_called_with('test/topic', 'test message', 0, False)
    #
    # @patch('MQTTSimpleClient.MqttPubSub.mqtt.Client')
    # def test_subscribe(self, mock_mqtt):
    #     def callback_function(message):
    #         print(f"Message received: {message.payload.decode()}")
    #
    #     self.mqtt_client.connect()
    #     subscriber = MqttSubscriber(self.mqtt_client, 'test/topic', funzione1=callback_function)
    #     self.mqtt_client.client.on_connect(mock_mqtt(), None, None, 0)
    #     sleep(2)
    #     mock_mqtt().subscribe.assert_called_with('test/topic', 0)
    #
    # def test_singleton(self):
    #     client1 = MqttClient(self.broker_host, self.broker_port, self.client_id)
    #     client2 = MqttClient(self.broker_host, self.broker_port, self.client_id)
    #     sleep(2)
    #     self.assertIs(client1, client2)


if __name__ == '__main__':
    unittest.main()
