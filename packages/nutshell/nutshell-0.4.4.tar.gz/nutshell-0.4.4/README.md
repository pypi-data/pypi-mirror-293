# Nutshell API

This is a work-in-progress attempt at a pythonic API for querying the Nutshell CRM API. The bulk of the methods only
read
data, except a few methods for editing activities.

## Installation

```bash 
pip install nutshell
```

## Usage

- Initialize the API instance with your credentials
- Create an instance of the method(s) you want to call
- Pass a single method instance, or a collection of methods to the `api_calls` property of the API class
- Execute the method calls on API with the `call_api()` method
    - If a single method is passed to the API instance, the result will be a single response object
    - If a collection of methods is passed, the result will be a list of response objects
    - *aiohttp is used to make the API calls asynchronous*

```python
import os

from rich import print

import nutshell
from nutshell import methods

find_activities = methods.FindActivityTypes()
ns = nutshell.NutshellAPI(os.getenv("NUTSHELL_USERNAME"), password=os.getenv("NUTSHELL_KEY"))
ns.api_calls = find_activities
activity_types = ns.call_api()
print(activity_types)
```

Each API call will have a corresponding response object with a `result` value that contains the response from the API.

```python
FindActivityTypesResult(
    result=[
        ActivityType(
            stub=True,
            id=1,
            rev='1',
            entity_type='Activity_Types',
            name='Phone Call / Meeting'
        ),
        ActivityType(
            stub=True,
            id=2,
            rev='7',
            entity_type='Activity_Types',
            name='Quotes Sent'
        ),
        ActivityType(
            stub=True,
            id=3,
            rev='4',
            entity_type='Activity_Types',
            name='New Introductions'
        ),
        ActivityType(
            stub=True,
            id=103,
            rev='1',
            entity_type='Activity_Types',
            name='Elevated Conversations / Leader Intros'
        )
    ]
)
```

## TODO

- Gracefully handle errors on method queries
- Convenience methods for common queries (Users, Leads, etc.)