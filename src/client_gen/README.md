# ratbag-emu-client
No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.0.1
- Package version: 1.0.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import ratbag_emu_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ratbag_emu_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi(ratbag_emu_client.ApiClient(configuration))
device_id = 56 # int | ID of the device to return
event_data = ratbag_emu_client.EventData() # EventData | Event data

try:
    # Send an event to a simulated device
    api_instance.device_event(device_id, event_data)
except ApiException as e:
    print("Exception when calling DeviceApi->device_event: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost:8080*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DeviceApi* | [**device_event**](docs/DeviceApi.md#device_event) | **POST** /devices/{device_id}/event | Send an event to a simulated device
*DeviceApi* | [**get_device**](docs/DeviceApi.md#get_device) | **GET** /devices/{device_id} | Returns a simulated device
*DeviceApi* | [**list_devices**](docs/DeviceApi.md#list_devices) | **GET** /devices | List of simulated devices


## Documentation For Models

 - [Device](docs/Device.md)
 - [EventData](docs/EventData.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Author



