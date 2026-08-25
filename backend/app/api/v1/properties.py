from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from app.core.auth import authenticate_request as get_current_user
from app.core.database_pool import db_pool

router = APIRouter()


@router.get("")
async def get_properties(
    page: int = Query(1, ge=1),
    page_size: int = Query(1000, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    tenant_id = getattr(current_user, "tenant_id", None)
    if not tenant_id:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

    start = (page - 1) * page_size
    end = start + page_size - 1
    if not db_pool.session_factory:
        await db_pool.initialize()

    async with await db_pool.get_session() as session:
        from sqlalchemy import text

        result = await session.execute(
            text("""
                SELECT id, tenant_id, name, timezone
                FROM properties
                WHERE tenant_id = :tenant_id
                ORDER BY name
                LIMIT :page_size OFFSET :offset
            """),
            {"tenant_id": tenant_id, "page_size": page_size, "offset": start},
        )
        items = [dict(row) for row in result.mappings().all()]

    return {
        "items": items,
        "total": len(items),
        "page": page,
        "page_size": page_size,
    }
