# Azure Service Bus CLI

`azure-servicebus-cli` is a simple command-line interface (CLI) tool for interacting with Azure Service Bus Queues. This tool allows you to send and receive messages from an Azure Service Bus Queue using a few straightforward commands.

## Installation

To install the `azure-servicebus-cli` package, use `pip`:

```bash
pip install azure-servicebus-cli
```

## Prerequisites

Before using the CLI tool, make sure you have:

1. An Azure Service Bus namespace and queue created in your Azure account.
2. The connection string for your Azure Service Bus. You can obtain this from the Azure portal.

## Environment Variable

Set the `AZURE_SERVICEBUS_CONNECTION_STRING` environment variable with your Service Bus connection string:

```bash
export AZURE_SERVICEBUS_CONNECTION_STRING="your-connection-string"
```

## Usage

### Sending a Message

You can send a message to a specified queue using the `send` command. You can directly pass a message or provide a path to a file containing the message content.

#### Example 1: Send a Message Directly

```bash
azsb send --queue <your-queue-name> --message "Your message here"
```

#### Example 2: Send a Message from a File

```bash
azsb send --queue <your-queue-name> --message /path/to/your/message.json
```

### Receiving Messages

You can receive messages from a specified queue using the `receive` command. You can also specify the maximum number of messages to receive.

#### Example 1: Receive a Single Message

```bash
azsb receive --queue <your-queue-name>
```

#### Example 2: Receive Multiple Messages

```bash
azsb receive --queue <your-queue-name> --max-number-of-messages 10
```

## License

This project is licensed under the MIT License.
