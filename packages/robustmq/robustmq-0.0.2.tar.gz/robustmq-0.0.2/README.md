# RobustMQ

**RobustMQ** is a reliable on-top mqtt-module designed to support dealing with unreliable connections. This project is aimed at providing a robust, easy-to-use messaging solution.

It is mainly designed for edge devices to  reliable transfer produced data even when there are power outages or longer connection troubles. The messages are cached on the file system to be reloaded again when the data transfer is possible.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **High Reliability:** Ensures message delivery even in the event of network failures or node crashes.
- **Message Caching:** Messages, which are not received by the broker are cached on the file system for later retries
- **Caching Methods:** Cache large messages directly to pickle or leightweight to sqlite database
- **Ease of Use:** Simple API for integrating with your application, allowing you to move easily from paho.mqtt bare implementation.

## Installation
To install **RobustMQ**, you can clone the repository and install the required dependencies:


```bash
git clone https://github.com/DaqOpen/robustmq.git
cd robustmq
pip install .
```

## Usage
Here is a simple example of how to use RobustMQ in your project:

```python
import time
from pathlib import Path
from robustmq.client import RobustClient

# Create a RobustClient instance
my_robust_client = RobustClient(client_id="testclient", cache_path=Path("/tmp/mymqttcache"))
# Establish a connection to the mqtt broker
my_robust_client.connect_async(mqtt_host="localhost")

# Send some messages
for i in range(20):
    my_robust_client.publish("dt/blah", f"Test Message {i:d}")
    time.sleep(1)

# Stop the client process
my_robust_client.stop()
```



## How it works

First, a separate process is spawned after the call of connect_async. This is done with the multiprocessing module. For further communication with this process, two queues are created.

The main goal is, to only put message by message into the queue of the mqtt-client, when the previous was sent successfully. This may reduce performance but allows to preserve messages when there are errors.

When publishing a message with the RobustClient, it follows this flow:

1. message is queued in the multiprocessing queue
2. the worker process checks the queue and consumes **one** message if available
3. this message is then published via the underlying paho.mqtt client
4. the process waits until the message has reached its destination (on_publish callback)
   1. if a timeout has been reached, the whole input queue (including the actual in publish stuck message) gets cached in the file system
   2. the caching is going on until the message has been successfully published
5. When the publish was successful, this meanwhile cached message is deleted
6. at the next loop, it will be checked, if cached data is available and starts publishing that



## Contributing

I welcome contributions to **RobustMQ**! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
