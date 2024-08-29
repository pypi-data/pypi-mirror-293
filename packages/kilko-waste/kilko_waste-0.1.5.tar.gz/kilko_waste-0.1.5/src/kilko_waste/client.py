from typing import List
from kilko_waste.requests import (
    login_request,
    balance_request,
    config_request,
    events_request,
    LoginRequest,
    AuthenticatedRequest,
)
from kilko_waste.definitions.config_response import ConfigResponse
from kilko_waste.definitions.events_response import Event

# Kilko is a waste management company that operates in the Netherlands
class KilkoClient:
    logged_in: bool
    token: str
    app_url: str
    client_name: str

    def __init__(self, app_url = "mykliko.kcm.com", client_name = "Ouder Amstel") -> None:
        self.logged_in = False
        self.app_url = app_url
        self.client_name = client_name

    def login(self, user: int, password: str):
        body = LoginRequest(user, password, self.app_url, self.client_name)
        response = login_request(body)
        self.logged_in = True
        self.token = response.token

    def balance(self) -> float:
        if not self.logged_in:
            print("You must be logged in!")
            raise Exception
        body = AuthenticatedRequest(self.app_url, self.token)
        response = balance_request(body)

        return response.balance

    # TODO
    def containers(self):
        raise NotImplementedError

    def configuration(self) -> ConfigResponse:
        if not self.logged_in:
            print("You must be logged in!")
            raise Exception
        body = AuthenticatedRequest(self.app_url, self.token)
        return config_request(body)

    def events(self) -> List[Event]:
        if not self.logged_in:
                print("You must be logged in!")
                raise Exception
        body = AuthenticatedRequest(self.app_url, self.token)
        return events_request(body)
