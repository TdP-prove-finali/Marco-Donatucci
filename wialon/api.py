#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ssl

try:
    from builtins import str
except:
    str = lambda x: "%s" % x

try:
    from urllib import urlencode
    from urlparse import urljoin
except Exception:
    from urllib.parse import urlencode, urljoin

try:
    from urllib2 import Request, urlopen, HTTPError, URLError
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

try:
    import libs.simplejson as json

    assert json  # Silence potential warnings from static analysis tools
except ImportError:
    import json

import gzip
import io


class WialonError(Exception):
    """
    Exception raised when an Wialon Remote API call fails due to a network
    related error or for a Wialon specific reason.
    """
    errors = {
        1: 'Invalid session',
        2: 'Invalid service',
        3: 'Invalid result',
        4: 'Invalid input',
        5: 'Error performing request',
        6: 'Unknown error',
        7: 'Access denied',
        8: 'Invalid user name or password',
        9: 'Authorization server is unavailable, please try again later',
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists',
        1003: 'Only one request of given time is allowed at the moment'
    }

    def __init__(self, code, text):
        self._text = text
        self._code = code
        try:
            self._code = int(code)
        except ValueError:
            pass

    def __unicode__(self):
        explanation = self._text
        if (self._code in WialonError.errors):
            explanation = " ".join([WialonError.errors[self._code], self._text])

        message = u'{error} ({code})'.format(error=explanation, code=self._code)
        return u'WialonError({message})'.format(message=message)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return str(self)


class Wialon(object):
    request_headers = {
        'Accept-Encoding': 'gzip, deflate'
    }

    def __init__(self, scheme='https', host="hst-api.wialon.com", port=443, sid=None, **extra_params):
        """
        Created the Wialon API object.
        """
        self._sid = sid
        self.__default_params = {}
        self.__default_params.update(extra_params)

        self.__base_url = (
            '{scheme}://{host}:{port}'.format(
                scheme=scheme,
                host=host,
                port=port
            )
        )

        self.__base_api_url = urljoin(self.__base_url, 'wialon/ajax.html?')

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, value):
        self._sid = value

    def update_extra_params(self, **params):
        """
        Updated the Wialon API default parameters.
        """
        self.__default_params.update(params)

    def avl_evts(self):
        """
        Call avl_event request
        """
        url = urljoin(self.__base_url, 'avl_evts')
        params = {
            'sid': self.sid
        }

        return self.request('avl_evts', url, params)

    def call(self, action_name, *argc, **kwargs):
        """
        Call the API method provided with the parameters supplied.
        """

        if (not kwargs):
            # List params for batch
            if isinstance(argc, tuple) and len(argc) == 1:
                params = json.dumps(argc[0], ensure_ascii=False)
            else:
                params = json.dumps(argc, ensure_ascii=False)
        else:
            params = json.dumps(kwargs, ensure_ascii=False)

        if action_name.startswith('unit_group'):
            if len(action_name) < 12:
                raise ValueError(f'Invalid action name {action_name}')
            action_name = 'unit_group/' + action_name[11:]
        elif action_name == 'core/search_items':
            pass
        elif action_name == 'unit/exec_cmd':
            pass
        elif action_name == 'unit/set_active':
            pass
        elif action_name == 'item/update_name':
            pass
        else:
            action_name = action_name.replace('_', '/', 1)

        params = {
            'svc': action_name,
            'params': params.encode("utf-8"),
            'sid': self.sid
        }

        all_params = self.__default_params.copy()
        all_params.update(params)
        return self.request(action_name, self.__base_api_url, all_params)

    def token_login(self, *args, **kwargs):
        kwargs['appName'] = 'python-wialon'
        return self.call('token_login', *args, **kwargs)

    def request(self, action_name, url, params):
        url_params = urlencode(params)
        data = url_params.encode('utf-8')
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            request = Request(url, data, headers=self.request_headers)
            response = urlopen(request, context=context)
            response_content = response.read()
        except HTTPError as e:
            raise WialonError(0, u"HTTP {code}".format(code=e.code))
        except URLError as e:
            raise WialonError(0, str(e))

        response_info = response.info()
        content_type = response_info.get('Content-Type')
        content_encoding = response_info.get('Content-Encoding')

        if content_encoding == 'gzip':
            buffer = io.BytesIO(response_content)
            f = gzip.GzipFile(fileobj=buffer)
            try:
                result = f.read()
            finally:
                f.close()
                buffer.close()
        else:
            result = response_content

        try:
            if content_type == 'application/json':
                result = result.decode('utf-8', errors='ignore')
                result = json.loads(result)
        except ValueError as e:
            raise WialonError(
                0,
                u"Invalid response from Wialon: {0}".format(e),
            )

        if (isinstance(result, dict) and 'error' in result and result['error'] > 0):
            raise WialonError(result['error'], action_name)

        errors = []
        if isinstance(result, list):
            # Check for batch errors
            for elem in result:
                if (not isinstance(elem, dict)):
                    continue
                if "error" in elem:
                    errors.append("%s (%d)" % (WialonError.errors[elem["error"]], elem["error"]))

        if (errors):
            errors.append(action_name)
            raise WialonError(0, " ".join(errors))

        return result

    def __getattr__(self, action_name):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self)

    def search_items(self, spec=None, force=1, flags=5243137, from_=0, to_=0):
        """
        Search for items based on the provided specification.

        Args:
            spec (dict): The specification for the search.
            force (int): Force the search (1 for yes, 0 for no).
            flags (int): Flags for the search.
            from_ (int): Start index for the search.
            to_ (int): End index for the search.

        Returns:
            dict: The search results.

        Raises:
            WialonError: If an error occurs during the search.
        """
        params = {
            'spec': spec,
            'force': force,
            'flags': flags,
            'from': from_,
            'to': to_
        }
        try:
            result = self.call('core/search_items', params)
            return result
        except WialonError as e:
            raise WialonError( 0,
                u"Invalid response from Wialon: {0}".format(e),)

    def execute_cmd(self, params=None):
        try:
            result_cmd = self.call('unit/exec_cmd', params)
            return result_cmd
        except WialonError as e:
            raise WialonError(0, u"Invalid response from Wialon: {0}".format(e),)

    def active_unit(self, unit_id):
        params = {
            "itemId": unit_id,
            "active": 1
        }
        try:
            result_activation = self.call('unit/set_active', params)
            return result_activation
        except WialonError as e:
            raise WialonError(0, u"Invalid response from Wialon: {0}".format(e),)

    def update_name(self, unit_id, name):
        params = {
            "itemId": unit_id,
            "name": str(name)
        }
        try:
            result_cmd = self.call('item/update_name', params)
            return result_cmd
        except WialonError as e:
            raise WialonError(0, u"Invalid response from Wialon: {0}".format(e),)


if __name__ == '__main__':
    try:
        wialon_api = Wialon()
        # token/login request
        token = 'TEST TOKEN HERE'
        result = wialon_api.token_login(token=token)
        wialon_api.sid = result['eid']
        # get events
        result = wialon_api.avl_evts()
        # core/logout request
        wialon_api.core_logout()
    except WialonError:
        pass
