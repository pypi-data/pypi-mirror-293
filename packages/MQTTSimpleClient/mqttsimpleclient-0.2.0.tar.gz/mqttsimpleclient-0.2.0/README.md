# MQTTSimpleClient

A custom MQTT library for interaction with an MQTT broker, providing enhanced functionality for managing MQTT clients and subscribers in Python.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [MqttClient](#mqttclient)
  - [MqttClientGroup](#mqttclientgroup)
  - [TopicHandlerManager](#topichandlermanager)
- [Contributing](#contributing)


## Introduction
This library provides a simple interface to interact with an MQTT broker using Python. It includes features like managing multiple MQTT clients, custom logging, and configuration management with an XML-based configuration file.

## Features
- **Singleton pattern** for managing MQTT clients.
- **Custom logger** with support for rotating file handlers.
- **XML-based configuration** to easily manage settings.
- **Support for multiple clients** with `MqttClientGroup`.
- **Flexible topic management** with `TopicHandlerManager`.
- **Asynchronous connection handling** and subscription management.


## Installation
To install the library, use the following command:

```sh
pip install MQTTSimpleClient
```

## Usage


### Configuration:

```ruby
<config>
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
</config>

```


### Logger
Here's how to use the custom logger:

```ruby
from MQTTSimpleClient.my_logger import Logger

logger = Logger('my_script').get_logger()
logger.info('This is an info message')
```


### MQTTClient
The MqttClient class manages the connection to an MQTT broker and handles publishing and subscribing to topics.
```ruby
from MQTTSimpleClient.mqtt_client import MqttClient

mqtt_client = MqttClient("broker_host", 1883, "client_id")
mqtt_client.connect()
mqtt_client.publish("topic", "message")
mqtt_client.add_subscriber("topic", 0, callback=my_callback_function)
mqtt_client.disconnect()
```

### MqttClientGroup
The MqttClientGroup class allows you to manage a group of MQTT clients subscribed to the same shared topic.
```ruby
from MQTTSimpleClient.mqtt_client import MqttClientGroup

def my_callback_function(message):
    print(f"Message received: {message.payload.decode()}")

client_group = MqttClientGroup("broker_host", 1883, 5, "shared/topic", my_callback_function)
client_group.run_all()
```

### TopicHandlerManager
The TopicHandlerManager class provides a way to register and manage multiple topic handlers.
```ruby
manager = TopicHandlerManager()
manager.register_topic_handler("topic1", 0, callbacks={"callback1": my_callback_function})
handler = manager.get_handler("topic1")
print(handler)
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss what you would like to change.


