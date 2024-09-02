# GenAI Chat Library

Caber's GenAI Chat Library provides a convenient way to pass user sessions for GenAI applications to Caber for inspection.  
The library handles each request and associated response as a single event, similar to an API requat and response. 

After initialization, you start each request by calling the `new_request` method with the appropriate parameters.  When 
the response is received, you can then pass the response body and parameters to the `handle_response` method to complete the request.

Once the request and response have been input, call the post_event method to send the event to Caber for inspection.

## Building the library

To build the GenAI Chat Library, you need to have the following tools installed:
setuptools, twine, wheel

These may already be installed in a local virtual environment.  If so, activate the environment before building the library.

```bash
cd GenAiChatLib
source ./genv/bin/activate
```

To build the library, first edit the version number in the setup.py file.  Then run the following command:

```bash
python setup.py sdist bdist_wheel
```

This will create a 'dist' directory containing the library packages.  Assuming the version number you set is '0.1.25'
the package files will be named `csi_genai_lib-0.1.25.tar.gz` and `csi_genai_lib-0.1.25-py3-none-any.whl`.  
You can then install the package using pip:

```bash
pip install ./GenAiChatLib/dist/csi_genai_lib-0.1.25-py3-none-any.whl --force-reinstall          
```

The `--force-reinstall` flag is used to force the reinstallation of the package, which is useful when testing the library.
Finally, you can upload the package to the PyPi repository using twine.  Make sure you have the correct credentials 
for the repository.

```bash
twine upload dist/*
```

## Installation

You can install the GenAI Chat Library using pip:

```bash
pip install csi-genai-chat
```

## Usage

To use the GenAI Chat Library in your code, you need to import the `MainHandler` class from the `genai_chat_lib.main` module:

```python
import csi_genai_lib as csi
```

## Creating a New Request

To create a new request, you can instantiate the MainHandler class and call the new_request method with the appropriate parameters:

```python
import csi_genai_lib as csi
csi.new_request(
    context="Hello, how can I assist you today?",
    base64=False,
    hostname="chatbot.com",
    user_id="user123",
    user_type="basic",
    user_hostname_or_ip="192.168.0.1",
    user_session="session123",
    api_name="chat-api",
    query="q=hello"
)
```

The following variable parameters can be passed to the new_request method:

* context (str, bytes, bytearray  default: ''): The context or content of the request. It represents the data, message, or prompt being sent in the request.
* base64 (bool default: False): A boolean flag indicating whether the context data has been base64 encoded.
* hostname (str default: gethostname()): The hostname or IP address of the service on which the library is running.  This is used to identify the service or agent handling the user's request to Caber.
* user_id (str default: "noAuth"): The user ID associated with the request. It represents the identity of the user making the request.
* user_type (str default: "basic"): The type of user authentication used for the request.
* user_hostname_or_ip (str default: ""): The hostname or IP address the user making the request is coming from.  This is not the hostname of the service handling the request.
* user_session (str default: None): An identifier that connects multiple user request/response pairs together into a session.
* api_name (str default: 'chat-post'): If there are multiple functions or API endpoints being used on the service 'hostname', this parameter can be used to identify the specific function or endpoint being called.
* mime_type (str default: 'application/json; charset=utf-8'): The MIME type of the request and response data.
* query (str default: None): The query string parameters to be included with the user's requects if any.

## Updating the Response

After processing the request, you can update the response using the update_response method as below.  Once the 
response has been updated, the event will automatcally be sent to Caber for inspection.

```python
import csi_genai_lib as csi
csi.new_request(
    context="Hello, how can I assist you today?",
    base64=False,
    hostname="chatbot.com",
    user_id="user123",
    user_type="basic",
    user_hostname_or_ip="192.168.0.1",
    user_session="session123",
    api_name="chat-api",
    query="q=hello"
)
csi.update_response(
    response="I'm here to help! How can I assist you?",
    mime_type="application/json"
)
```

The following variable parameters can be passed to the update_response method:

* response (str, bytes, bytearray  default: ''): The context or content of the request. It represents the data, message, or prompt being sent in the request.
* base64 (bool default: False): A boolean flag indicating whether the context data has been base64 encoded.
* mime_type (str default: 'application/json; charset=utf-8'): The MIME type of the request and response data.

## Configuration

The GenAI Chat Library relies on certain configuration parameters, such as the SQS queue name and other settings. Make sure to properly configure these parameters based on your environment and requirements.

## Example

Here's a complete example of using the GenAI Chat Library:

```python
import csi_genai_lib as csi

csi.new_request(
    context="Hello, how can I assist you today?",
    user_id="user123",
    user_session="session123",
    api_name="chat-api"
)

# Process the request and generate a response
response = "I'm here to help! How can I assist you?"

csi.update_response(
    response=response,
    mime_type="application/json"
)

```

## Getting the User's IP address and UserAgent

### Flask
To obtain the IP address and user agent of a remote user logged into a Dash app, you can access the request headers from the Flask request object, which is available in Dash through flask.request. Here’s how you can modify your Dash app to capture this information:
Import Flask Request: Make sure you have access to the Flask request object by importing it.
from flask import request
Access IP Address and User Agent: You can access the IP address and user agent within your callback or any part of your Dash app where you handle user interactions. Here’s an example of how you might do this within a callback:

```python
from dash import Dash, html, Input, Output
import flask

app = Dash(__name__)

# Example layout
app.layout = html.Div([
    html.Button("Get Info", id="info-btn"),
    html.Div(id="user-info")
])

@app.callback(
    Output("user-info", "children"),
    Input("info-btn", "n_clicks")
)
def get_user_info(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    # Accessing the user's IP address and user agent
    user_ip = flask.request.remote_addr
    user_agent = flask.request.headers.get('User-Agent')

    return f"IP Address: {user_ip}, User Agent: {user_agent}"

if __name__ == '__main__':
    app.run_server(debug=True)
```

In this example:
When the user clicks the "Get Info" button, the callback get_user_info is triggered.
The flask.request.remote_addr provides the IP address of the client.
The flask.request.headers.get('User-Agent') retrieves the user agent string from the request headers.

Security Considerations: Be aware that IP addresses can be spoofed, especially if the user is behind a proxy or VPN. The user agent can also be easily modified on the client side. Use this information cautiously, especially if making security-related decisions.

Deployment Note: If your Dash app is deployed behind a proxy or in a complex network environment (like a cloud deployment), you might need to configure your proxy or web server to pass the correct headers that contain the real IP address and other necessary information. This often involves setting headers like X-Forwarded-For in your proxy configuration.
This setup should help you capture and utilize the IP address and user agent of users interacting with your Dash application.