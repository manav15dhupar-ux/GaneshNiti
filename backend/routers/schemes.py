"""
routers/schemes.py — the GET /schemes endpoint.

WHAT THIS DOES:
When someone visits /schemes, this returns the full list of verified
government schemes (from Firestore if it's set up, otherwise from the
local backup file so the app never breaks).
"""

from fastapi import APIRouter
from services.firestore_client import get_all_schemes, get_all_channel_partners, is_using_live_firestore

router = APIRouter()


@router.get("/schemes")
def list_schemes():
    """Returns every verified scheme."""
    schemes = get_all_schemes()
    return {
        "count": len(schemes),
        "source": "firestore" if is_using_live_firestore() else "local_fallback",
        "schemes": schemes,
    }


@router.get("/channel-partners")
def list_channel_partners():
    """Returns every (simulated) channel partner."""
    partners = get_all_channel_partners()
    return {
        "count": len(partners),
        "source": "firestore" if is_using_live_firestore() else "local_fallback",
        "note": "All channel partner data is simulated for this prototype.",
        "partners": partners,
    }