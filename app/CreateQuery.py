import os
from azure.eventhub import EventHubConsumerClient
import json
import threading


CONNECTION_STR1 = ""
CONNECTION_STR2 = ""
CONNECTION_STR3 = ""

EVENTHUB_NAME1 = "consumer01"
EVENTHUB_NAME2 = "secondconsumer"
EVENTHUB_NAME3 = "thirdconsumer"

OUTPUT_FILE_PATH = "C:/Users/user/OneDrive/Bureau/QoS-optimization-in-IoT-systems-main/telemetry.txt"  # Replace with your desired file path


def save_telemetry_to_file(file_path, telemetry_data):
    with open(file_path, 'a') as file:
        for param_name, param_value in telemetry_data.items():
            file.write(f"{param_value}\n")

def on_event_1(partition_context, event):
    event_data = event.body_as_str()
    try:
        parsed_data = json.loads(event_data)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return

    telemetry_data = parsed_data.get('telemetry', {})
    save_telemetry_to_file(OUTPUT_FILE_PATH, telemetry_data)



def receive_events(client, event_handler):
    with client:
        client.receive(
            on_event=event_handler,
            starting_position="-1",
        )

# Create EventHubConsumerClient instances
client_1 = EventHubConsumerClient.from_connection_string(
    conn_str=CONNECTION_STR1,
    consumer_group="$Default",
    eventhub_name=EVENTHUB_NAME1,
)

# client_2 = EventHubConsumerClient.from_connection_string(
#     conn_str=CONNECTION_STR2,
#     consumer_group="$Default",
#     eventhub_name=EVENTHUB_NAME2,
# )

# client_3 = EventHubConsumerClient.from_connection_string(
#     conn_str=CONNECTION_STR3,
#     consumer_group="$Default",
#     eventhub_name=EVENTHUB_NAME3,
# )

# Create threads to run clients simultaneously
thread_1 = threading.Thread(target=receive_events, args=(client_1, on_event_1))
# thread_2 = threading.Thread(target=receive_events, args=(client_2, on_event_2))
# thread_3 = threading.Thread(target=receive_events, args=(client_3, on_event_3))

# Start threads
thread_1.start()
# thread_2.start()
# thread_3.start()