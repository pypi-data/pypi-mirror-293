<a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
<a href="https://pypi.org/project/gmfy/"><img alt="pypi version" src="https://img.shields.io/pypi/v/gmfy"></a>
<a href="https://gmfycode.gitlab.yandexcloud.net/gmfy-sdk/gmfy-sdk-python/activity"><img alt="Number of tests" src="https://img.shields.io/badge/tests-42 passed-emerald"></a>

<br>
<div align="center">
  <a href="https://gmfy.io/">
    <img alt="GMFY" width="400" src="https://static.tildacdn.com/tild6136-3638-4632-b632-383132653436/logo.svg">
  </a>
</div>
<br>

Our project is Python library that allows easy integration with
gmfy API. With this SDK, you can conveniently manage mechanics
that allow you to adjust user behavior, but also measure the
effectiveness of such correction.

## How it works 🎮

GMFY receives events related to user actions in the gamified
system. This allows you to analyze user behavior before and
after the introduction of gamification.

Through the administrative interface, various game mechanics
are configured, taking into account incoming events. This is
how ratings and leaderboards are built, user achievements are
calculated and corporate currencies are awarded.

In order to give users feedback, you need to visualize your
achievements. This could be a block in an existing user
profile, contextual widgets, or a separate page with
achievement results, available to users authorized in the
gamified system.

# **Installation Guide ⤵️**

To install the library, you need to choose how you want to use it: **synchronously**, **asynchronously**, or **both**.
This approach ensures that you only install the necessary dependencies, keeping your project clean and efficient.
Depending on your use case, you can select the appropriate mode as follows:

- Use synchronously:

```bash
pip install 'gmfy[sync]'
```

- Use asynchronously:

```bash
pip install 'gmfy[async]'
```

- Use both synchronously and asynchronously:

```bash
pip install 'gmfy[sync,async]'
```

By selecting the appropriate mode, you ensure that your project includes only
the dependencies it needs, avoiding unnecessary clutter.

# **Quick Start ⭐**

#### _The first thing you need to do is *initialize the SDK* to interact with GMFY_

Import a synchronous or asynchronous class to initialize your data. As an example, we will consider both options

```python
from gmfy.sync_clients.gmfy_client import GMFYClientSync
from gmfy.async_clients.gmfy_client import GMFYClientAsync

### Synchronous use ###
gmfy_sync = GMFYClientSync(GMFY_API_KEY, GMFY_URL)

### Asynchronous use ###
gmfy_async = GMFYClientAsync(GMFY_API_KEY, GMFY_URL)
```

#### __❗Replace GMFY_API_KEY and GMFY_URL with your actual credentials.❗__

If you want to change such parameters as request verification or request timeout, you can specify these parameters additionally:

```python
from gmfy.sync_clients.gmfy_client import GMFYClientSync
from gmfy.async_clients.gmfy_client import GMFYClientAsync


### Synchronous use ###
gmfy_sync = GMFYClientSync(GMFY_API_KEY, GMFY_URL, verify=True, timeout=120)

### Asynchronous use ###
gmfy_async = GMFYClientAsync(GMFY_API_KEY, GMFY_URL, verify=True, timeout=120)
```
# __POST methods ➡️__

## 1️⃣ *_Create events to GMFY_*

### 1. *Define Event Types and Actions*

Create custom classes inheriting from **BaseEventType** and **BaseEventAction**. For example:

```python
from gmfy import BaseEventAction, BaseEventType


class EventType(BaseEventType):
    subscription = "subscription"
    register = "register"
    visit_user = "visit_user"


class EventAction(BaseEventAction):
    create = "create"
    remove = "remove"
```

- _**EventType** must inherit from **BaseEventType**_
- _**EventAction** must inherit from **BaseEventAction**_

You can also expand these classes with your own functionality,
for example likes or dislikes.

This needs to be done so that you can add your types and actions.

❕You can use both the list of events and single events. To begin with, we will analyze the use of sending several events ❕

### 2. *Create your events*

Now you need to create your own events. They can be classically, actionable, or have an idempotency key.
Depending on what type of event you need, inherit from a specific class:

- _Classic Event_

It can be an ordinary event, for example, user registration on the site:
```python
from gmfy import BaseEvent
from typing import Literal
from pydantic import Field


class RegisterEvent(BaseEvent):
    event_type: Literal[EventType.register] = Field(exclude=True)
```

- _Action Event_

This event is needed for actions that can be created and removed. For example, likes, subscriptions, and so on:
```python
from gmfy import BaseActionEvent
from typing import Literal
from pydantic import Field


class SubscriptionEvent(BaseActionEvent):
    event_type: Literal[EventType.subscription] = Field(exclude=True)
```

- _Unique Event_

This event is needed to identify the action. For example, viewing specific content:
```python
from gmfy import BaseUniqueEvent
from typing import Literal
from pydantic import Field


class VisitUserEvent(BaseUniqueEvent):
    event_type: Literal[EventType.visit_user] = Field(exclude=True)
```

#### ❗ **Important: If you skip this step, you will get a TypeError error**:

```text
TypeError: Event classes inherited from BaseEvent were not found in your project. Ensure you've created your events by inheriting from BaseEvents.
```
To resolve this issue, ensure that your events are properly set up by inheriting from `BaseEvents`.
Create a Python package and include a file where you initialize your classes that extend `BaseEvents`.
This step is essential for smooth operation.

### 3. *Prepare data for send events*

To send data, you can use class **EventData** to work with objects:

```python
from gmfy.data import EventData

create_subscription_event = EventData(
        event_type=EventType.subscription,
        user_id=f"{user_id}",
        event_action=EventAction.create
    ).model_dump(by_alias=True)

register_event = EventData(
        event_type=EventType.register,
        user_id=f"{user_id}",
    ).model_dump(by_alias=True)

visit_user_event = EventData(
        event_type=EventType.visit_user,
        user_id=f"{user_id}",
        idempotence_key=f"{instance.id}",
    ).model_dump(by_alias=True)

event_data = [create_subscription_event, register_event, visit_user_event]
```

Or you can use a dictionary structure to provide the data to be sent

```python
event_data = [
    {
        "event_type": EventType.subscription,
        "user_id": f"{user.id}",
        "event_action": EventAction.create,
    },
    {
        "event_type": EventType.register,
        "user_id": f"{user.id}",
    },
    {
        "event_type": EventType.visit_user,
        "user_id": f"{user.id}",
        "idempotence_key": f"{instance.id}",
    },
]
```

### 4. *Send events*

Now that you have prepared the data for sending, you can send a request to GMFY and create an event.

To do this, call the **create_batch_events** method regardless of what type of synchronization you have chosen

```python
### Synchronous use ###
gmfy_sync.create_batch_events(event_data)

### Asynchronous use ###
await gmfy_async.create_batch_events(event_data)
```

### Well, now let's figure out how you can send not just a list of events, but single events

The basic logic for preparing the data and sending the request does not change.
The only important thing is that now you need to work with dict instead of list.
Let's see the differences from these options:

### 1. *Prepare data for send single event*

```python
from gmfy import EventData

event_data = EventData(
    event_type=EventType.subscription,
    user_id=f"{user_id}",
    event_action=EventAction.create
).model_dump(by_alias=True)
```

Well, according to tradition, if you want to work directly with dictionaries, then do this:

```python
event_data = {
    "event_type": EventType.subscription,
    "user_id": f"{user.id}",
    "event_action": EventAction.create,
},
```
### 2. *Create your event*
```python
from gmfy import BaseActionEvent
from typing import Literal
from pydantic import Field


class SubscriptionEvent(BaseActionEvent):
    event_type: Literal[EventType.subscription] = Field(exclude=True)
```

### 3. *Send single event*

Now we can send a request to create one event. To do this, use the **create_event** method as follows:

```python
### Synchronous use ###
gmfy_sync.create_event(event_data)

### Asynchronous use ###
await gmfy_async.create_event(event_data)
```

## 2️⃣ *_Create payments to GMFY_*

To send a post request to send a payment to GMFY, follow these steps:

### 1. Prepare data for send payment

Similar to the previous example, you can use a class or create your own data dictionary.
Both options are presented below:

- Using the class PaymentData:

```python
from gmfy import PaymentData, LocaleEnum

payment_data = PaymentData(
    amount={"value": 100, "currency": "USD"},
    confirmation={"returnUrl": "https://example.com/"},
    user_id=f"{user_id}",
    description="Payment for order #123",
    locale=LocaleEnum.EN,
).model_dump(by_alias=True)
```

- Using dictionary:

```python
from gmfy import LocaleEnum

payment_data = {
    "amount": {"value": 100, "currency": "USD"},
    "confirmation": {"returnUrl": "https://example.com/"},
    "user_id": f"{user_id}",
    "description": "Payment for order #123",
    "locale": LocaleEnum.EN,
}
```

### 2. Use basic ones or create your own classes for data management

To validate data, you can use the base classes **BasePayment**, **BaseAmount** and
**BaseConfirmation** or override them if you have such a need:

- Use base classes:

```python
from gmfy import BasePayment

payment = BasePayment(**payment_data)
```

- Create your own classes:

```python
from pydantic import Field

from gmfy import BasePayment, BaseAmount, BaseConfirmation


class CustomAmount(BaseAmount): ...
# modify the class according to your needs


class CustomConfirmation(BaseConfirmation): ...
# modify the class according to your needs


class CustomPayment(BasePayment):
    amount: CustomAmount = Field(...)
    confirmation: CustomConfirmation = Field(...)
    # modify the class according to your needs
```

### 3. Use the **create_payment** method to send a request to GMFY:

- If you used a base class:

```python
### Synchronous use ###
gmfy_sync.create_payment(BasePayment(**payment_data))

### Asynchronous use ###
await gmfy_async.create_payment(BasePayment(**payment_data))
```

- If you created your own class:

```python
### Synchronous use ###
gmfy_sync.create_payment(CustomPayment(**payment_data))

### Asynchronous use ###
await gmfy_async.create_payment(CustomPayment(**payment_data))
```

#### _Unlike creating an event, when creating a payment you will receive a response statusof **200**, not **201**, as
well as a response from the server:_

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "CREATED",
  "confirmationUrl": "string"
}
```

## 3️⃣ *_Create resend code to GMFY_*

You can also create a resend code by passing the payment id like this:

```python
### Synchronous use ###
gmfy_sync.create_resend_code(payment_id=f"{payment_id}")

### Asynchronous use ###
await gmfy_async.create_resend_code(payment_id=f"{payment_id}")
```

It is important to note that you will receive a 200 OK status in response, as well as the following response:

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "value": 0,
  "returnUrl": "string",
  "description": "string",
  "currency": "string",
  "status": "CREATED",
  "locale": "RU",
  "expiresIn": 0
}
```

# __GET methods ⬅️__

## *_1️⃣ Get user's data from GMFY_*

You can get information about all users or information about one user by ID using the **get_users** method

1) _Get a list of all users information:_

```python
### Synchronous use ###
gmfy_sync.get_users()

### Asynchronous use ###
await gmfy_async.get_users()
```

2) _Get information about one user by id_

```python
### Synchronous use ###
gmfy_sync.get_users(user_id=f"{user_id}")

### Asynchronous use ###
await gmfy_async.get_users(user_id=f"{user_id}")
```

*️⃣ _Example response:_

```json
[
  {
    "userId": "string",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "userRatings": [
      {
        "userId": "string",
        "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "ratingId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "value": 0,
        "metaInfo": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "position": 0
      }
    ],
    "userChallenges": [
      {
        "userId": "string",
        "challengeId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "progress": 0,
        "passedSteps": [
          {
            "challengeStepId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "order": 0,
            "weight": 0,
            "dateComplete": "2024-08-19T13:03:31.653Z"
          }
        ],
        "metaInfo": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "name": "string"
      }
    ],
    "userBadges": [
      {
        "userId": "string",
        "badgeId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "acquisitionDate": "2024-08-19T13:03:31.653Z",
        "metaInfo": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "name": "string",
        "description": "string",
        "permanent": true,
        "count": 0
      }
    ],
    "userFeatures": [
      {
        "userId": "string",
        "featureId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "accessDate": "2024-08-19T13:03:31.653Z",
        "metaInfo": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "name": "string",
        "description": "string"
      }
    ],
    "userAccountBalances": [
      {
        "userId": "string",
        "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "resourceKey": "string",
        "amount": 0
      }
    ]
  }
]
```

## *_2️⃣ Get user badges by user id_*

To get a list of user badges, use the **get_user_badges** method, passing it the user id:

```python
### Synchronous use ###
gmfy_sync.get_user_badges(user_id=f"{user_id}")

### Asynchronous use ###
await gmfy_async.get_user_badges(user_id=f"{user_id}")
```

*️⃣ _Example response:_

```json
[
  {
    "userId": "string",
    "badgeId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "acquisitionDate": "2024-08-19T14:34:11.608Z",
    "metaInfo": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "name": "string",
    "description": "string",
    "permanent": true,
    "count": 0
  }
]
```

## *_3️⃣ Get top of users in rating_*

Also you can get top of users in rating by id:

```python
### Synchronous use ###
gmfy_sync.get_rating_top_users(rating_id=f"{rating_id})

### Asynchronous use ###
await gmfy_async.get_rating_top_users(rating_id=f"{rating_id}")
```

_❗By default request has parameters **offset = 0, limit = 10, sorted by ASC**.
But if you want to override them, you can do it like this:_

```python
### Synchronous use ###
gmfy_sync.get_rating_top_users(
    rating_id=f"{rating_id}",
    offset=5,
    limit=20,
    sort="DESC"
)

### Asynchronous use ###
gmfy_async.get_rating_top_users(
    rating_id=f"{rating_id}",
    offset=5,
    limit=20,
    sort="DESC"
)

```

*️⃣ _Example response:_

```json
[
  {
    "userId": "string",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "ratingId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "value": 0,
    "metaInfo": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "position": 0
  }
]
```

## *_4️⃣ Get top of users in challenge_*

You can get top of users in challenge by id:

```python
### Synchronous use ###
gmfy_sync.get_challenge_top_users(challenge_id=f"{challenge_id}")

### Asynchronous use ###
await gmfy_async.get_challenge_top_users(challenge_id=f"{challenge_id}")
```

_❗By default request has parameter **limit = 10**. But if you want to override them, you can do it like this:_

```python
### Synchronous use ###
gmfy_sync.get_challenge_top_users(challenge_id=f"{challenge_id}", limit=20)

### Asynchronous use ###
await gmfy_async.get_challenge_top_users(challenge_id=f"{challenge_id}", limit=20)
```

*️⃣ _Example response:_

```json
[
  {
    "userId": "string",
    "challengeId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "progress": 0,
    "passedSteps": [
      {
        "challengeStepId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "order": 0,
        "weight": 0,
        "dateComplete": "2024-08-19T14:20:26.219Z"
      }
    ],
    "metaInfo": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "name": "string"
  }
]
```

## *_5️⃣ Get information about payment by id_*

Using the **get_payment** method you can get payment information like this

```python
### Synchronous use ###
gmfy_sync.get_payment(payment_id=f"{payment_id}")

### Asynchronous use ###
await gmfy_async.get_payment(payment_id=f"{payment_id}")
```

- *️⃣ _Example response:_

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "value": 0,
  "returnUrl": "string",
  "description": "string",
  "currency": "string",
  "status": "CREATED",
  "locale": "RU",
  "expiresIn": 0
}
```

## *_6️⃣ Get notification's information_*

You can receive notifications using the **get_notifications** method like this:

```python
### Synchronous use ###
gmfy_sync.get_notifications()

### Asynchronous use ###
await gmfy_async.get_notifications()
```

- *️⃣ _Example response:_

```json
[
  {
    "userId": "string",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "message": "string"
  }
]
```

## *_7️⃣ Get unread notification's information_*:
You can also get information about unread notifications of all users, or for a single user, if you specify his id.
This can be done using the **get_unread_notifications()** method:

- Get unread notifications for all users:
```python
### Synchronous use ###
gmfy_sync.get_unread_notifications()

### Asynchronous use ###
await gmfy_async.get_unread_notifications()
```

- Get unread notifications for single user by id:
```python
### Synchronous use ###
gmfy_sync.get_unread_notifications(user_id=f"{user_id}")

### Asynchronous use ###
await gmfy_async.get_unread_notifications(user_id=f"{user_id}")
```

- *️⃣ _Example response for both options:_

```json
[
  {
    "userId": "string",
    "clientId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "message": "string"
  }
]
```

## *_8️⃣ Get version of API GMFY_*

And, of course, you can get the API version using previously initialized classes using the **get_api_version** method

```python
### Synchronous use ###
gmfy_sync.get_api_version()

### Asynchronous use ###
await gmfy_async.get_api_version()
```

*️⃣ _Example response:_

```json
{
  "version": "1.0",
  "deploymentDate": "2024-07-22T17:28:03.876Z"
}
```

# **Contributors and Contact 💬**

The GMFY SDK library were developed by *Evgeny Izvekov* and *Yuriy Belotserkovskiy*,
and is actively maintained by our team. If you have any
questions, suggestions, or feedback, feel free to reach out to us.

- **Evgeny Izvekov**
    - <a href=https://gitlab.rdclr.ru/evgeny.izvekov>*GitLab*</a>
    - <a href=mailto:evgeny.izvekov@redcollar.ru>*Email*</a>


- **Yuriy Belotserkovskiy**
    - <a href=https://gitlab.rdclr.ru/yuriy.belotserkovskiy>*GitLab*</a>
    - <a href=mailto:yuriy.belotserkovskiy@redcollar.ru>*Email*</a>

### **Happy gamifying! 👾**
