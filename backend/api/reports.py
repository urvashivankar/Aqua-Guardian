from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Form
from typing import List, Optional

from db.supabase import supabase
from db.models import Report, ReportCreate
from ml.infer import predict_image
from blockchain.write_hash import generate_hash, write_hash_to_chain
from utils.storage import upload_file, get_public_url
from utils.notify import notify_authorities

router = APIRouter()

@router.post("/", response_model=Report)
async def create_report(
    background_tasks: BackgroundTasks,
    user_id: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: str = Form(...),
    severity: int = Form(...),
    file: UploadFile = File(...)
) -> Report:
    """Create a new pollution report.

    Handles mandatory image upload, AI inference, stores the report in Supabase,
    and logs the report hash to the blockchain as a background task.
    """
    # 1. Process image upload and AI inference
    photo_url: Optional[str] = None
    ai_result = {"class": None, "confidence": 0.0}
    
    file_bytes = await file.read()
    # Use the user ID from the report for a unique filename
    file_name = f"{user_id}_{file.filename}"
    if upload_file(file_bytes, file_name):
        photo_url = get_public_url(file_name)
    
    try:
        ai_result = predict_image(file_bytes)
    except Exception as e:
        print(f"AI Inference failed: {e}")

    # 2. Build the report payload for Supabase
    report_payload = {
        "user_id": user_id,
        "latitude": latitude,
        "longitude": longitude,
        "description": description,
        "severity": severity,
        "ai_class": ai_result["class"],
        "ai_confidence": ai_result["confidence"],
        # "photo_url": photo_url,  # Removed: Column missing in DB and migration failed
        "status": "pending",
    }

    # 3. Insert the report into Supabase
    try:
        res = supabase.table("reports").insert(report_payload).execute()
        if not res.data:
            raise HTTPException(status_code=500, detail="Database insert failed")
        new_report = res.data[0]
        
        # Insert photo reference to photos table
        if photo_url:
            supabase.table("photos").insert({"report_id": new_report["id"], "url": photo_url}).execute()
            # Manually add photo_url to the response object since it's not in the reports table
            new_report["photo_url"] = photo_url
            
        # 4. Log to blockchain asynchronously
        background_tasks.add_task(log_report_to_blockchain, new_report)
        
        # 5. Notify authorities if high-confidence pollution detected
        if ai_result["confidence"] >= 0.90:
            background_tasks.add_task(notify_authorities, new_report)
        
        return new_report
    except Exception as e:
        print(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def log_report_to_blockchain(report_data: dict) -> None:
    """Generate a hash of the report and write it to the blockchain.

    Runs as a background task to avoid blocking the API response.
    """
    try:
        report_hash = generate_hash(report_data)
        tx_hash = write_hash_to_chain(report_hash)
        if tx_hash and tx_hash.startswith("0x"):
            supabase.table("blockchain_logs").insert({"report_id": report_data["id"], "tx_hash": tx_hash}).execute()
    except Exception as bc_e:
        print(f"Blockchain logging failed (background): {bc_e}")

@router.get("/", response_model=List[Report])
def get_reports() -> List[Report]:
    """Retrieve all reports."""
    res = supabase.table("reports").select("*").execute()
    return res.data

@router.get("/{report_id}", response_model=Report)
def get_report(report_id: str) -> Report:
    """Retrieve a single report by its ID."""
    res = supabase.table("reports").select("*").eq("id", report_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Report not found")
    return res.data[0]

@router.post("/{report_id}/verify")
def verify_report(report_id: str) -> List[dict]:
    """Mark a report as verified (admin/NGO action)."""
    res = supabase.table("reports").update({"status": "verified"}).eq("id", report_id).execute()
    return res.data
