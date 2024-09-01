import time
import os
import sys
from pathlib import Path
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Only necessary for development
from robustmq.client import RobustClient

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a RobustClient instance
my_robust_client = RobustClient(client_id="testclient", cache_path=Path("/tmp/mymqttcache"))
# Configure additional options like username and password
my_robust_client.mqtt_client.username_pw_set(username="michael", password="passwd") # Optionally Configure MQTT Client itself
# Establish a connection to the mqtt broker
my_robust_client.connect_async(mqtt_host="localhost")

# Send some messages
for i in range(20):
    my_robust_client.publish("dt/blah", f"Test Message {i:d}")
    time.sleep(1)

# Stop the client process
my_robust_client.stop()
