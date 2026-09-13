# -*- coding: utf-8 -*-
"""
Debug toggles API — currently just FIX-seed mode (see debug_state.py).

Process-global, resets to OFF on restart by design. The UI toggle on the
main toolbar (next to Voice ON/OFF) is the single control; GET is used by
the frontend on load to sync its button to whatever the backend actually
has (so a backend restart correctly shows the toggle as off again).
"""

from fastapi import APIRouter
from pydantic import BaseModel

import debug_state

router = APIRouter(prefix="/api/debug", tags=["debug"])


class FixSeedRequest(BaseModel):
    enabled: bool
    value: int = 43


@router.get("/fix-seed")
async def get_fix_seed():
    return debug_state.fix_seed_state()


@router.post("/fix-seed")
async def set_fix_seed(req: FixSeedRequest):
    debug_state.set_fix_seed(req.enabled, req.value)
    return debug_state.fix_seed_state()
