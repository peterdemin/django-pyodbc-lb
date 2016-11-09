django-pyodbc-lb
================

Database engine based on django-pyodbc-azure that overrides database connection.
If `OPTIONS` dictionary contains `load_balancer` it must be an object with `choose` method which returnds list of hosts.

Example configuration::

    DATABASES = {
        'default': {
            'ENGINE': 'sql_server_lb',
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'password'
            'HOST': 'host',  # Not used
            'PORT': 1433,
            'COMMAND_TIMEOUT': 360,
            'CONN_MAX_AGE': 3600,  # Persistent connection limited to an hour
            'OPTIONS': {
                'load_balancer': LoadBalancer('database'),
                'driver': 'FreeTDS',
                'host_is_server': True,
                'extra_params': 'TDS_Version=7.3',
            }
        },
    }
