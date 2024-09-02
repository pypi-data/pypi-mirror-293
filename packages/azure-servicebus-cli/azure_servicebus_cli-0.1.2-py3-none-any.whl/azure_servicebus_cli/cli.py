import os
import types
import argparse
from azure.servicebus import ServiceBusClient, ServiceBusMessage

class AzureServiceBusCLI:
    def __init__(self):
        self.client = None

    def init(self):
        conn_str = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
        if not conn_str:
            raise EnvironmentError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set")

        self.client = ServiceBusClient.from_connection_string(conn_str)

    def send_message(self, queue_name, message, subject=None, reply_to=None):
        if os.path.isfile(message):
            with open(message, 'r') as file:
                message = file.read()
        else:
            message = message  # Treat as a plain string

        with self.client.get_queue_sender(queue_name) as sender:
            bus_message = ServiceBusMessage(
                body=message,
                subject=subject,
                reply_to=reply_to
            )
            sender.send_messages(bus_message)
        print("Message sent successfully")

    def read_message(self, queue_name, max_messages=1):
        with self.client.get_queue_receiver(queue_name) as receiver:
            messages = receiver.receive_messages(max_message_count=max_messages, max_wait_time=10)
            for msg in messages:
                if isinstance(msg.body, bytes):
                    print(f"Received: {msg.body.decode()}")
                else:
                    message_body = b''.join(msg.body) if isinstance(msg.body, (list, types.GeneratorType)) else msg.body
                    print(f"Received: {message_body.decode()}")
                receiver.complete_message(msg)

def main():
    try:
        bus = AzureServiceBusCLI()
        bus.init()

        parser = argparse.ArgumentParser(description="CLI tool for Azure Service Bus Queue")
        subparsers = parser.add_subparsers(dest="command")

        send_parser = subparsers.add_parser("send", help="Send message to queue")
        send_parser.add_argument("--queue", required=True, help="Queue name")
        send_parser.add_argument("--message", required=True, help="Message to send")
        send_parser.add_argument("--subject", help="Subject of message")
        send_parser.add_argument("--replyto", help="ReplyTo of message")

        receive_parser = subparsers.add_parser("receive", help="Receive message from queue")
        receive_parser.add_argument("--queue", required=True, help="Queue name")
        receive_parser.add_argument("--max-number-of-messages", type=int, default=1, help="Maximum number of messages to receive")
        receive_parser.add_argument("--output", choices=["tsv", "json"], default="tsv", help="Output format")

        args = parser.parse_args()

        if args.command == "send":
            bus.send_message(queue_name=args.queue, message=args.message, subject=args.subject, reply_to=args.replyto)
        elif args.command == "receive":
            bus.read_message(queue_name=args.queue, max_messages=args.max_number_of_messages)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
