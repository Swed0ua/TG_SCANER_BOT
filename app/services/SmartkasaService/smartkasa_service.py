import requests
from typing import Dict, Optional


class SmartKasaAPIError(Exception):
    pass

class SmartKasaService:
    BASE_URL = "https://core.smartkasa.ua"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _build_headers(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        if refresh_token:
            headers["X-Refresh-Token"] = refresh_token
        return headers

    def authenticate(self, phone_number: str, password: str) -> Dict[str, str]:
        url = f"{self.BASE_URL}/api/v1/auth/sessions"
        payload = {
            "session": {
                "phone_number": phone_number,
                "password": password
            }
        }
        headers = self._build_headers()
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            data = response.json().get("data", {})
            return {
                "access_token": data.get("access"),
                "access_expires_at" : data.get("access_expires_at"),
                "refresh_token": data.get("refresh"),
                "refresh_expires_at": data.get("refresh_expires_at"),
            }
        raise SmartKasaAPIError(f"Authentication failed: {response.status_code}, {response.text}")

    def refresh_session(self, refresh_token: str) -> str:
        url = f"{self.BASE_URL}/api/v1/auth/refresh"
        headers = self._build_headers(refresh_token=refresh_token)
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("data", {})
            return {
                "access_token": data.get("access"),
                "access_expires_at" : data.get("access_expires_at"),
                "refresh_token": data.get("refresh"),
                "refresh_expires_at": data.get("refresh_expires_at"),
            }
        raise SmartKasaAPIError(f"Refresh failed: {response.status_code}, {response.text}")

    def logout(self, access_token: str) -> None:
        url = f"{self.BASE_URL}/api/v1/auth/logout"
        headers = self._build_headers(access_token=access_token)
        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            raise SmartKasaAPIError(f"Logout failed: {response.status_code}, {response.text}")
