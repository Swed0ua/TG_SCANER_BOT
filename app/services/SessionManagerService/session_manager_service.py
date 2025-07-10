from datetime import datetime
from typing import Optional, Dict


class Session:
    def __init__(
        self,
        telegram_id: int,
        access_token: str,
        access_expires_at: str,
        refresh_token: str,
        refresh_expires_at: str,
        csrf: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        self.telegram_id = telegram_id
        self.access_token = access_token
        self.access_expires_at = self._parse_dt(access_expires_at)
        self.refresh_token = refresh_token
        self.refresh_expires_at = self._parse_dt(refresh_expires_at)
        self.csrf = csrf
        self.created_at = datetime.utcnow()
        self.last_access_at = datetime.utcnow()
        self.metadata = metadata or {}

    def _parse_dt(self, dt_str: str) -> datetime:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

    def to_dict(self) -> Dict:
        return {
            "telegram_id": self.telegram_id,
            "access_token": self.access_token,
            "access_expires_at": self.access_expires_at.isoformat(),
            "refresh_token": self.refresh_token,
            "refresh_expires_at": self.refresh_expires_at.isoformat(),
            "csrf": self.csrf,
            "created_at": self.created_at.isoformat(),
            "last_access_at": self.last_access_at.isoformat(),
            "metadata": self.metadata
        }

    def update_tokens(
        self,
        access_token: str,
        access_expires_at: str,
        refresh_token: Optional[str] = None,
        refresh_expires_at: Optional[str] = None,
        csrf: Optional[str] = None
    ):
        self.access_token = access_token
        self.access_expires_at = self._parse_dt(access_expires_at)
        if refresh_token:
            self.refresh_token = refresh_token
        if refresh_expires_at:
            self.refresh_expires_at = self._parse_dt(refresh_expires_at)
        if csrf:
            self.csrf = csrf
        self.last_access_at = datetime.utcnow()


class SessionManagerService:
    def __init__(self):
        self._storage: Dict[int, Session] = {}

    def create_or_update_session(
        self,
        telegram_id: int,
        access_token: str,
        access_expires_at: str,
        refresh_token: str,
        refresh_expires_at: str,
        csrf: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        session = self._storage.get(telegram_id)
        if session:
            session.update_tokens(access_token, access_expires_at, refresh_token, refresh_expires_at, csrf)
        else:
            session = Session(
                telegram_id,
                access_token,
                access_expires_at,
                refresh_token,
                refresh_expires_at,
                csrf,
                metadata
            )
            self._storage[telegram_id] = session

    def get_session(self, telegram_id: int) -> Optional[Session]:
        return self._storage.get(telegram_id)

    def delete_session(self, telegram_id: int):
        if telegram_id in self._storage:
            del self._storage[telegram_id]

    def session_exists(self, telegram_id: int) -> bool:
        return telegram_id in self._storage

    def list_sessions(self) -> Dict[int, Dict]:
        return {tid: s.to_dict() for tid, s in self._storage.items()}
