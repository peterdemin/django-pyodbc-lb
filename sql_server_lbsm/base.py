"""
MS SQL Server database backend for Django with LBSM
"""
import os
import re
import time

from sql_server.pyodbc.base import (
    Database,
    DatabaseWrapper as BaseDatabaseWrapper,
    DatabaseClient,
    DatabaseCreation,
    DatabaseFeatures,
    DatabaseIntrospection,
    DatabaseOperations,
    DatabaseSchemaEditor,
    encode_connection_string,
)


__all__ = [
    'DatabaseWrapper',
    'DatabaseClient',
    'DatabaseCreation',
    'DatabaseFeatures',
    'DatabaseIntrospection',
    'DatabaseOperations',
    'DatabaseSchemaEditor',
]


class RetryException(Exception):
    pass


class DatabaseWrapper(BaseDatabaseWrapper):
    _unrecoverable_error_numbers = (
        '18456',  # login failed
        '18486',  # account is locked
        '18487',  # password expired
        '18488',  # password should be changed
        '18452',  # login from untrusted domain
    )

    def get_new_connection(self, conn_params):
        hosts = self.get_mirror_hosts(conn_params)
        connection_strings = [
            self.get_connection_string(conn_params, host)
            for host in hosts
        ]
        options = conn_params.get('OPTIONS', {})
        return self.retrying_connect(connection_strings, options)

    def get_mirror_hosts(self, conn_params):
        options = conn_params.get('OPTIONS', {})
        if 'failover_partner' in options:
            return [conn_params.get('HOST', 'localhost'),
                    options['failover_partner']]
        elif 'load_balancer' in options:
            return options['load_balancer'].choose()
        else:
            return [conn_params.get('HOST', 'localhost')]

    def retrying_connect(self, connection_strings, options, timeout=5):
        retry_time = 0.08 * timeout
        retry_delay = 0.2
        end_time = time.time() + timeout
        while True:
            for connection_string in connection_strings:
                try:
                    return self.try_connection(connection_string, options, retry_time)
                except RetryException as rexc:
                    if time.time() > end_time:
                        raise rexc.args[0]
                    time.sleep(retry_delay)
                    retry_time += 0.08 * timeout
                    retry_delay = min(1, retry_delay * 2)

    def try_connection(self, connection_string, options, timeout):
        unicode_results = options.get('unicode_results', False)
        try:
            return Database.connect(connection_string,
                                    unicode_results=unicode_results,
                                    timeout=timeout)
        except Exception as e:
            for error_number in self._unrecoverable_error_numbers:
                if error_number in e.args[1]:
                    raise
            raise RetryException(e)

    def get_connection_string(self, conn_params, host):
        database = conn_params['NAME']
        user = conn_params.get('USER', None)
        password = conn_params.get('PASSWORD', None)
        port = conn_params.get('PORT', None)
        default_driver = 'SQL Server' if os.name == 'nt' else 'FreeTDS'
        options = conn_params.get('OPTIONS', {})
        driver = options.get('driver', default_driver)
        dsn = options.get('dsn', None)

        # unixODBC uses string 'FreeTDS'; iODBC requires full path to lib
        if driver == 'FreeTDS' or driver.endswith('/libtdsodbc.so'):
            driver_is_freetds = True
        else:
            driver_is_freetds = False

        # Microsoft driver names assumed here are:
        # * SQL Server
        # * SQL Native Client
        # * SQL Server Native Client 10.0/11.0
        # * ODBC Driver 11 for SQL Server
        ms_drivers = re.compile('.*SQL (Server$|(Server )?Native Client)')

        cstr_parts = {}
        if dsn:
            cstr_parts['DSN'] = dsn
        else:
            # Only append DRIVER if DATABASE_ODBC_DSN hasn't been set
            cstr_parts['DRIVER'] = driver

            if ms_drivers.match(driver) or driver_is_freetds and options.get('host_is_server', False):
                if port:
                    cstr_parts['PORT'] = str(port)
                cstr_parts['SERVER'] = host
            else:
                cstr_parts['SERVERNAME'] = host

        if user:
            cstr_parts['UID'] = user
            cstr_parts['PWD'] = password
        else:
            if ms_drivers.match(driver):
                cstr_parts['Trusted_Connection'] = 'yes'
            else:
                cstr_parts['Integrated Security'] = 'SSPI'

        cstr_parts['DATABASE'] = database

        if ms_drivers.match(driver) and not driver == 'SQL Server':
            self.supports_mars = True
        if self.supports_mars:
            cstr_parts['MARS_Connection'] = 'yes'

        connstr = encode_connection_string(cstr_parts)

        # extra_params are glued on the end of the string without encoding,
        # so it's up to the settings writer to make sure they're appropriate -
        # use encode_connection_string if constructing from external input.
        if options.get('extra_params', None):
            connstr += ';' + options['extra_params']
        return connstr
