import numpy as np

def calculate_dialysis_metrics(pre_urea, post_urea, weight_loss, post_weight, hours):
    """
    Core engine: Calculates URR and Kt/V using vectorized NumPy operations.
    """
    # 1. Calculate URR (Urea Reduction Ratio)
    urr = ((pre_urea - post_urea) / pre_urea) * 100
    
    # 2. Calculate Kt/V (Daugirdas Formula)
    # R is the ratio of post-to-pre urea
    R = post_urea / pre_urea
    # Natural log of (R - correction for urea generation during treatment)
    term1 = -np.log(R - (0.008 * hours))
    # Adjustment for fluid removal (weight loss)
    term2 = (4 - 3.5 * R) * (weight_loss / post_weight)
    
    ktv = term1 + term2
    return urr, ktv

def analyze_patient_history(history):
    """
    Processes the records and generates a medical report with alerts.
    """
    # Extract data from the structured array
    dates = history['date']
    urr, ktv = calculate_dialysis_metrics(
        history['pre_urea'], 
        history['post_urea'], 
        history['weight_loss'], 
        history['post_weight'], 
        history['duration']
    )
    
    print(f"\n{'DATE':<12} | {'URR %':<8} | {'Kt/V':<8} | {'STATUS'}")
    print("-" * 55)
    
    for i in range(len(history)):
        # Clinical Thresholds: URR > 65% and Kt/V > 1.2
        is_adequate = urr[i] >= 65 and ktv[i] >= 1.2
        status = "OPTIMAL" if is_adequate else "SUB-OPTIMAL"
        
        print(f"{dates[i]:<12} | {urr[i]:>7.1f}% | {ktv[i]:>8.2f} | {status}")

    # --- ADD-ON: CLINICAL TREND ALERTS ---
    print("\n" + "="*20 + " CLINICAL ALERTS " + "="*20)
    
    # Check for declining efficiency (The "Access Failure" Warning)
    if len(ktv) >= 3:
        # Check if the last three sessions are strictly decreasing
        if ktv[-1] < ktv[-2] < ktv[-3]:
            print("![!] ALERT: Steady decline in Kt/V detected over last 3 sessions.")
            print("    Action: Inspect vascular access for possible stenosis/clotting.")
            
    # Check for excessive fluid weight (The "Heart Strain" Warning)
    # If weight loss required is > 5% of body weight, it's risky
    fluid_ratio = history['weight_loss'] / history['post_weight']
    if np.any(fluid_ratio > 0.05):
        high_fluid_dates = dates[fluid_ratio > 0.05]
        print(f"![!] WARNING: Excessive fluid removal (>5%) on: {', '.join(high_fluid_dates)}")
        print("    Action: Review patient's salt/fluid intake between sessions.")

# --- MAIN DATA SETUP ---

# Define the data structure (Schema)
# 'U10' = String, 'f4' = 32-bit float
dtype = [('date', 'U10'), ('pre_urea', 'f4'), ('post_urea', 'f4'), 
         ('weight_loss', 'f4'), ('post_weight', 'f4'), ('duration', 'f4')]

# Simulated track records for a patient
patient_records = np.array([
    ('2026-03-01', 110.0, 32.0, 2.5, 70.0, 4.0),
    ('2026-03-03', 108.0, 35.0, 2.0, 70.5, 4.0),
    ('2026-03-05', 115.0, 42.0, 4.5, 71.0, 3.5), # High fluid & low duration
    ('2026-03-08', 112.0, 44.0, 2.2, 70.8, 4.0), # Declining Kt/V session 1
    ('2026-03-10', 105.0, 48.0, 2.0, 71.2, 4.0), # Declining Kt/V session 2
], dtype=dtype)

analyze_patient_history(patient_records)
