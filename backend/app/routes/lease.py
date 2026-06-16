from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import extract_text_from_pdf
from app.services.agent import analyze_lease
from app.models import LeaseAnalysisResponse

router = APIRouter()


@router.post("/analyze", response_model=LeaseAnalysisResponse)
async def analyze_lease_upload(file: UploadFile = File(...)):
    """
    Upload a lease PDF and get an AI-powered violation analysis.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large. Max 10MB.")

    # Extract text from PDF
    lease_text = extract_text_from_pdf(contents)
    if not lease_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from PDF. The file may be scanned/image-based.",
        )

    # Run AI analysis
    result = await analyze_lease(lease_text)
    return LeaseAnalysisResponse(**result)


@router.post("/analyze-text", response_model=LeaseAnalysisResponse)
async def analyze_lease_text(body: dict):
    """
    Submit raw lease text for analysis (useful for testing without PDF).
    """
    lease_text = body.get("text", "")
    if not lease_text.strip():
        raise HTTPException(status_code=400, detail="No lease text provided.")

    result = await analyze_lease(lease_text)
    return LeaseAnalysisResponse(**result)
