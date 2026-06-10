import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyFitSystem:
    def __init__(self):
        # 1. Inputs (Antecedents) and Outputs (Consequents)
        self.sleep = ctrl.Antecedent(np.arange(0, 11, 1), 'Sleep Quality')
        self.soreness = ctrl.Antecedent(np.arange(0, 11, 1), 'Muscle Soreness')
        self.energy = ctrl.Antecedent(np.arange(0, 11, 1), 'Energy Level')
        self.stress = ctrl.Antecedent(np.arange(0, 11, 1), 'Stress Level')
        
        self.intensity = ctrl.Consequent(np.arange(0, 101, 1), 'Workout Intensity (%)')
        self.volume = ctrl.Consequent(np.arange(0, 121, 1), 'Workout Volume (Min)')
        
        # 2. Membership Functions
        
        # Sleep Quality [0-10]
        self.sleep['Poor'] = fuzz.trapmf(self.sleep.universe, [0, 0, 3, 5])
        self.sleep['Average'] = fuzz.trimf(self.sleep.universe, [4, 6, 8])
        self.sleep['Good'] = fuzz.trapmf(self.sleep.universe, [7, 9, 10, 10])
        
        # Muscle Soreness [0-10]
        self.soreness['Low'] = fuzz.trapmf(self.soreness.universe, [0, 0, 2, 4])
        self.soreness['Moderate'] = fuzz.trimf(self.soreness.universe, [3, 5, 7])
        self.soreness['High'] = fuzz.trapmf(self.soreness.universe, [6, 8, 10, 10])
        
        # Energy Level [0-10]
        self.energy['Deficit'] = fuzz.trapmf(self.energy.universe, [0, 0, 3, 5])
        self.energy['Balanced'] = fuzz.trimf(self.energy.universe, [4, 6, 8])
        self.energy['Surplus'] = fuzz.trapmf(self.energy.universe, [7, 9, 10, 10])
        
        # Stress Level [0-10]
        self.stress['Low'] = fuzz.trapmf(self.stress.universe, [0, 0, 2, 4])
        self.stress['Normal'] = fuzz.trimf(self.stress.universe, [3, 5, 7])
        self.stress['High'] = fuzz.trapmf(self.stress.universe, [6, 8, 10, 10])
        
        # OUTPUTS
        # Workout Intensity (%) [0-100]
        self.intensity['Very Light'] = fuzz.trapmf(self.intensity.universe, [0, 0, 20, 40])
        self.intensity['Light'] = fuzz.trimf(self.intensity.universe, [20, 40, 60])
        self.intensity['Moderate'] = fuzz.trimf(self.intensity.universe, [40, 60, 80])
        self.intensity['High'] = fuzz.trimf(self.intensity.universe, [60, 80, 100])
        self.intensity['Maximum'] = fuzz.trapmf(self.intensity.universe, [80, 95, 100, 100])
        
        # Workout Volume (Min) [0-120]
        self.volume['Low'] = fuzz.trapmf(self.volume.universe, [0, 0, 30, 60])
        self.volume['Medium'] = fuzz.trimf(self.volume.universe, [40, 60, 80])
        self.volume['High'] = fuzz.trapmf(self.volume.universe, [60, 90, 120, 120])
        
        # 3. Fuzzy Rules
        rules = []
        
        # Extreme negative conditions
        rules.append(ctrl.Rule(self.sleep['Poor'] | self.soreness['High'] | self.stress['High'], 
                          (self.intensity['Very Light'], self.volume['Low'])))
        rules.append(ctrl.Rule(self.energy['Deficit'] & self.soreness['High'], 
                          (self.intensity['Very Light'], self.volume['Low'])))
        
        # Perfect conditions
        rules.append(ctrl.Rule(self.sleep['Good'] & self.soreness['Low'] & self.energy['Surplus'] & self.stress['Low'],
                          (self.intensity['Maximum'], self.volume['High'])))
        rules.append(ctrl.Rule(self.sleep['Good'] & self.soreness['Low'] & self.energy['Balanced'] & self.stress['Normal'],
                          (self.intensity['High'], self.volume['High'])))
                          
        # Standard / Average conditions
        rules.append(ctrl.Rule(self.sleep['Average'] & self.soreness['Moderate'] & self.energy['Balanced'],
                          (self.intensity['Moderate'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.sleep['Average'] & self.soreness['Low'] & self.stress['Normal'],
                          (self.intensity['Moderate'], self.volume['High'])))
                          
        # Fatigue exists but energy/sleep is good
        rules.append(ctrl.Rule(self.sleep['Good'] & self.soreness['Moderate'] & self.energy['Surplus'],
                          (self.intensity['High'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.sleep['Average'] & self.soreness['Moderate'] & self.energy['Surplus'],
                          (self.intensity['Moderate'], self.volume['Medium'])))
                          
        # Low energy but otherwise fine
        rules.append(ctrl.Rule(self.energy['Deficit'] & self.soreness['Low'] & self.sleep['Good'],
                          (self.intensity['Light'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.energy['Deficit'] & self.soreness['Moderate'],
                          (self.intensity['Very Light'], self.volume['Low'])))
                          
        # Stress focused rules
        rules.append(ctrl.Rule(self.stress['High'] & self.sleep['Average'] & self.energy['Balanced'],
                          (self.intensity['Light'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.stress['Low'] & self.sleep['Poor'] & self.soreness['Low'],
                          (self.intensity['Light'], self.volume['Low'])))
                          
        # Intermediate/Mixed conditions (To prevent dead zones)
        rules.append(ctrl.Rule(self.sleep['Average'] | self.energy['Balanced'] | self.stress['Normal'],
                          (self.intensity['Moderate'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.soreness['Low'] & self.energy['Surplus'] & self.stress['High'],
                          (self.intensity['Moderate'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.soreness['High'] & self.sleep['Good'] & self.energy['Surplus'],
                          (self.intensity['Light'], self.volume['Low'])))
        rules.append(ctrl.Rule(self.sleep['Poor'] & self.energy['Balanced'] & self.soreness['Moderate'],
                          (self.intensity['Light'], self.volume['Low'])))
        rules.append(ctrl.Rule(self.energy['Deficit'] & self.sleep['Average'] & self.stress['Normal'],
                          (self.intensity['Light'], self.volume['Medium'])))
        rules.append(ctrl.Rule(self.soreness['Moderate'] & self.stress['Low'] & self.energy['Balanced'],
                          (self.intensity['Moderate'], self.volume['Medium'])))

        # 4. Create Control System
        self.fitness_ctrl = ctrl.ControlSystem(rules)
        self.fitness_sim = ctrl.ControlSystemSimulation(self.fitness_ctrl)
        
    def evaluate(self, sleep_val, soreness_val, energy_val, stress_val, defuzz_method='centroid'):
        # Set dynamic defuzzification method
        self.intensity.defuzzify_method = defuzz_method
        self.volume.defuzzify_method = defuzz_method
        
        # Provide crisp inputs to the system
        self.fitness_sim.input['Sleep Quality'] = sleep_val
        self.fitness_sim.input['Muscle Soreness'] = soreness_val
        self.fitness_sim.input['Energy Level'] = energy_val
        self.fitness_sim.input['Stress Level'] = stress_val
        
        # Compute Defuzzification
        try:
            self.fitness_sim.compute()
            intensity = self.fitness_sim.output['Workout Intensity (%)']
            volume = self.fitness_sim.output['Workout Volume (Min)']
        except (KeyError, ValueError):
            # Fallback if no rules strongly match (should be rare with 18 rules)
            intensity = 50.0
            volume = 60.0
            
        return {
            'intensity': intensity,
            'volume': volume
        }

    def evaluate_sugeno(self, sleep_val, soreness_val, energy_val, stress_val):
        """Computes outputs using a Sugeno-style Fuzzy Inference System."""
        # Fuzzification
        s = {
            'Poor': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Poor'].mf, sleep_val)),
            'Average': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Average'].mf, sleep_val)),
            'Good': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Good'].mf, sleep_val))
        }
        so = {
            'Low': float(fuzz.interp_membership(self.soreness.universe, self.soreness['Low'].mf, soreness_val)),
            'Moderate': float(fuzz.interp_membership(self.soreness.universe, self.soreness['Moderate'].mf, soreness_val)),
            'High': float(fuzz.interp_membership(self.soreness.universe, self.soreness['High'].mf, soreness_val))
        }
        e = {
            'Deficit': float(fuzz.interp_membership(self.energy.universe, self.energy['Deficit'].mf, energy_val)),
            'Balanced': float(fuzz.interp_membership(self.energy.universe, self.energy['Balanced'].mf, energy_val)),
            'Surplus': float(fuzz.interp_membership(self.energy.universe, self.energy['Surplus'].mf, energy_val))
        }
        st_val = {
            'Low': float(fuzz.interp_membership(self.stress.universe, self.stress['Low'].mf, stress_val)),
            'Normal': float(fuzz.interp_membership(self.stress.universe, self.stress['Normal'].mf, stress_val)),
            'High': float(fuzz.interp_membership(self.stress.universe, self.stress['High'].mf, stress_val))
        }

        # Singletons definition
        # Intensity (%)
        i_sing = {
            'Very Light': 15.0,
            'Light': 35.0,
            'Moderate': 55.0,
            'High': 75.0,
            'Maximum': 95.0
        }
        # Volume (Min)
        v_sing = {
            'Low': 25.0,
            'Medium': 65.0,
            'High': 105.0
        }

        # Rule evaluation (Firing strengths and corresponding singleton outputs)
        rules = [
            (max(s['Poor'], so['High'], st_val['High']), i_sing['Very Light'], v_sing['Low']),
            (min(e['Deficit'], so['High']), i_sing['Very Light'], v_sing['Low']),
            (min(s['Good'], so['Low'], e['Surplus'], st_val['Low']), i_sing['Maximum'], v_sing['High']),
            (min(s['Good'], so['Low'], e['Balanced'], st_val['Normal']), i_sing['High'], v_sing['High']),
            (min(s['Average'], so['Moderate'], e['Balanced']), i_sing['Moderate'], v_sing['Medium']),
            (min(s['Average'], so['Low'], st_val['Normal']), i_sing['Moderate'], v_sing['High']),
            (min(s['Good'], so['Moderate'], e['Surplus']), i_sing['High'], v_sing['Medium']),
            (min(s['Average'], so['Moderate'], e['Surplus']), i_sing['Moderate'], v_sing['Medium']),
            (min(e['Deficit'], so['Low'], s['Good']), i_sing['Light'], v_sing['Medium']),
            (min(e['Deficit'], so['Moderate']), i_sing['Very Light'], v_sing['Low']),
            (min(st_val['High'], s['Average'], e['Balanced']), i_sing['Light'], v_sing['Medium']),
            (min(st_val['Low'], s['Poor'], so['Low']), i_sing['Light'], v_sing['Low']),
            (max(s['Average'], e['Balanced'], st_val['Normal']), i_sing['Moderate'], v_sing['Medium']),
            (min(so['Low'], e['Surplus'], st_val['High']), i_sing['Moderate'], v_sing['Medium']),
            (min(so['High'], s['Good'], e['Surplus']), i_sing['Light'], v_sing['Low']),
            (min(s['Poor'], e['Balanced'], so['Moderate']), i_sing['Light'], v_sing['Low']),
            (min(e['Deficit'], s['Average'], st_val['Normal']), i_sing['Light'], v_sing['Medium']),
            (min(so['Moderate'], st_val['Low'], e['Balanced']), i_sing['Moderate'], v_sing['Medium'])
        ]

        # Calculate weighted average
        sum_w = 0.0
        sum_w_int = 0.0
        sum_w_vol = 0.0

        for w, int_val, vol_val in rules:
            sum_w += w
            sum_w_int += w * int_val
            sum_w_vol += w * vol_val

        if sum_w > 0:
            intensity = sum_w_int / sum_w
            volume = sum_w_vol / sum_w
        else:
            intensity = 50.0
            volume = 60.0

        return {
            'intensity': intensity,
            'volume': volume
        }

    def get_membership_values(self, sleep_val, soreness_val, energy_val, stress_val):

        """Returns the membership value (degree of activation) for each linguistic category of each input variable."""
        return {
            'Sleep Quality': {
                'Poor': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Poor'].mf, sleep_val)),
                'Average': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Average'].mf, sleep_val)),
                'Good': float(fuzz.interp_membership(self.sleep.universe, self.sleep['Good'].mf, sleep_val))
            },
            'Muscle Soreness': {
                'Low': float(fuzz.interp_membership(self.soreness.universe, self.soreness['Low'].mf, soreness_val)),
                'Moderate': float(fuzz.interp_membership(self.soreness.universe, self.soreness['Moderate'].mf, soreness_val)),
                'High': float(fuzz.interp_membership(self.soreness.universe, self.soreness['High'].mf, soreness_val))
            },
            'Energy Level': {
                'Deficit': float(fuzz.interp_membership(self.energy.universe, self.energy['Deficit'].mf, energy_val)),
                'Balanced': float(fuzz.interp_membership(self.energy.universe, self.energy['Balanced'].mf, energy_val)),
                'Surplus': float(fuzz.interp_membership(self.energy.universe, self.energy['Surplus'].mf, energy_val))
            },
            'Stress Level': {
                'Low': float(fuzz.interp_membership(self.stress.universe, self.stress['Low'].mf, stress_val)),
                'Normal': float(fuzz.interp_membership(self.stress.universe, self.stress['Normal'].mf, stress_val)),
                'High': float(fuzz.interp_membership(self.stress.universe, self.stress['High'].mf, stress_val))
            }
        }

