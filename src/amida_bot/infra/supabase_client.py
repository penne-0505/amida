from __future__ import annotations

from supabase import Client, create_client


def create_supabase_client(url: str, service_role_key: str) -> Client:
    return create_client(url, service_role_key)
