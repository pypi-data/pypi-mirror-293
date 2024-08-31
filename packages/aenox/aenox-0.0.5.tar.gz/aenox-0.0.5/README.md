## ⚙️ Installation
Python 3.10 or higher is required
```
pip install aenox
```

## 🚀 Example Usage
To be able to perform your API query properly, replace `[YOUR_API_KEY]` with a valid API key.

### Example

```python
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")

api.test()  # Prints "Success!" if it is installed correctly
```


## 🫧 Cooldown
The API has a 10-second cooldown period for each query. This means you must wait 10 seconds between two requests. If you attempt to send another request before this time has passed, you will receive a `noxii.errors.CooldownError`.

### Example
You cannot run this query twice within 10 seconds:
```python
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")

await api.get_user_stats(user_id=123)
```

In such cases, use `try/except` to handle the error. For example:

```python
from aenox import CooldownError
from aenox import AenoXAPI

api = AenoXAPI(api_key="[YOUR_API_KEY]")

try:
    await api.get_user_stats(user_id=123)
except CooldownError:
    print('Cooldown!')
```

