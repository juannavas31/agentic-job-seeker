from __future__ import annotations

import math
import os
from typing import Any

import httpx
from dotenv import load_dotenv

from app.services.portal.linkedin import JobOffer, Presence

# Base64-encoded Glassdoor location id for Madrid: {"t":"S","id":6789,"n":"Madrid"}
DEFAULT_LOCATION_ID = "eyJ0IjoiUyIsImlkIjo2Nzg5LCJuIjoiTWFkcmlkIn0="

# Bound pagination to protect the RapidAPI monthly request quota.
_MAX_PAGES = 3


def _time_frame_to_days(time_frame: str) -> int:
    """Convert "xxH" (hours) or "xxD" (days) into a number of days for datePosted."""
    value = str(time_frame or "").strip().lower()
    try:
        if value.endswith("h"):
            return max(1, math.ceil(int(value[:-1]) / 24))
        if value.endswith("d"):
            return max(1, int(value[:-1]))
    except ValueError:
        pass
    return 1


def _next_cursor(data: dict[str, Any]) -> str | None:
    cursors = data.get("paginationCursors") or []
    for entry in cursors:
        if isinstance(entry, dict) and entry.get("cursor"):
            return str(entry["cursor"])
    return None


def _to_offer(item: dict[str, Any], role: str, location: str) -> JobOffer:
    if item.get("is_remote") is True or str(item.get("is_remote", "")).lower() == "true":
        presence = Presence.REMOTE
    else:
        normalized = str(item.get("workplace_type") or item.get("job_workplace") or "").lower()
        if "remote" in normalized:
            presence = Presence.REMOTE
        elif "hybrid" in normalized:
            presence = Presence.HYBRID
        else:
            presence = Presence.ON_SITE

    return JobOffer(
        company=str(item.get("employer_name") or item.get("company") or item.get("organization") or ""),
        published_date=str(
            item.get("post_date")
            or item.get("posted_at")
            or item.get("date_posted")
            or item.get("listed_date")
            or ""
        ),
        role=str(item.get("job_title") or item.get("title") or role),
        description=str(item.get("job_description") or item.get("description") or ""),
        location=str(item.get("location") or location),
        presence=presence,
        job_url=str(item.get("job_url") or item.get("url") or item.get("job_link") or ""),
    )


class Glassdoor_Jobs:
    """Adapter for fetching Glassdoor job offers via RapidAPI."""

    def __init__(self) -> None:
        load_dotenv()
        self.rapidAPI_url = os.getenv("RapidAPI_glassdoor_url", "")
        self.rapidAPI_glassdoor_host = os.getenv("RapidAPI_glassdoor_host", "")
        self.rapidAPI_key = os.getenv("X-RapidAPI-Key", "")

    async def get_jobs(
        self,
        role: str,
        time_frame: str = "24h",
        location: str = "Madrid, Spain",
        remoteOnly: bool | str = "false",
    ) -> list[JobOffer]:
        from app.main import app  # deferred import: reuse the singleton httpx client

        client: httpx.AsyncClient = app.state.httpx_client
        headers = {
            "x-rapidapi-key": self.rapidAPI_key,
            "x-rapidapi-host": self.rapidAPI_glassdoor_host,
        }
        remote_flag = remoteOnly if isinstance(remoteOnly, str) else str(remoteOnly).lower()
        params: dict[str, Any] = {
            "query": role,
            "locationId": DEFAULT_LOCATION_ID,
            "datePosted": _time_frame_to_days(time_frame),
            "remoteOnly": remote_flag,
        }

        offers: list[JobOffer] = []
        cursor: str | None = None
        for _ in range(_MAX_PAGES):
            page_params = dict(params)
            if cursor:
                page_params["pageCursor"] = cursor

            response = await client.get(self.rapidAPI_url, headers=headers, params=page_params)
            response.raise_for_status()
            payload = response.json()

            data = payload.get("data") if isinstance(payload, dict) else None
            if isinstance(data, dict):
                items = data.get("jobs") or data.get("results") or []
            elif isinstance(payload, list):
                items = payload
            else:
                items = []

            offers.extend(_to_offer(item, role, location) for item in items if isinstance(item, dict))

            cursor = _next_cursor(data) if isinstance(data, dict) else None
            if not cursor:
                break

        return offers
