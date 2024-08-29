import requests
import time
import uuid
import webbrowser

from keycloak import KeycloakOpenID
from urllib.parse import urlencode

class AuthenticationFailure(Exception):
    def __init__(self, message):
        self.message = message

class Job:
    def __init__ (self, job_id):
        self._job_id = job_id
    def id(self):
        return self._job_id

class StrafulProvider:

    _asp_net_port = "5001"
    _key_cloak_port = "8443"
    _client_id = "straful-client"
    _realm_name = "straful-realm"

    # use_https should be False only when testing but NEVER in production
    def __init__ (self, *, url, use_https = True, debug=False):
        self._verify = use_https
        self._debug = debug
        self._state = None
        self._token_info = None
        self._access_token = None
        self._refresh_token = None
        self._keycloak_openid = None
        self._provider_url = url.rstrip('/')
        self._asp_net_url = f'{self._provider_url}:{self._asp_net_port}'
        self._auth_call_back_url = f'{self._asp_net_url}/auth/callback'
        self._show_code_callback_url = f"{self._asp_net_url}/auth/showcode"
        self._keycloak_server_url = f'{self._provider_url}:{self._key_cloak_port}'

        if not self._is_server_online(self._keycloak_server_url):
            print(f"Error: the service you are trying to access at: {url}, appears to be down. Please doublecheck the service url.")
            return            

        self._keycloak_openid = KeycloakOpenID(server_url=self._keycloak_server_url,
                                 client_id=self._client_id,
                                 realm_name=self._realm_name,
                                 verify=self._verify)

    def authenticate(self):
        if self._keycloak_openid is None:
            print("Error: you must setup a provider first.")
            return
            
        try:
            self._token_info = None
            self._access_token = None
            self._refresh_token = None
            self._store_state()
            auth_url = self._get_authentication_url()
            webbrowser.open(auth_url)
            auth_code = self._get_autehntication_code()
            token_response = self._keycloak_openid.token(
                grant_type='authorization_code',
                code=auth_code,
                redirect_uri=self._auth_call_back_url
            )
            self._token_info = token_response
            self._access_token = token_response['access_token']
            self._refresh_token = token_response['refresh_token']
            self._token_expiration_time = time.time() + token_response['expires_in'] - 10
            self._refresh_token_expiration_time = time.time() + token_response['refresh_expires_in'] - 10
        except AuthenticationFailure:
            print("Failed to authenticate with the quantum provider.")
        except Exception as ex:
            print("Failed to authenticate with the quantum provider.")
            print("Unexpected exception: ", ex)

    def submit_job(self, *, backend, circuit_data, shots, comments):
        if self._keycloak_openid is None:
            print("Error: you must setup a provider first.")
            return
        if not backend:
            print("The backend name is empty.")
            return
        if not circuit_data:
            print("The circuit is empty.")
            return
        if not isinstance(shots, int):
            print("The number of shots must be specified as an integer number.")
            return
        if shots is None:
            print("The number of shots must be specified as an integer number.")
            return
        try:
            job_data = {
                "BackendName" : backend,
                "CircuitData" : circuit_data,
                "Shots" : shots,
                "Comments": comments,
            }
            (status_code, result) = self._make_post_request(f"{self._asp_net_url}/api/job", job_data)
            if status_code == 201:
                return Job(result["id"])
            elif status_code == 400:
                print("Bad request.")
            elif status_code == 401:
                print("You are not authorized to access this service. Try perhaps to authenticate again.")
            elif status_code == 406:
                print("The requested backenkend is not available or may be offline.")
            elif status_code == 500:
                print("Internal server error.")
            else:
                print(f"Job submission has failed with http status code: {status_code}.")
            return Job(None)
        except Exception as ex:
            print(ex)
            
    def get_backends(self):
        if self._keycloak_openid is None:
            print("Error: you must setup a provider first.")
            return
        try:
            response = self._make_get_request(f"{self._asp_net_url}/api/backends")
            status_code = response.status_code
            if status_code == 500:
                print("Internal server error.")
            elif status_code == 401:
                print("You are not authorized to access this service. Perhaps you should try to authenticate again.")
            elif status_code == 200:
                backends = response.json()
                for backend in backends:
                    print(backend["name"], "-", "Online" if backend["online"] else "Offline")
            else:
                print(f"Request has failed with http status code: {status_code}.")
        except Exception as ex:
            print(ex)

    def get_job_status(self, job):
        if self._keycloak_openid is None:
            print("Error: you must setup a provider first.")
            return
        if job.id is None:
            print("This job invalid.")
            return
        try:
            response = self._make_get_request(f"{self._asp_net_url}/api/job/status/{job.id()}")
            status_code = response.status_code
            if status_code == 500:
                print("Internal server error.")
            elif status_code == 401:
                print("You are not authorized to access this service. Perhaps you should try to authenticate again.")
            elif status_code == 200:
                print("Job status: ", response.text)
            else:
                print(f"Request has failed with http status code: {status_code}.")
        except Exception as ex:
            print(ex)

    def get_job_result(self, job):
        if self._keycloak_openid is None:
            print("Error: you must setup a provider first.")
            return
        if job.id is None:
            print("This job invalid.")
            return
        try:
            response = self._make_get_request(f"{self._asp_net_url}/api/job/result/{job.id()}")
            status_code = response.status_code
            if status_code == 500:
                print("Internal server error.")
            elif status_code == 401:
                print("You are not authorized to access this service. Perhaps you should try to authenticate again.")
            elif status_code == 200:
                print(response.text)
            else:
                print(f"Request has failed with http status code: {status_code}.")
        except Exception as ex:
            print(ex)

    def _make_get_request(self, api_url):
        if self.is_token_expired():
            self._refresh_tokens()
        return requests.get(api_url, headers={'Authorization': f'Bearer {self._access_token}'}, verify=self._verify)

    def _make_post_request(self, api_url, data):
        if self.is_token_expired():
            self._refresh_tokens()
            
        response = requests.post(api_url, json=data, headers={'Authorization': f'Bearer {self._access_token}'}, verify=self._verify)
        
        try:
            json = response.json()
        except:
            json = "{}"
            
        return (response.status_code, json)
    
    def is_token_expired(self):
        if not hasattr(self, "_token_expiration_time"):
            return True
        return time.time() > self._token_expiration_time

    def is_refresh_token_expired(self):
        if not hasattr(self, "_refresh_token_expiration_time"):
            return True
        return time.time() > self._refresh_token_expiration_time

    def _refresh_tokens(self):
        if hasattr(self, "_refresh_token_expiration_time") and self.is_refresh_token_expired():
            print("You session timed out, you need to re-authenticate!")
            raise AuthenticationFailure("Refresh token expired")
            
        token_response = self._keycloak_openid.token(
            grant_type='refresh_token',
            refresh_token=self._refresh_token
        )
        self._token_info = token_response
        self._access_token = token_response['access_token']
        self._refresh_token = token_response['refresh_token']

    def _is_server_online(self, url):
        try:
            response = requests.get(url, verify=self._verify)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            return False
    
    def _store_state(self):
        state = str(uuid.uuid4())
        session = requests.Session() 
        session_response = session.get(f"{self._asp_net_url}/auth/storestate", params={'state': state}, verify=self._verify)
        if session_response.status_code != 200:
            if not self._is_server_online(self._asp_net_url):
                print("The server seems to be down.")
            elif self._debug:
                print("The provider does not respond to store state in order to initiate autehntication.")
            raise AuthenticationFailure("Cannot store state to initiate authentication, provider does not respond")
        self._state = state

    def _get_authentication_url(self):
        auth_url_params = {
            'client_id': self._client_id,
            'redirect_uri': self._auth_call_back_url,
            'response_type': 'code',
            'scope': 'openid profile email',
            'kc_idp_hint': 'google',
            'state': self._state
        }
        return f"{self._keycloak_server_url}/realms/{self._realm_name}/protocol/openid-connect/auth?{urlencode(auth_url_params)}"

    def _get_autehntication_code(self):
        
        timeout_seconds = 300
        start_time = time.time()
        delta_t = time.time() - start_time
        
        while delta_t < timeout_seconds:
            
            if delta_t < 10:
                time.sleep(1)
            else:
                time.sleep(3)

            delta_t = time.time() - start_time
            
            try:
                response = requests.get(self._show_code_callback_url, params={'state': self._state},  verify=self._verify)
                if response.status_code == 400:
                    if response.text == "Authorization state is missing.":
                        raise AuthenticationFailure("Authorization state not found on remote server.")
                    continue
                data = response.text
                auth_code = data.split(": ")[1]
                return auth_code
            except requests.RequestException as e:
                if self._debug:
                    print(f"Error polling callback URL: {e}")
                raise AuthenticationFailure(f"Remote server not responding to attempts to retrieve authorization code.")
        
        if self._debug:
            print("Timeout reached. Authorization code not received.")
            
        raise AuthenticationFailure("Authorization code not received")
