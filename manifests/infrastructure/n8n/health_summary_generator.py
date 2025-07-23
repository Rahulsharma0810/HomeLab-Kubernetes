# manifests/infrastructure/n8n/health_summary_generator.py
import json
import pandas as pd
from datetime import datetime

def safe_get(d, path, default=None):
    keys = path.split(".")
    for key in keys:
        if isinstance(d, list):
            return len(d)
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def WorkOut_Stairs(w):
    # Step count
    steps = w.get("stepCount", [])
    total_steps = sum(s.get("qty", 0) for s in steps)
    step_count_points = len(steps)
    duration_min = w.get("duration", 0) / 60
    avg_step_cadence = round(total_steps / duration_min, 2) if duration_min > 0 else 0

    # Heart rate data
    hr_data = w.get("heartRateData", [])
    hr_points = len(hr_data)
    avg_hr = round(sum(d.get("Avg", 0) for d in hr_data) / hr_points, 2) if hr_points > 0 else None
    min_hr = min((d.get("Min", float('inf')) for d in hr_data), default=None)
    max_hr = max((d.get("Max", float('-inf')) for d in hr_data), default=None)

    # Heart rate recovery
    hr_recovery = w.get("heartRateRecovery", [])
    hr_recovery_points = len(hr_recovery)
    if hr_recovery_points > 1:
        start_hr = hr_recovery[0].get("Avg", 0)
        end_hr = hr_recovery[-1].get("Avg", 0)
        drop_hr = start_hr - end_hr
        start_time = datetime.strptime(hr_recovery[0]["date"], "%Y-%m-%d %H:%M:%S %z")
        end_time = datetime.strptime(hr_recovery[-1]["date"], "%Y-%m-%d %H:%M:%S %z")
        recovery_duration = (end_time - start_time).total_seconds() / 60
    else:
        start_hr = end_hr = drop_hr = recovery_duration = None

    return {
        "Name": w.get("name"),
        "Start": w.get("start"),
        "Avg HR (bpm)": avg_hr,
        "Min HR": min_hr,
        "Max HR": max_hr,
        "Duration (min)": round(duration_min, 2),
        "Energy (kJ)": round(safe_get(w, "activeEnergyBurned.qty", 0), 2),
        "Temp (°C)": round(safe_get(w, "temperature.qty", 0), 2),
        "Humidity (%)": safe_get(w, "humidity.qty", 0),
        "Intensity": round(safe_get(w, "intensity.qty", 0), 2),
        "Total Steps": round(total_steps, 2),
        "Step Point": step_count_points,
        "Avg Step Cadence": avg_step_cadence,
        "HR Data Points": hr_points,
        "Recovery Start HR": start_hr,
        "Recovery End HR": end_hr,
        "Recovery Drop": round(drop_hr, 2) if drop_hr is not None else None,
        "Recovery Duration": round(recovery_duration, 2) if recovery_duration is not None else None,
        "Recovery Data Points": hr_recovery_points
    }

def summarize_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        workouts = data['data']['workouts']
        summary = [WorkOut_Stairs(w) for w in workouts]
        df = pd.DataFrame(summary)
        return df

# Example usage:
# df_summary = summarize_json('HealthAutoExport-2025-07-22 2.json')
# df_summary.to_csv("Workout_Summary.csv", index=False)
