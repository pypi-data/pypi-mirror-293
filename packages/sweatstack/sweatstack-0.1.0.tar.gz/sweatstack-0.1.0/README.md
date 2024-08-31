# SweatStack Python Library

## Overview

SweatStack is a powerful Python library designed for athletes, coaches, and sports scientists to analyze and manage athletic performance data. It provides a seamless interface to interact with the SweatStack API, allowing users to retrieve, analyze, and visualize activity data, user information, and performance metrics.

## Installation

We recommend using `uv` to manage Python and install the library.
Read more about `uv` [here](https://docs.astral.sh/uv/getting-started/).

```bash
uv pip install sweatstack
```

You can also install it with `pip` (or `pipx`) directly.
```bash
pip install sweatstack
```

## Quickstart

Get started with analyzing your latest activity:

```python
import sweatstack as ss

ss.login()

latest_activity = ss.get_latest_activity()

print(latest_activity)  # `latest_activity` is a pandas DataFrame
```


## Authentication

To be able to access your data in Sweat Stack, you need to authenticate the library with your Sweat Stack account.
The easiest way to do this is to use your browser to login:

```python
import sweatstack as ss

ss.login()
```
This will automaticallyset the appropriate authentication tokens in your Python code.

Alternatively, you can set the `SWEAT_STACK_API_KEY` environment variable to your API key.
You can create an API key [here](https://app.sweatstack.com/account/api-keys).

```python
import os

import sweatstack as ss

os.environ["SWEAT_STACK_API_KEY"] = "your_api_key_here"

# Now you can use the library
```


## Listing activities

To list activities, you can use the `list_activities()` function:

```python
for activity in ss.list_activities():
    print(activity)
```
> **Info:** This method returns a summary of the activities, not the actual timeseries data.
> To get the actual data, you need to use the `get_activity_data()` or `get_latest_activity_data()`) methods documented below.

## Getting activity summaries

To get the summary of an activity, you can use the `get_activity()` function:

```python
activity = ss.get_activity(activity_id)
print(activity)
```

To quickly the latest activity, you can use the `get_latest_activity()` function:

```python
activity = ss.get_latest_activity()
print(activity)
```

## Getting activity data

To get the timeseries data of one activity, you can use the `get_activity_data()` method:

```python
data = ss.get_activity_data(activity_id)
print(data)
```

This method returns a pandas DataFrame.
If your are not familiar with pandas and/or DataFrames, start by reading this [introduction](https://pandas.pydata.org/docs/user_guide/10min.html).

Similar as for the summaries, you can use the `get_latest_activity_data()` method to get the timeseries data of the latest activity:

```python
data = ss.get_latest_activity_data()
print(data)
```

To get the timeseries data of multiple activities, you can use the `get_longitudinal_data()` method:

```python
longitudinal_data = ss.get_longitudinal_data(
    start=date.today() - timedelta(days=180),
    sport="running",
    metrics=["power", "heart_rate"],
)
print(longitudinal_data)
```

Because the result of `get_longitudinal_data()` can be very large, the data is retrieved in a compressed format (parquet) that requires the `pyarrow` library to be installed. If you intend to use this method, make sure to install the `sweatstack` libraryr with `uv pip install sweatstack[parquet]`.
Also note that depending on the amount of data that you requested, this might take a while.

## Accessing other user's data

By default, the library will give you access to your own data.

You can list all users you have access to with the `list_accessible_users()` method:

```python
for user in ss.list_accessible_users():
    print(user)
```

You can switch to another user by using the `switch_user()` method:

```python
ss.switch_user(user)
```

Calling any of the methods above will return the data for the user you switched to.

You can easily switch back to your original user by calling the `switch_to_root_user()` method:

```python
ss.switch_to_root_user()
```


## Metrics

The API supports the following metrics:
- `power`: Power in Watt
- `speed`: Speed in m/s
- `heart_rate`: Heart rate in BPM
- `smo2`: Muscle oxygen saturation in %
- `core_temperature`: Core body temperature in °C
- `altitude`: Altitude in meters
- `cadence`: Cadence in RPM
- `temperature`: Ambient temperature in °C
- `distance`: Distance in m
- `longitude`: Longitude in degrees
- `latitude`: Latitude in degrees


## Sports

The API supports the following sports:
- `running`: Running
- `cycling`: Cycling

More sports will be added in the future.