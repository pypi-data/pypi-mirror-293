
mepost-python-sdk
=================

The `mepost-sdk` is a Python library designed to simplify interactions with the Mepost API. It provides convenient methods to send and manage messages efficiently. This SDK is ideal for developers looking to integrate Mepost messaging capabilities into their Python applications.

Features
--------

-   Send emails directly through the Mepost API.
-   Schedule and manage email deliveries.
-   Retrieve detailed information about scheduled messages.
-   Cancel scheduled messages.
-   Send emails using predefined templates.

Installation
------------

Install `mepost-sdk` using pip:

```bash
pip install mepost-sdk
```

Usage
-----

Here is a quick example to get you started:

```python
from mepost import MepostClient

# Create an instance of MepostClient with your API key
client = MepostClient('your_api_key_here')

# Send an email
email_data = {
    "from_email": "info@example.com",
    "from_name": "Example Company",
    "html": "This is a test email sent from the Mepost Python SDK.",
    "subject": "Example Subject",
    "to": [
        { "email": "recipient1@example.com" },
        { "email": "recipient2@example.com" }
    ]
}

response = client.send_email(email_data)
print(response)
```

API Methods
-----------

### `MepostClient(api_key)`

Initializes and returns a new instance of MepostClient.

-   Parameters
    -   `api_key`: Your Mepost API key.

### Company Endpoints

#### `add_domain(request: AddDomainRequest)`

Adds a domain to the Mepost account.

-   Parameters
    -   `request`: An object containing the domain to add.

#### `get_domain_list()`

Retrieves a list of domains associated with the Mepost account.

-   No parameters.

#### `remove_domain(request: RemoveDomainRequest)`

Removes a domain from the Mepost account.

-   Parameters
    -   `request`: An object containing the domain to remove.

### Groups Endpoints

#### `list_groups(limit: int = 10, page: int = 1)`

Retrieves a list of email groups.

-   Parameters
    -   `limit`: The maximum number of groups to return (default: 10).
    -   `page`: The page number for pagination (default: 1).

#### `create_group(request: CreateNewGroupRequest)`

Creates a new email group.

-   Parameters
    -   `request`: An object containing the details of the new group.

#### `delete_group(group_id: str)`

Deletes an email group.

-   Parameters
    -   `group_id`: The ID of the group to delete.

#### `get_group_by_id(group_id: str)`

Retrieves information about a specific email group.

-   Parameters
    -   `group_id`: The ID of the group to retrieve.

#### `update_group(group_id: str, request: RenameGroupRequest)`

Updates the name of an email group.

-   Parameters
    -   `group_id`: The ID of the group to update.
    -   `request`: An object containing the new group name.

### Subscribers Endpoints

#### `list_subscribers(group_id: str, limit: int = 10, page: int = 1)`

Retrieves a list of subscribers in a group.

-   Parameters
    -   `group_id`: The ID of the group.
    -   `limit`: The maximum number of subscribers to return (default: 10).
    -   `page`: The page number for pagination (default: 1).

#### `add_subscriber(group_id: str, request: CreateSubscriberRequest)`

Adds a subscriber to a group.

-   Parameters
    -   `group_id`: The ID of the group.
    -   `request`: An object containing subscriber details.

#### `delete_subscriber(group_id: str, request: DeleteSubscriberRequest)`

Deletes a subscriber from a group.

-   Parameters
    -   `group_id`: The ID of the group.
    -   `request`: An object containing the emails of subscribers to delete.

#### `get_subscriber_by_email(group_id: str, email: str)`

Retrieves subscriber details by email.

-   Parameters
    -   `group_id`: The ID of the group.
    -   `email`: The email address of the subscriber.

### Messages Endpoints

#### `get_message_info(schedule_id: str, email: str)`

Retrieves information about a specific scheduled message.

-   Parameters
    -   `schedule_id`: The ID of the scheduled message.
    -   `email`: The email address to which the message was sent.

#### `cancel_scheduled_message(request: CancelScheduledMessageRequest)`

Cancels a scheduled message.

-   Parameters
    -   `request`: An object containing the scheduled message ID.

#### `send_marketing(request: SendMarketingRequest)`

Sends a marketing email.

-   Parameters
    -   `request`: An object for sending marketing emails.

#### `send_message_by_template(request: SendMessageByTemplateRequest)`

Sends an email using a template.

-   Parameters
    -   `request`: An object containing the message details and template ID.

#### `get_schedule_info(schedule_id: str)`

Retrieves schedule information for a specific scheduled message.

-   Parameters
    -   `schedule_id`: The ID of the scheduled message.

#### `send_transactional(request: SendTransactionalRequest)`

Sends a transactional email.

-   Parameters
    -   `request`: An object for sending transactional emails.

#### `send_transactional_by_template(request: SendMessageByTemplateRequest)`

Sends a transactional email using a template.

-   Parameters
    -   `request`: An object containing the message details and template ID.

### Outbound IP Endpoints

#### `create_ip_group(request: CreateIpGroupRequest)`

Creates a new IP group.

-   Parameters
    -   `request`: An object containing the IP group details.

#### `get_ip_group_info(name: str)`

Retrieves information about a specific IP group.

-   Parameters
    -   `name`: The name of the IP group.

#### `list_ip_groups()`

Retrieves a list of all IP groups.

-   No parameters.

#### `cancel_warmup(request: CancelWarmUpRequest)`

Cancels a warmup process for an IP address.

-   Parameters
    -   `request`: An object containing the IP address.

#### `get_ip_info(ip: str)`

Retrieves information about a specific IP address.

-   Parameters
    -   `ip`: The IP address to retrieve.

#### `list_ips()`

Retrieves a list of all IP addresses.

-   No parameters.

#### `set_ip_group(request: SetIpGroupRequest)`

Assigns an IP address to a specific IP group.

-   Parameters
    -   `request`: An object containing the IP address and group details.

#### `start_warmup(request: StartWarmUpRequest)`

Starts a warmup process for an IP address.

-   Parameters
    -   `request`: An object containing the IP address.

Contributing
------------

Contributions are always welcome! Please read the contributing guide for ways to contribute to this project.

License
-------

`mepost-sdk` is released under the MIT License. See the LICENSE file for more details.
