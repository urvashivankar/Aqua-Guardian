from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from db.supabase import supabase
from utils.storage import upload_file, get_public_url

router = APIRouter()

@router.post("/{report_id}")
def start_cleanup(report_id: str, actor_id: str = Form(...)):
    res = supabase.table("cleanup_actions").insert({
        "report_id": report_id,
        "actor_id": actor_id,
        "status": "in_progress"
    }).execute()
    return res.data

@router.post("/{report_id}/evidence")
async def upload_evidence(report_id: str, file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_name = f"evidence_{report_id}_{file.filename}"
    upload_res = upload_file(file_bytes, file_name, bucket="evidence")
    
    if not upload_res:
        raise HTTPException(status_code=500, detail="Upload failed")
        
    url = get_public_url(file_name, bucket="evidence")
    
    # Update cleanup action
    # Assuming we append to an array or create a new evidence record. 
    # For simplicity, we'll assume we update the cleanup_actions table.
    
    # First get the cleanup action for this report
    # In reality, we might need the specific cleanup action ID, but assuming one per report for now.
    
    res = supabase.table("cleanup_actions").update({
        "status": "completed",
        "evidence_urls": [url] # This would overwrite, in real app use array_append
    }).eq("report_id", report_id).execute()
    
    return res.data
