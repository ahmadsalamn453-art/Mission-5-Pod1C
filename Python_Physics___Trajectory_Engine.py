import numpy as np

class ParachuteDriftCalculator:
    """
    Parachute Wind Drift and Landing Zone Radius Calculator
    Mission 05 (SEDS-TASK-RCK-SRILANKA-020) - Ahmad Salman
    """
    def __init__(self, safe_radius_m=400.0, baseline_descent_ms=5.2):
        self.safe_radius_m = safe_radius_m
        self.baseline_descent_ms = baseline_descent_ms

    def calculate_descent(self, deployment_alt_m, ground_elevation_m, wind_speed_ms, wind_dir_deg):
        # Effective altitude
        effective_alt_m = max(deployment_alt_m - ground_elevation_m, 1.0)
        
        # Fall duration calculation (seconds)
        fall_duration_s = effective_alt_m / self.baseline_descent_ms
        
        # Meteorological bearing to vector angle conversion
        drift_rad = np.radians((wind_dir_deg + 180) % 360)
        
        # Drift distance magnitude
        total_drift_m = wind_speed_ms * fall_duration_s
        
        # Target Cartesian offset coordinates relative to Launch Pad Origin (0,0)
        target_x = total_drift_m * np.sin(drift_rad)
        target_y = -total_drift_m * np.cos(drift_rad)
        
        # Validate against 400m launch pad radius limit
        is_compliant = total_drift_m <= self.safe_radius_m
        
        # Compass directional heading string
        dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        compass_text = dirs[int(round(wind_dir_deg / 45.0)) % 8]
        
        return {
            "effective_alt_m": effective_alt_m,
            "fall_duration_s": fall_duration_s,
            "total_drift_m": total_drift_m,
            "target_x": target_x,
            "target_y": target_y,
            "landing_bearing": f"{wind_dir_deg}° {compass_text}",
            "is_compliant": is_compliant,
            "safe_radius_m": self.safe_radius_m
        }

if __name__ == "__main__":
    calc = ParachuteDriftCalculator()
    
    # Test Scenario: 350m Deployment Alt, 5.0 m/s Wind @ 135 deg
    result = calc.calculate_descent(
        deployment_alt_m=350,
        ground_elevation_m=0,
        wind_speed_ms=5.0,
        wind_dir_deg=135
    )
    
    print("=" * 60)
    print("SEDS MISSION 05: PARACHUTE DRIFT & LZ RADIUS SUMMARY")
    print(f"Candidate: Ahmad Salman")
    print("=" * 60)
    print(f"Fall Duration     : {int(result['fall_duration_s'] // 60)}m {int(result['fall_duration_s'] % 60)}s")
    print(f"Total Drift       : {result['total_drift_m']:.2f} m")
    print(f"Landing Bearing   : {result['landing_bearing']}")
    print(f"Target Offset (X,Y): ({result['target_x']:.2f}m, {result['target_y']:.2f}m)")
    print(f"400m Radius Compliance: {'PASSED' if result['is_compliant'] else 'FAILED'}")
    print("=" * 60)