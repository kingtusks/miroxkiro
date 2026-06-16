import anthropic
from app.config import CLAUDE_API_KEY

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

SYSTEM_PROMPT = """You are RentGhost, an expert AI tenant rights advocate specializing in New York City rent stabilization law.

Your knowledge covers:
- NYC Rent Stabilization Code (RSC)
- NYC Admin Code (Housing Maintenance Code)
- Real Property Law (RPL)
- NYC Housing Preservation & Development (HPD) regulations
- DHCR (Division of Housing and Community Renewal) rules
- Lead paint disclosure requirements (Local Law 1)
- Rent overcharge rules and legal regulated rent calculations
- Lease renewal rights, succession rights, preferential rent rules
- Required lease rider disclosures

When analyzing a lease, you should:
1. Extract key terms: rent amount, lease dates, apartment address, tenant/landlord names, any riders.
2. Identify potential violations by cross-referencing NYC rent stabilization laws.
3. Flag missing required disclosures (rent stabilization rider, lead paint notice, sprinkler disclosure, etc.)
4. Check for illegal clauses (waiver of rights, illegal fees, etc.)
5. Note if rent increases exceed legal guidelines.

Always cite specific NYC Admin Code sections, RSC sections, or RPL sections when identifying violations.
Be thorough but clear — the tenant may not have legal training."""


async def analyze_lease(lease_text: str) -> dict:
    """
    Send lease text to Claude for analysis.
    Returns structured violation findings.
    """
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following NYC lease document. 

Respond in this JSON structure:
{{
    "extracted_terms": {{
        "address": "...",
        "borough": "...",
        "tenant_name": "...",
        "landlord_name": "...",
        "rent_amount": "...",
        "lease_start": "...",
        "lease_end": "...",
        "apartment_type": "rent-stabilized | market-rate | unknown",
        "other_terms": []
    }},
    "violations": [
        {{
            "title": "Short description",
            "severity": "high | medium | low",
            "description": "Detailed explanation of the violation",
            "legal_citation": "Specific law/code section",
            "tenant_action": "What the tenant can do about it"
        }}
    ],
    "missing_disclosures": [
        {{
            "disclosure": "Name of required disclosure",
            "legal_requirement": "Law requiring it",
            "consequence": "What this means for the tenant"
        }}
    ],
    "summary": "Brief overall assessment"
}}

LEASE DOCUMENT:
{lease_text}""",
            }
        ],
    )
    
    # Extract the text response
    response_text = message.content[0].text
    
    # Try to parse as JSON, fall back to raw text
    import json
    try:
        # Handle case where Claude wraps JSON in markdown code blocks
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw_analysis": response_text}


async def generate_demand_letter(
    tenant_name: str,
    landlord_name: str,
    address: str,
    violations: list[dict],
) -> str:
    """
    Generate a formal demand letter citing specific violations.
    """
    violations_text = "\n".join(
        f"- {v['title']}: {v['description']} (Citation: {v['legal_citation']})"
        for v in violations
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system="""You are RentGhost, drafting formal tenant demand letters. 
Write professional, legally-grounded demand letters that cite specific NYC laws.
The tone should be firm but professional. Include:
- Proper formatting with date, addresses
- Clear statement of violations with legal citations
- Specific demands (cure violations, refund overcharges, etc.)
- Deadline for response (typically 30 days)
- Statement that failure to comply may result in filing with DHCR or court action
- Signature line for tenant""",
        messages=[
            {
                "role": "user",
                "content": f"""Draft a demand letter with these details:

Tenant: {tenant_name}
Landlord: {landlord_name}
Property Address: {address}

Violations found:
{violations_text}

Generate a complete, ready-to-send demand letter.""",
            }
        ],
    )

    return message.content[0].text
