# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 14:51:40 2023

@author: Filomena Riccardo
"""

import paho.mqtt.client as mqtt
from time import sleep
from paho.mqtt.client import Client
from .my_logger import Logger
import threading
from typing import Optional

# Create a logger
logger = Logger(__name__.split(".")[-1]).get_logger()


class MqttClientGroup:
    def __init__(self, broker_host: str, broker_port: int, number_clients: int, shared_topic: str,
                 callback, client_id_root: str = "Client", qos: int = 0):
        """
        Initializes a group of MqttClient instances subscribed to the same shared topic
        and using the same callback function.

        :param str broker_host: The broker host address.
        :param int broker_port: The broker port number.
        :param int number_clients: Number of client IDs to create.
        :param str shared_topic: The shared topic to which all clients will subscribe.
        :param callback: The callback function to be used by all clients.
        :param str client_id_root: Client string root used to create list of client_ids.
        :param int qos: The quality of service level to use.
        """
        self.clients = []
        self.shared_topic = shared_topic
        self.qos = qos

        for client_idx in range(number_clients):
            client_id = "_".join([client_id_root, str(client_idx).zfill(2)])
            client = MqttClient(broker_host, broker_port, client_id)
            client.connect(asyncronous=True)
            client.add_subscriber(shared_topic, self.qos, callback=callback)
            self.clients.append(client)

    def run_all(self):
        """Starts all clients' loops asynchronously."""
        for client in self.clients:
            client.run()

    def disconnect_all(self):
        """Disconnects all clients."""
        for client in self.clients:
            client.disconnect()


class TopicHandlerManager:
    def __init__(self):
        self._topic_handlers = {}

    def register_topic_handler(self, topic: str, qos: int, callbacks) -> None:
        """Registers a handler for a specific topic, preventing duplication."""
        if topic in self._topic_handlers:
            raise ValueError(f"The topic '{topic}' is already registered and cannot be duplicated.")

        self._topic_handlers[topic] = {
            "qos": qos,
            "callbacks": callbacks,
            "clean_topic": self._get_clean_topic(topic)
        }

    def get_handler(self, topic: str) -> dict:
        """Retrieves the handler associated with the topic."""
        return self._topic_handlers.get(topic)

    def _get_clean_topic(self, topic: str) -> str:
        """register the "clean" topic if it is a shared topic"""
        if topic.startswith("$share/"):
            topic_parts = topic.split('/', 2)
            if len(topic_parts) > 2:
                return topic_parts[2]
        return topic

    @property
    def topic_handlers(self) -> dict:
        return self._topic_handlers


class MqttClient:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, broker_host: str = 'localhost', broker_port: int = 1883, client_id: str = 'default_client',
                username: Optional[str] = None, password: Optional[str] = None, mqtt_client=None):
        with cls._lock:
            if client_id not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[client_id] = instance
            return cls._instances[client_id]

    def __init__(self, broker_host: str = 'localhost', broker_port: int = 1883, client_id: str = 'default_client',
                 username: Optional[str] = None, password: Optional[str] = None, mqtt_client=None):
        self.__topic_handlers = {}

        if not hasattr(self, 'initialized'):
            self.__broker_host = broker_host
            self.__broker_port = broker_port
            self.__client_id = client_id
            self.__username = username
            self.__password = password

            self.__client = mqtt_client or mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                                                       client_id=client_id)
            # self.__logger = my_logger or Logger(__name__.split(".")[-1]).get_logger()
            self.__connected: bool = False
            self.__topic = []
            self.__qos = 0

            # Inizializza l'oggetto TopicHandlerManager
            self.__topic_handler_manager = TopicHandlerManager()

            # Connect MQTT event handlers
            self.__setup_callbacks()

            self.initialized = True

            logger.info(f"Client <{self.__client_id}> - Module initialized")

    def __setup_callbacks(self):
        """Sets up MQTT event handlers."""
        self.__client.on_connect = self.__on_connect
        self.__client.on_publish = self.__on_publish
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_subscribe = self.__on_subscribe

    def __on_connect(self, client, userdata, flags, rc, properties) -> None:
        if rc == 0:
            self.__connected = True
            self.__subscribe()
            logger.info(f"Client <{self.__client_id}> - Connected to the MQTT broker {self.__broker_host}")
        else:
            logger.error(f"Client <{self.__client_id}> - MQTT broker connection failed due to: " + str(rc))

    def __on_disconnect(self, client, userdata, flags, rc, properties):
        logger.info(f"Client <{self.__client_id}> - Disconnected from MQTT broker {self.__broker_host} cod. {rc}")

    def __on_publish(self, client, userdata, mid, reason_code, properties) -> None:
        logger.info(
            f"Client <{self.__client_id}> - Message published Mid: <{str(mid)}> topic <{self.__topic}> "
            f"qos <{self.__qos}>")

    def __on_subscribe(self, client, userdata, mid, granted_qos, properties):
        logger.info(f"Client <{self.__client_id}> - Subscription established on topic '{self.__topic[0]}':"
                    f" QoS <{str(self.__qos)}>, callback <{list(self.__topic_handler_manager.get_handler(self.__topic[0])['callbacks'].keys())}>")
        self.__topic.pop(0)

    def __on_message(self, client, userdata, message):
        logger.info(f"Client <{self.__client_id}> - message received on topic {message.topic}:"
                    f" {message.payload.decode()[:40]} ... ")
        self.__message = message
        for topic, handler in self.__topic_handler_manager.topic_handlers.items():
            if message.topic == handler.get("clean_topic"):
                callbacks = handler.get("callbacks")

                for k, func in callbacks.items():
                    sleep(0.1)
                    try:
                        func(self.__message)
                        sleep(0.1)
                    except Exception as e:
                        logger.error(f"Client <{self.__client_id}> - Error in __on_message() callback: {str(e)}")

    def connect(self, asyncronous: bool = False) -> None:
        logger.info(f"Client <{self.__client_id}> - Test Connection MQTT broker <{self.__broker_host}>")
        if self.__username and self.__password:
            self.__client.username_pw_set(self.__username, self.__password)
        try:
            if asyncronous:
                self.__client.connect_async(self.__broker_host, self.__broker_port, 60)
            else:
                self.__client.connect(self.__broker_host, self.__broker_port, 60)
        except Exception as e:
            logger.error(
                f"Client <{self.__client_id}> - Error connecting to the MQTT broker <{self.__broker_host}>: {e}")
        sleep(0.1)

    def publish(self, topic: str, message: str, qos: int = 0, retain: bool = False) -> None:
        self.__topic = topic
        self.__qos = qos
        try:
            self.__client.publish(topic, message, qos, retain)
        except Exception as e:
            logger.error(f"Client <{self.__client_id}> - not connected to the MQTT broker <{self.__broker_host}> -> "
                         f"Unable to publish message: {e}")
        sleep(0.1)

    def add_subscriber(self, topic: str, qos: int, **callback) -> None:

        logger.info(f"Client <{self.__client_id}> - Test subscription: topic <{topic}>")

        callback_dict = {key: value for key, value in callback.items() if callable(value)}

        self.__topic_handler_manager.register_topic_handler(topic, qos, callback_dict)

        sleep(0.1)

    def run(self) -> None:
        self.__client.loop_start()
        logger.info(f"Client <{self.__client_id}> - Client Loop Start")

    def run_forever(self) -> None:
        logger.info(f"Client <{self.__client_id}> - Client Loop_Forever Start")
        self.__client.loop_forever()

    def disconnect(self) -> None:
        try:
            self.__client.disconnect()
            self.__client.loop_stop()
            self.__connected = False
            logger.info(f"Client <{self.__client_id}> - Disconnected from MQTT broker")
        except Exception as e:
            logger.error(f"Client <{self.__client_id}> - Error disconnecting from the MQTT broker: {e}")

    def __subscribe(self) -> None:
        for topic, handler in self.__topic_handler_manager.topic_handlers.items():
            self.__topic.append(topic)
            try:
                self.__client.subscribe(topic, handler.get("qos"))
            except Exception as e:
                logger.error(f"Client <{self.__client_id}> - Error subscribing to topic <{topic}>: {e}")

    def unsubscribe(self) -> None:
        for topic, handler in self.__topic_handler_manager.topic_handlers.items():
            self.__client.unsubscribe(topic)

    @classmethod
    def __subscribe_all(cls) -> None:
        for client_id, instance in cls._instances.items():
            for topic, handler in instance.__topic_handler_manager.topic_handlers.items():
                instance.__topic = topic
                instance.__client.subscribe(topic, handler.get("qos"))

    @classmethod
    def unsubscribe_all(cls) -> None:
        for client_id, instance in cls._instances.items():
            for topic, handler in instance.__topic_handler_manager.topic_handlers.items():
                instance.__client.unsubscribe(topic)

    @classmethod
    def run_all(cls) -> None:
        pass

    @classmethod
    def run_forever_all(cls) -> None:
        pass

    @property
    def client(self) -> Client:
        return self.__client

    @property
    def connected(self) -> bool:
        return self.__connected

    @property
    def broker_host(self) -> str:
        return self.__broker_host

    @property
    def client_id(self) -> str:
        return self.__client_id
