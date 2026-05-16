from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.product_scanner_service import (
    extract_barcode_from_image, lookup_product, generate_product_verdict
)

router = APIRouter(prefix="/product", tags=["Product Scanner"])

class ProductScanResponse(BaseModel):
    barcode: str
    product_name: str
    brand: str
    nutriscore: str
    nutriments: dict
    allergens: list
    verdict: dict
    ingredients_preview: str

@router.post("/scan", response_model=ProductScanResponse)
async def scan_product(
    file: UploadFile = File(...),
    child_age: int = Form(7),
    child_name: str = Form("your child"),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    image_bytes = await file.read()
    
    barcode = extract_barcode_from_image(image_bytes)
    if not barcode:
        raise HTTPException(status_code=422, detail="No barcode detected in image. Try photographing the barcode directly.")
    
    product = lookup_product(barcode)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with barcode {barcode} not found in Open Food Facts database.")
    
    verdict = generate_product_verdict(product, child_age, child_name)
    
    return ProductScanResponse(
        barcode=barcode,
        product_name=product["name"],
        brand=product["brand"],
        nutriscore=product["nutriscore"],
        nutriments=product["nutriments"],
        allergens=product["allergens"],
        verdict=verdict,
        ingredients_preview=product["ingredients"][:200] + "..." if len(product["ingredients"]) > 200 else product["ingredients"],
    )

@router.get("/lookup")
async def lookup_by_barcode(
    barcode: str = Query(..., description="EAN/UPC barcode number"),
    child_age: int = Query(7),
    child_name: str = Query("your child"),
):
    """Look up a product directly by barcode number — useful for testing."""
    product = lookup_product(barcode)
    if not product:
        raise HTTPException(status_code=404, detail=f"Barcode {barcode} not found.")
    verdict = generate_product_verdict(product, child_age, child_name)
    return {**product, "verdict": verdict}
