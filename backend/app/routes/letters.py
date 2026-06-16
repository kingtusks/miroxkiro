from fastapi import APIRouter
from app.services.agent import generate_demand_letter
from app.models import DemandLetterRequest, DemandLetterResponse

router = APIRouter()


@router.post("/generate", response_model=DemandLetterResponse)
async def create_demand_letter(request: DemandLetterRequest):
    """
    Generate a formal demand letter citing lease violations.
    """
    letter = await generate_demand_letter(
        tenant_name=request.tenant_name,
        landlord_name=request.landlord_name,
        address=request.address,
        violations=request.violations,
    )
    return DemandLetterResponse(letter=letter)
