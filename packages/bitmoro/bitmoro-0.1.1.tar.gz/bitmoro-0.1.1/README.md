# Bitmoro Messaging and OTP Library [![PyPI version](https://img.shields.io/pypi/v/bitmoro.svg)](https://pypi.org/project/bitmoro/) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/bitmoro)

This library provides a convenient interface for sending messages and handling OTP (One-Time Password) operations using the Bitmoro API from Python.

## Installation

```sh
pip install bitmoro

```

## Usage

The code below shows how to get started using the messaging and OTP features.

### Sending Messages

```python
from bitmoro import MessageSender

token = 'your_token_here'  # Replace with your API token
sender = MessageSender(token)

def send_message():
    try:
        success = sender.send_sms('Hello, World!', ['+1234567890'], 'YourSenderId')
        print('Message sent:', success)
    except Exception as error:
        print('Error sending message:', error)

send_message()

```
### Scheduling Messages

```python
from bitmoro import MessageScheduler
from datetime import datetime, timedelta

token = 'your_token_here'  # Replace with your API token
scheduler = MessageScheduler(token)

def schedule_message():
    future_time = datetime.now() + timedelta(minutes=10)
    try:
        scheduler.schedule_sms('Scheduled message!', ['+1234567890'], future_time, 'YourSenderId')
        print('Message scheduled successfully.')
    except Exception as error:
        print('Error scheduling message:', error)

schedule_message()

```

### Handling OTPs

```python
from bitmoro import OtpHandler

token = 'your_token_here'  # Replace with your API token
otp_handler = OtpHandler(token)

def send_otp():
    try:
        otp_handler.send_otp_message('9841452888', 'md_alert')
        print('OTP sent successfully.')
    except Exception as error:
        print('Error sending OTP:', error)

def verify_otp():
    otp = input("Enter the OTP received: ")
    try:
        is_valid = otp_handler.verify_otp('9841452888', otp)
        print('OTP valid:', is_valid)
    except Exception as error:
        print('Error verifying OTP:', error)

send_otp()
verify_otp()

```

## Features

- **Send Messages**: Easily send SMS messages to multiple recipients using a straightforward API.
- **OTP Generation and Verification**: Generate secure OTPs and verify them for authentication purposes.
- **Error Handling**: Includes custom error classes to handle API errors effectively.

### Streaming Responses

The library supports streaming responses for real-time applications. This can be particularly useful for use cases where immediate feedback is required.

### Request & Response Types

The library includes TypeScript definitions for all request parameters and response fields, ensuring type safety and better developer experience.

### Automated Function Calls

Automate repetitive tasks by integrating function calls within your message handling and OTP verification processes.

### Bulk Operations

For applications requiring bulk message sending or OTP generation, the library provides helper functions to streamline these operations.

## Error Handling

When the library is unable to connect to the API, or if the API returns a non-success status code, a `MessageSenderError` will be thrown. Here’s an example of how to handle such errors:

```python
def main():
    try:
        sender.send_sms('Hello, World!', ['+1234567890'])
    except MessageSenderError as err:
        print(err)  # Error message
    except Exception as err:
        raise err

main()

```



### Explanation

- **Language Identifier**: Use `python` after the opening triple backticks to specify Python syntax highlighting.
- **Token**: Replace `'your_token_here'` with your actual API token.
- **Phone Number and Sender ID**: Adjust the phone number `['+1234567890']` and the sender ID `'YourSenderId'` to match your requirements.
- **Function**: The `send_message` function demonstrates how to instantiate the `MessageSender` class and send a message, handling any exceptions that may occur.

By using the correct syntax highlighting, your README will be more readable and user-friendly for developers who are using your library.
