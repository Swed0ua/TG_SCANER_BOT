from datetime import datetime, timezone
from typing import Optional

from app.services.SessionManagerService.session_manager_service import SessionManagerService
from app.services.SmartkasaService.smartkasa_service import SmartKasaAPIError, SmartKasaService


class AuthHandler:
    def __init__(self, session_manager: SessionManagerService, kasa_service: SmartKasaService):
        self.sessions = session_manager
        self.kasa = kasa_service

    def is_logged_in(self, telegram_id: int) -> bool:
        session = self.sessions.get_session(telegram_id)
        if not session:
            return False
        now = datetime.now(timezone.utc)  # aware datetime в UTC
        return session.refresh_expires_at > now

    def login(self, telegram_id: int, phone: str, password: str) -> None:
        try:
            data = self.kasa.authenticate(phone, password)
        except SmartKasaAPIError as e:
            return False

        print(f"Login data: {data}")
        print(type(data))

        self.sessions.create_or_update_session(
            telegram_id=telegram_id,
            access_token=data["access_token"],
            access_expires_at=data["access_expires_at"],
            refresh_token=data["refresh_token"],
            refresh_expires_at=data["refresh_expires_at"],
            csrf=data.get("csrf")
        )

        return True

    def logout(self, telegram_id: int):
        session = self.sessions.get_session(telegram_id)
        if session:
            try:
                self.kasa.logout(session.access_token)
            except SmartKasaAPIError:
                pass  
            self.sessions.delete_session(telegram_id)

    def get_valid_access_token(self, telegram_id: int) -> Optional[str]:
        session = self.sessions.get_session(telegram_id)
        if not session:
            return None

        now = datetime.now(timezone.utc)  # aware datetime в UTC

        if session.access_expires_at > now:
            return session.access_token

        if session.refresh_expires_at > now:
            try:
                new_data = self.kasa.refresh_session(session.refresh_token)
                session.update_tokens(
                    access_token=new_data["access_token"],
                    access_expires_at=new_data["access_expires_at"]
                )
                return session.access_token
            except SmartKasaAPIError:
                self.sessions.delete_session(telegram_id)
                return None

        self.sessions.delete_session(telegram_id)
        return None