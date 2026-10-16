from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import httpx
from dotenv import load_dotenv


class Presence(StrEnum):
    ON_SITE = "on-site"
    HYBRID = "hybrid"
    REMOTE = "remote"


@dataclass(slots=True)
class JobOffer:
    company: str
    published_date: str
    role: str
    description: str
    location: str
    presence: Presence
    job_url: str


def _parse_presence(value: Any) -> Presence:
    normalized = str(value or "").strip().lower()
    if "remote" in normalized:
        return Presence.REMOTE
    if "hybrid" in normalized:
        return Presence.HYBRID
    return Presence.ON_SITE


class LinkedIn_Jobs:
    """Adapter for fetching LinkedIn job offers via RapidAPI."""

    def __init__(self) -> None:
        load_dotenv()
        self.rapidAPI_url = os.getenv("RapidAPI_url", "")
        self.rapidAPI_linkedin_host = os.getenv("RapidAPI_linkedIn_host", "")
        self.rapidAPI_key = os.getenv("X-RapidAPI-Key", "")

    async def get_jobs(self, role: str, time_frame: str = "24h") -> list[JobOffer]:
        from app.main import app  # deferred import: reuse the singleton httpx client

        client: httpx.AsyncClient = app.state.httpx_client
        url = f"https://{self.rapidAPI_linkedin_host}/rapidapi.com/active-jb?"
        headers = {
            "x-rapidapi-host": self.rapidAPI_linkedin_host,
            "x-rapidapi-key": self.rapidAPI_key,
        }
        params = {
            "title": role,
            "location": "Spain OR Madrid OR remote",
            "time_frame": time_frame,
            "limit": 20,
            "description_format": "text",
            "ai_work_arrangement": "Hybrid, Remote OK, Remote Solely",
        }

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = payload.get("data") or payload.get("jobs") or []
        else:
            items = []

        offers: list[JobOffer] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            offers.append(
                JobOffer(
                    company=str(item.get("organization") or item.get("company") or ""),
                    published_date=str(item.get("date_posted") or item.get("published_date") or ""),
                    role=str(item.get("title") or item.get("role") or role),
                    description=str(item.get("description_text") or item.get("description") or ""),
                    location=str(item.get("location") or ""),
                    presence=_parse_presence(
                        item.get("workplace_type") or item.get("ai_work_arrangement")
                    ),
                    job_url=str(item.get("url") or item.get("job_url") or ""),
                )
            )
        return offers
