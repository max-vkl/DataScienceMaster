# Assignment 3

Group: 
* Max van Klinski
* Simon Stephan

## Setup of environment

### For running airflow

```
docker compose up
```

To get the logging mails you have to set the `email` variable in the `default_args`:

```python
default_args = {
    ...
    'email': <insert_you_email>,
    'email_on_retry': False,
    ...
}
```

We wrote an extra task that throws an exception. So if you want to test the error logging just replace the task list by this: 

```python
task_with_error
``` 


### For testing our scripts
1. Create python venv:
   ```
   python -m venv </path/to/new/virtual/environment>
   ```
2. activate venv (depends on OS)
3. install packages:
    ```
    pip install -r requiremnts.txt
   ```
4. Starten eines Testes:
   1. In `tests` Ornder navigieren mit `cd`
   ```
   python test_<function_to_test>.py
   ```
