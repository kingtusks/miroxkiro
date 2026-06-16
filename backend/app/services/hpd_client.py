import httpx
from typing import Optional

NYC_OPEN_DATA_HPD_URL = "https://data.cityofnewyork.us/resource/wvxf-dwi5.json"


async def get_hpd_violations(
    borough: str,
    block: Optional[str] = None,
    lot: Optional[str] = None,
    address: Optional[str] = None,
    limit: int = 50,
) -> list[dict]:
    """
    Query the NYC HPD Violations database via NYC Open Data API.
    Can search by borough + block/lot or by address.
    """
    params: dict = {"$limit": str(limit), "$order": "inspectiondate DESC"}

    if borough:
        # HPD uses uppercase borough names
        params["boroid"] = _borough_to_id(borough)

    if block:
        params["block"] = block
    if lot:
        params["lot"] = lot

    if address:
        params["$where"] = f"upper(streetaddress) like upper('%{address}%')"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(NYC_OPEN_DATA_HPD_URL, params=params)
        resp.raise_for_status()
        return resp.json()


def _borough_to_id(borough: str) -> str:
    mapping = {
        "manhattan": "1",
        "bronx": "2",
        "brooklyn": "3",
        "queens": "4",
        "staten island": "5",
    }
    return mapping.get(borough.lower(), "1")
