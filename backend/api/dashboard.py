from fastapi import APIRouter, HTTPException
import random
from typing import List, Dict, Any
from db.supabase import supabase
from datetime import datetime

router = APIRouter()

@router.get("/water-quality")
def get_water_quality():
    """
    Fetches the latest water quality reading from the database.
    Falls back to simulated data if no readings exist.
    """
    try:
        # Get the most recent reading
        result = supabase.table("water_quality_readings").select("*").order("recorded_at", desc=True).limit(1).execute()
        
        if result.data and len(result.data) > 0:
            reading = result.data[0]
            return {
                "pH": float(reading["ph"]),
                "turbidity": float(reading["turbidity"]),
                "oxygen": float(reading["oxygen"]),
                "salinity": float(reading["salinity"]),
                "temperature": float(reading["temperature"])
            }
        else:
            # Fallback to simulated data if no readings exist
            return {
                "pH": round(random.uniform(6.5, 8.5), 1),
                "turbidity": round(random.uniform(0.5, 5.0), 1),
                "oxygen": round(random.uniform(5.0, 10.0), 1),
                "salinity": round(random.uniform(0.1, 1.0), 1),
                "temperature": round(random.uniform(20.0, 30.0), 1)
            }
    except Exception as e:
        print(f"Error fetching water quality: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/water-quality")
def add_water_quality_reading(
    ph: float,
    turbidity: float,
    oxygen: float,
    salinity: float,
    temperature: float,
    location: str = "Default Monitoring Station",
    latitude: float = None,
    longitude: float = None
):
    """
    Adds a new water quality reading to the database.
    Useful for simulating sensor data or manual entry.
    """
    try:
        result = supabase.table("water_quality_readings").insert({
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "ph": ph,
            "turbidity": turbidity,
            "oxygen": oxygen,
            "salinity": salinity,
            "temperature": temperature
        }).execute()
        
        return result.data[0] if result.data else {}
    except Exception as e:
        print(f"Error adding water quality reading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/water-quality-history")
def get_water_quality_history(limit: int = 20):
    """
    Fetches historical water quality readings for chart visualization.
    Returns the most recent readings ordered by time.
    """
    try:
        result = supabase.table("water_quality_readings").select("*").order("recorded_at", desc=True).limit(limit).execute()
        
        if result.data:
            # Reverse to get chronological order (oldest to newest)
            readings = list(reversed(result.data))
            
            # Transform to chart-friendly format
            chart_data = []
            for reading in readings:
                # Format timestamp for display
                timestamp = reading["recorded_at"]
                # Extract time portion (HH:MM)
                time_str = timestamp.split("T")[1][:5] if "T" in timestamp else timestamp[:5]
                
                chart_data.append({
                    "time": time_str,
                    "pH": float(reading["ph"]),
                    "oxygen": float(reading["oxygen"]),
                    "turbidity": float(reading["turbidity"]),
                    "temperature": float(reading["temperature"]),
                    "salinity": float(reading["salinity"])
                })
            
            return chart_data
        else:
            # Return empty array if no data
            return []
    except Exception as e:
        print(f"Error fetching water quality history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/marine-impact")
def get_marine_impact():
    """
    Returns marine impact metrics.
    Currently returns static data, but could be calculated from database in the future.
    """
    return [
        {"name": "Fish Population", "current": 75, "target": 90, "color": "#3b82f6"},
        {"name": "Coral Health", "current": 62, "target": 85, "color": "#10b981"},
        {"name": "Water Clarity", "current": 58, "target": 80, "color": "#06b6d4"},
        {"name": "Biodiversity", "current": 68, "target": 90, "color": "#8b5cf6"},
    ]

@router.get("/success-stories")
def get_success_stories():
    """
    Fetches all success stories from the database.
    """
    try:
        result = supabase.table("success_stories").select("*").order("created_at", desc=False).execute()
        
        if result.data:
            # Transform database format to frontend format
            stories = []
            for story in result.data:
                stories.append({
                    "id": story["id"],
                    "title": story["title"],
                    "location": story["location"],
                    "timeframe": story["timeframe"],
                    "description": story["description"],
                    "image": story["image_url"],
                    "status": story["status"],
                    "impact": {
                        "waterQualityImproved": story["water_quality_improved"],
                        "speciesRecovered": story["species_recovered"],
                        "livesImpacted": story["lives_impacted"],
                        "pollutionReduced": story["pollution_reduced"]
                    },
                    "challenges": story["challenges"],
                    "solutions": story["solutions"],
                    "results": story["results"],
                    "stakeholders": story["stakeholders"]
                })
            return stories
        else:
            return []
    except Exception as e:
        print(f"Error fetching success stories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_dashboard_stats():
    """
    Returns key dashboard statistics for pollution reporting app.
    """
    try:
        # Get total reports count
        reports_result = supabase.table("reports").select("id", count="exact").execute()
        total_reports = reports_result.count if reports_result.count else 0
        
        # Get resolved reports count
        resolved_result = supabase.table("reports").select("id", count="exact").eq("status", "resolved").execute()
        resolved_reports = resolved_result.count if resolved_result.count else 0
        
        # Get unique users count (approximate based on reports)
        users_result = supabase.table("reports").select("user_id").execute()
        unique_users = len(set([r["user_id"] for r in users_result.data])) if users_result.data else 0
        
        # Calculate average response time (mock for now)
        avg_response_time = "2.5 days"
        
        return {
            "total_reports": total_reports,
            "active_users": unique_users,
            "resolved_reports": resolved_reports,
            "avg_response_time": avg_response_time
        }
    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        # Return fallback data
        return {
            "total_reports": 0,
            "active_users": 0,
            "resolved_reports": 0,
            "avg_response_time": "N/A"
        }

@router.get("/reports/timeline")
def get_reports_timeline(days: int = 30):
    """
    Returns daily report counts for the last N days.
    """
    try:
        from datetime import datetime, timedelta
        
        # Get reports from last N days
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()
        
        reports_result = supabase.table("reports").select("created_at").gte("created_at", cutoff_str).execute()
        
        # Group by date
        date_counts = {}
        for report in reports_result.data:
            date_str = report["created_at"].split("T")[0]  # Get date part only
            date_counts[date_str] = date_counts.get(date_str, 0) + 1
        
        # Fill in missing dates with 0
        timeline = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            date_str = date.strftime("%Y-%m-%d")
            timeline.append({
                "date": date_str,
                "count": date_counts.get(date_str, 0)
            })
        
        return timeline
    except Exception as e:
        print(f"Error fetching reports timeline: {e}")
        return []

@router.get("/reports/by-type")
def get_reports_by_type():
    """
    Returns count of reports grouped by pollution type.
    """
    try:
        reports_result = supabase.table("reports").select("description").execute()
        
        # Extract pollution type from description (format: "Type at Location: Description")
        type_counts = {
            "Plastic Pollution": 0,
            "Oil Spill": 0,
            "Sewage Overflow": 0,
            "Industrial Discharge": 0,
            "Chemical Contamination": 0,
            "Agricultural Runoff": 0,
            "Other": 0
        }
        
        for report in reports_result.data:
            desc = report["description"]
            found = False
            for pollution_type in type_counts.keys():
                if pollution_type in desc:
                    type_counts[pollution_type] += 1
                    found = True
                    break
            if not found:
                type_counts["Other"] += 1
        
        # Convert to array format for charts
        return [{"name": k, "value": v} for k, v in type_counts.items() if v > 0]
    except Exception as e:
        print(f"Error fetching reports by type: {e}")
        return []

@router.get("/reports/by-status")
def get_reports_by_status():
    """
    Returns count of reports grouped by status.
    """
    try:
        reports_result = supabase.table("reports").select("status").execute()
        
        status_counts = {
            "pending": 0,
            "investigating": 0,
            "resolved": 0
        }
        
        for report in reports_result.data:
            status = report["status"].lower()
            if status in status_counts:
                status_counts[status] += 1
        
        # Convert to array format for charts
        return [
            {"status": "Pending", "count": status_counts["pending"]},
            {"status": "Investigating", "count": status_counts["investigating"]},
            {"status": "Resolved", "count": status_counts["resolved"]}
        ]
    except Exception as e:
        print(f"Error fetching reports by status: {e}")
        return []

@router.get("/reports/geographic-heatmap")
def get_geographic_heatmap():
    """
    Returns geographic distribution of pollution reports with severity levels.
    Groups reports by location and calculates severity based on report density.
    """
    try:
        reports_result = supabase.table("reports").select("*").execute()
        
        # Group reports by location
        location_data = {}
        for report in reports_result.data:
            location = report.get("location", "Unknown")
            lat = report.get("latitude")
            lng = report.get("longitude")
            
            if location not in location_data:
                location_data[location] = {
                    "location": location,
                    "lat": lat if lat else 0,
                    "lng": lng if lng else 0,
                    "reports": 0,
                    "severity": 0
                }
            
            location_data[location]["reports"] += 1
        
        # Calculate severity based on report count (normalize to 0-100 scale)
        max_reports = max([data["reports"] for data in location_data.values()]) if location_data else 1
        
        heatmap_data = []
        for data in location_data.values():
            # Severity calculation: more reports = higher severity
            severity = min(100, int((data["reports"] / max_reports) * 100))
            heatmap_data.append({
                "location": data["location"],
                "lat": data["lat"],
                "lng": data["lng"],
                "reports": data["reports"],
                "severity": severity
            })
        
        # Sort by severity (highest first)
        heatmap_data.sort(key=lambda x: x["severity"], reverse=True)
        
        return heatmap_data
    except Exception as e:
        print(f"Error fetching geographic heatmap: {e}")
        return []

@router.get("/reports/severity-distribution")
def get_severity_distribution():
    """
    Returns distribution of reports by severity level.
    Calculates severity based on pollution type and status.
    """
    try:
        reports_result = supabase.table("reports").select("description, status").execute()
        
        severity_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0
        }
        
        # Define severity mapping for pollution types
        critical_types = ["Oil Spill", "Chemical Contamination", "Industrial Discharge"]
        high_types = ["Sewage Overflow", "Plastic Pollution"]
        medium_types = ["Agricultural Runoff"]
        
        for report in reports_result.data:
            desc = report.get("description", "")
            status = report.get("status", "").lower()
            
            # Determine severity based on pollution type
            severity = "Low"
            for pollution_type in critical_types:
                if pollution_type in desc:
                    severity = "Critical"
                    break
            
            if severity == "Low":
                for pollution_type in high_types:
                    if pollution_type in desc:
                        severity = "High"
                        break
            
            if severity == "Low":
                for pollution_type in medium_types:
                    if pollution_type in desc:
                        severity = "Medium"
                        break
            
            # Increase severity if status is pending (unresolved)
            if status == "pending" and severity == "Low":
                severity = "Medium"
            
            severity_counts[severity] += 1
        
        # Convert to chart format
        return [
            {"name": "Critical", "value": severity_counts["Critical"], "fill": "#ef4444"},
            {"name": "High", "value": severity_counts["High"], "fill": "#f59e0b"},
            {"name": "Medium", "value": severity_counts["Medium"], "fill": "#eab308"},
            {"name": "Low", "value": severity_counts["Low"], "fill": "#10b981"}
        ]
    except Exception as e:
        print(f"Error fetching severity distribution: {e}")
        return []

@router.get("/reports/trend-comparison")
def get_trend_comparison(months: int = 6):
    """
    Returns trend data comparing reports, resolutions, and response times over months.
    """
    try:
        from datetime import datetime, timedelta
        
        # Get reports from last N months
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        cutoff_str = cutoff_date.isoformat()
        
        reports_result = supabase.table("reports").select("created_at, status").gte("created_at", cutoff_str).execute()
        
        # Group by month
        monthly_data = {}
        for report in reports_result.data:
            created_at = report["created_at"]
            # Extract year-month
            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            month_key = date_obj.strftime("%b")
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "month": month_key,
                    "reports": 0,
                    "resolved": 0,
                    "avgResponseTime": 2.5  # Mock for now
                }
            
            monthly_data[month_key]["reports"] += 1
            if report["status"].lower() == "resolved":
                monthly_data[month_key]["resolved"] += 1
        
        # Convert to array and sort by month
        trend_data = list(monthly_data.values())
        
        # Calculate average response time (mock calculation for now)
        for data in trend_data:
            if data["resolved"] > 0:
                data["avgResponseTime"] = round(3.0 - (data["resolved"] / data["reports"]) * 0.5, 1)
        
        return trend_data
    except Exception as e:
        print(f"Error fetching trend comparison: {e}")
        return []

@router.get("/marine-impact/metrics")
def get_marine_impact_metrics():
    """
    Returns marine impact metrics including species data and pollution sources.
    """
    try:
        # Get total pollution reports to calculate impact
        reports_result = supabase.table("reports").select("id", count="exact").execute()
        total_reports = reports_result.count if reports_result.count else 0
        
        # Calculate impact based on report volume (mock calculation)
        base_impact = min(100, total_reports * 2)
        
        return {
            "species_impact": [
                {
                    "species": "Marine Fish",
                    "currentPopulation": 2500000,
                    "projectedChange": -15,
                    "threats": ["Plastic Pollution", "Chemical Runoff", "Temperature Rise"],
                    "conservationStatus": "Vulnerable"
                },
                {
                    "species": "Coral Reefs",
                    "currentPopulation": 850,
                    "projectedChange": -23,
                    "threats": ["Ocean Acidification", "Pollution", "Warming Waters"],
                    "conservationStatus": "Critical"
                },
                {
                    "species": "Sea Turtles",
                    "currentPopulation": 45000,
                    "projectedChange": -8,
                    "threats": ["Plastic Ingestion", "Nesting Site Loss", "Fishing Nets"],
                    "conservationStatus": "Endangered"
                },
                {
                    "species": "Dolphins & Whales",
                    "currentPopulation": 12000,
                    "projectedChange": 3,
                    "threats": ["Noise Pollution", "Ship Strikes", "Chemical Toxins"],
                    "conservationStatus": "Stable"
                }
            ],
            "pollution_sources": [
                {"source": "Industrial Discharge", "impact": 35, "trend": "Increasing"},
                {"source": "Plastic Waste", "impact": 28, "trend": "Stable"},
                {"source": "Agricultural Runoff", "impact": 22, "trend": "Decreasing"},
                {"source": "Urban Sewage", "impact": 15, "trend": "Increasing"}
            ],
            "ecosystem_health": {
                "water_quality": 82,
                "biodiversity": 75,
                "pollution_level": 68,
                "conservation_effort": 91
            },
            "ai_predictions": [
                {
                    "timeframe": "Next 5 Years",
                    "prediction": "Moderate decline in marine biodiversity if current pollution trends continue",
                    "confidence": 87,
                    "severity": "High"
                },
                {
                    "timeframe": "Next 10 Years",
                    "prediction": "Critical threshold for coral reef ecosystems without intervention",
                    "confidence": 92,
                    "severity": "Critical"
                },
                {
                    "timeframe": "Next 20 Years",
                    "prediction": "Potential for significant recovery with aggressive conservation efforts",
                    "confidence": 76,
                    "severity": "Moderate"
                }
            ]
        }
    except Exception as e:
        print(f"Error fetching marine impact metrics: {e}")
        return {}

