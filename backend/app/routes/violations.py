from fastapi import APIRouter, HTTPException
from app.services.hpd_client import get_hpd_violations
from app.models import HPDViolationQuery

router = APIRouter()


@router.post("/hpd")
async def lookup_hpd_violations(query: HPDViolationQuery):
    """
    Look up HPD violations for a property from NYC Open Data.
    """
    try:
        violations = await get_hpd_violations(
            borough=query.borough,
            address=query.address,
            block=query.block,
            lot=query.lot,
        )
        return {
            "count": len(violations),
            "violations": violations,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error querying NYC Open Data: {str(e)}")
