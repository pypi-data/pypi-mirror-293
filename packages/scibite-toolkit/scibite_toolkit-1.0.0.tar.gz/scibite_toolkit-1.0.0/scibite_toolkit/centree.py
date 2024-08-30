import requests
import logging

# Get the logger for this module
logger = logging.getLogger(__name__)

class CentreeRequestBuilder:
    """
    Class for creating CENtree Requests.
    """

    def __init__(self, timeout: int = 10):
        """
        Initialize the CentreeRequestBuilder.

        Parameters
        ----------
        timeout : int, optional
            The timeout for HTTP requests in seconds (default is 10 seconds).
        """
        self.centree_url = ''
        self.headers = {}
        self.session = requests.Session()
        self.timeout = timeout
        self.logger: logging.Logger = logger

    def set_url(self, centree_url: str):
        """
        Set the URL of the CENtree instance.

        Parameters
        ----------
        centree_url : str
            The URL of the CENtree instance to be hit.

        Examples
        --------
        >>> crb.set_url("http://example.com")
        """
        self.centree_url = centree_url.rstrip('/')
        self.logger.info(f"Set CENtree URL to {self.centree_url}")

    def set_authentication(self, username: str, password: str, remember_me: bool = True, verification: bool = True):
        """
        Authenticates with the CENtree token API using username and password, generates an access token,
        and sets the request header.

        Parameters
        ----------
        username : str
            The username for authentication.
        password : str
            The password for authentication.
        remember_me : bool, optional
            Whether to remember the user (default is True).
        verification : bool, optional
            Whether to verify SSL certificates (default is True).

        Examples
        --------
        >>> crb.set_authentication("user", "pass")
        """
        authenticate_url = f"{self.centree_url}/api/authenticate"

        try:
            token_response = self.session.post(
                authenticate_url,
                json={
                    "rememberMe": remember_me,
                    "username": username,
                    "password": password,
                },
                headers={"Content-Type": "application/json"},
                verify=verification,
                timeout=self.timeout
            )
            token_response.raise_for_status()
            access_token = token_response.json().get("id_token")

            if not access_token:
                raise ValueError("Access token not found in the response.")

            self.headers = {"Authorization": f"Bearer {access_token}"}
            self.logger.info("Authentication successful")


        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.reason}")
            raise http_err  # Re-raise the HTTPError for the test to catch
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error: {req_err}")
            raise req_err  # Re-raise the RequestException for the test to catch
        except ValueError as val_err:
            self.logger.error(f"Value error: {val_err}")
            raise val_err  # Re-raise the ValueError for the test to catch
        except Exception as err:
            self.logger.error(f"An error occurred: {err}")
            raise err  # Re-raise the generic exception for the test to catch

    def search_classes(self, query: str, ontology_id: str = None, exact: bool = False, obsolete: bool = False,
                       page_from: int = 0, page_size: int = 10) -> dict:
        """
        Search classes in the CENtree ontology.

        Parameters
        ----------
        query : str
            The search query.
        ontology_id : str, optional
            The ontology ID to search within.
        exact : bool, optional
            Whether to perform an exact search (default is False).
        obsolete : bool, optional
            Whether to include obsolete classes (default is False).
        page_from : int, optional
            The starting page number (default is 0).
        page_size : int, optional
            The number of results per page (default is 10).

        Returns
        -------
        dict
            The JSON response from the search endpoint.

        Examples
        --------
        >>> result = crb.search_classes("diabetes")
        """
        params = {
            "q": query,
            "ontology": ontology_id,
            "from": page_from,
            "size": page_size
        }

        # Clean up params dictionary to remove None values
        params = {k: v for k, v in params.items() if v is not None}

        # Construct the endpoint URL
        endpoint_suffix = ''
        if obsolete:
            endpoint_suffix += '/obsolete'
        if exact:
            endpoint_suffix += '/exact'

        search_endpoint = f"{self.centree_url}/api/search{endpoint_suffix}"

        try:
            response = self.session.get(search_endpoint, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Search request successful")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request error occurred: {req_err}")
        except Exception as err:
            self.logger.error(f"An error occurred: {err}")