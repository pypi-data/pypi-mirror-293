# Django Admin Plugin

Django Admin Plugins to enhance django admin abilities

<div>
  <a href="https://badge.fury.io/py/django-admin-plugin">
      <img src="https://badge.fury.io/py/django-admin-plugin.svg" alt="Version"/>
  </a>
</div>

## Quickstart

1 - Install with `pip`:

```bash
pip install django-admin-plugin
```

## Quickstart

```python
# admin.py
from django_admin_plugin.admin import ActionButton
from django_admin_plugin.admin import ActionButtonAdmin


class MyCustomAdmin(ActionButtonAdmin):
        action_buttons = (
            ActionButton(
                name="Activate", model_function="activate", color="green"
            ),
            ActionButton(
                name="Deactivate", model_function="deactivate", color="red"
            ),
        )
```

```python
INSTALLED_APPS = [
    ...
    "django_admin_plugin",
]

```



## Initialize And Sync

1 - Create action button permissions
```bash
python manage.py init_admin_plugin
```

![action-button.png](docs%2Fimage%2Faction-button.png)
