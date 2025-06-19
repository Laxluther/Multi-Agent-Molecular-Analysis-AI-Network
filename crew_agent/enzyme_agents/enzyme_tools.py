from crewai.tools import tool
from typing import List, Dict, Any, Optional
import math
import numpy as np

@tool
def simulate_enzyme_kinetics(enzyme_name: str, substrate: str,
                           conditions: Dict[str, Any],
                           inhibitors: List[str] = None) -> Dict[str, Any]:
    """
    Simulate enzyme kinetics under specified conditions
    
    Args:
        enzyme_name: Name of the enzyme
        substrate: Primary substrate
        conditions: Reaction conditions
        inhibitors: List of potential inhibitors
        
    Returns:
        Enzyme kinetics simulation results
    """
    
    # Load enzyme database
    enzyme_database = load_enzyme_database()
    
    # Add inhibitors to conditions
    conditions_with_inhibitors = conditions.copy()
    conditions_with_inhibitors['inhibitors'] = inhibitors or []
    
    # Simulate kinetics
    kinetics = simulate_kinetics_parameters(enzyme_name, substrate, conditions_with_inhibitors, enzyme_database)
    
    return kinetics

def load_enzyme_database() -> Dict[str, Dict[str, Any]]:
    """Load enzyme kinetic parameters database"""
    return {
        'amylase': {
            'substrates': ['starch', 'amylose', 'amylopectin'],
            'km': {'starch': 2.5, 'amylose': 1.8, 'amylopectin': 3.2},  # mM
            'vmax': {'starch': 45.0, 'amylose': 38.0, 'amylopectin': 52.0},  # μmol/min/mg
            'kcat': {'starch': 1200, 'amylose': 980, 'amylopectin': 1350},  # s⁻¹
            'optimal_ph': 6.8,
            'optimal_temp': 55.0,
            'molecular_weight': 56000.0,
            'cofactors': ['Ca2+', 'Cl-']
        },
        'protease': {
            'substrates': ['casein', 'albumin', 'globulin'],
            'km': {'casein': 0.8, 'albumin': 1.2, 'globulin': 1.5},
            'vmax': {'casein': 25.0, 'albumin': 18.0, 'globulin': 22.0},
            'kcat': {'casein': 450, 'albumin': 320, 'globulin': 380},
            'optimal_ph': 8.5,
            'optimal_temp': 45.0,
            'molecular_weight': 35000.0,
            'cofactors': ['Zn2+']
        },
        'lipase': {
            'substrates': ['triglycerides', 'phospholipids'],
            'km': {'triglycerides': 0.5, 'phospholipids': 0.3},
            'vmax': {'triglycerides': 35.0, 'phospholipids': 28.0},
            'kcat': {'triglycerides': 890, 'phospholipids': 720},
            'optimal_ph': 8.0,
            'optimal_temp': 40.0,
            'molecular_weight': 42000.0,
            'cofactors': ['Ca2+']
        },
        'peroxidase': {
            'substrates': ['H2O2', 'phenolic_compounds'],
            'km': {'H2O2': 0.1, 'phenolic_compounds': 0.05},
            'vmax': {'H2O2': 75.0, 'phenolic_compounds': 65.0},
            'kcat': {'H2O2': 2500, 'phenolic_compounds': 2100},
            'optimal_ph': 7.0,
            'optimal_temp': 25.0,
            'molecular_weight': 44000.0,
            'cofactors': ['heme']
        },
        'catalase': {
            'substrates': ['H2O2'],
            'km': {'H2O2': 25.0},
            'vmax': {'H2O2': 150.0},
            'kcat': {'H2O2': 40000},  # Very high turnover
            'optimal_ph': 7.0,
            'optimal_temp': 37.0,
            'molecular_weight': 250000.0,
            'cofactors': ['heme', 'Fe3+']
        },
        'lysozyme': {
            'substrates': ['peptidoglycan'],
            'km': {'peptidoglycan': 0.006},
            'vmax': {'peptidoglycan': 85.0},
            'kcat': {'peptidoglycan': 3500},
            'optimal_ph': 9.2,
            'optimal_temp': 25.0,
            'molecular_weight': 14300.0,
            'cofactors': []
        }
    }

def simulate_kinetics_parameters(enzyme_name: str, substrate: str, 
                         conditions: Dict[str, Any], enzyme_database: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Simulate enzyme kinetics under given conditions
    
    Args:
        enzyme_name: Name of the enzyme
        substrate: Primary substrate
        conditions: Reaction conditions
        enzyme_database: Database of enzyme parameters
        
    Returns:
        Kinetics simulation results
    """
    
    # Get enzyme parameters
    enzyme_data = enzyme_database.get(enzyme_name.lower(), {})
    if not enzyme_data:
        return default_kinetics_simulation(enzyme_name, substrate)
    
    # Base kinetic parameters
    base_km = enzyme_data['km'].get(substrate, enzyme_data['km'][list(enzyme_data['km'].keys())[0]])
    base_vmax = enzyme_data['vmax'].get(substrate, enzyme_data['vmax'][list(enzyme_data['vmax'].keys())[0]])
    base_kcat = enzyme_data['kcat'].get(substrate, enzyme_data['kcat'][list(enzyme_data['kcat'].keys())[0]])
    
    # Apply environmental corrections
    corrected_params = apply_environmental_effects(
        base_km, base_vmax, base_kcat, enzyme_data, conditions
    )
    
    # Calculate inhibition effects
    inhibition_data = calculate_inhibition_effects(
        enzyme_name, conditions.get('inhibitors', [])
    )
    
    # Determine activity factors
    activity_factors = calculate_activity_factors(enzyme_data, conditions)
    
    # Create optimal conditions
    optimal_conditions = {
        'temperature': enzyme_data['optimal_temp'],
        'ph': enzyme_data['optimal_ph'],
        'duration': 60,  # Standard assay time
        'ionic_strength': 0.1
    }
    
    return {
        'enzyme_name': enzyme_name,
        'substrate': substrate,
        'km': corrected_params['km'],
        'vmax': corrected_params['vmax'],
        'kcat': corrected_params['kcat'],
        'inhibition_data': inhibition_data,
        'optimal_conditions': optimal_conditions,
        'activity_factors': activity_factors,
        'molecular_weight': enzyme_data.get('molecular_weight', 50000),
        'cofactors': enzyme_data.get('cofactors', [])
    }

def apply_environmental_effects(km: float, vmax: float, kcat: float,
                               enzyme_data: Dict[str, Any], 
                               conditions: Dict[str, Any]) -> Dict[str, float]:
    """Apply environmental effects to kinetic parameters"""
    
    # Temperature effects (Arrhenius equation approximation)
    temp = conditions.get('temperature', 25.0)
    optimal_temp = enzyme_data['optimal_temp']
    
    # Q10 temperature coefficient (typically 2-3 for enzymes)
    q10 = 2.5
    temp_factor = q10 ** ((temp - optimal_temp) / 10.0)
    
    # Temperature denaturation above optimal
    if temp > optimal_temp + 15.0:
        denaturation_factor = math.exp(-(temp - optimal_temp - 15.0) / 10.0)
        temp_factor *= denaturation_factor
    
    # pH effects (bell-shaped curve)
    ph = conditions.get('ph', 7.0)
    optimal_ph = enzyme_data['optimal_ph']
    ph_factor = math.exp(-0.5 * ((ph - optimal_ph) / 1.5) ** 2)  # Gaussian
    
    # Ionic strength effects
    ionic_strength = conditions.get('ionic_strength', 0.15)
    # Most enzymes have optimal activity around 0.1-0.2 M
    if ionic_strength < 0.05:
        ionic_factor = 0.7  # Too low salt
    elif ionic_strength > 0.5:
        ionic_factor = 0.8  # Too high salt
    else:
        ionic_factor = 1.0
    
    # Combined effects
    overall_factor = temp_factor * ph_factor * ionic_factor
    
    return {
        'km': km / ph_factor,  # pH affects binding affinity
        'vmax': vmax * overall_factor,  # All factors affect Vmax
        'kcat': kcat * temp_factor * ionic_factor  # Temperature and ionic strength affect turnover
    }

def calculate_inhibition_effects(enzyme_name: str, 
                                inhibitors: List[str]) -> Dict[str, Dict[str, float]]:
    """Calculate inhibition constants and types"""
    inhibition_data = {}
    
    # Common enzyme inhibitors in food
    inhibitor_database = {
        'heavy_metals': {
            'ki': 0.01,  # mM
            'type': 'competitive',
            'severity': 'high'
        },
        'phenolic_compounds': {
            'ki': 0.5,
            'type': 'non_competitive',
            'severity': 'medium'
        },
        'organic_acids': {
            'ki': 2.0,
            'type': 'competitive',
            'severity': 'low'
        },
        'salts': {
            'ki': 10.0,
            'type': 'uncompetitive',
            'severity': 'low'
        }
    }
    
    for inhibitor in inhibitors:
        # Map specific inhibitors to categories
        inhibitor_category = categorize_inhibitor(inhibitor)
        if inhibitor_category in inhibitor_database:
            base_data = inhibitor_database[inhibitor_category].copy()
            
            # Enzyme-specific adjustments
            if enzyme_name.lower() == 'amylase' and 'phenolic' in inhibitor_category:
                base_data['ki'] *= 0.5  # Amylase more sensitive to phenolics
            elif enzyme_name.lower() == 'protease' and 'heavy_metals' in inhibitor_category:
                base_data['ki'] *= 0.2  # Protease very sensitive to metals
            
            inhibition_data[inhibitor] = base_data
    
    return inhibition_data

def categorize_inhibitor(inhibitor: str) -> str:
    """Categorize inhibitor by type"""
    inhibitor_lower = inhibitor.lower()
    
    if any(metal in inhibitor_lower for metal in ['pb', 'hg', 'cd', 'cu', 'lead', 'mercury', 'cadmium']):
        return 'heavy_metals'
    elif any(compound in inhibitor_lower for compound in ['phenol', 'tannin', 'flavonoid']):
        return 'phenolic_compounds'
    elif any(acid in inhibitor_lower for acid in ['citric', 'acetic', 'lactic', 'malic']):
        return 'organic_acids'
    elif any(salt in inhibitor_lower for salt in ['nacl', 'kcl', 'mgcl2', 'cacl2', 'salt']):
        return 'salts'
    else:
        return 'phenolic_compounds'  # Default category

def calculate_activity_factors(enzyme_data: Dict[str, Any], 
                              conditions: Dict[str, Any]) -> Dict[str, float]:
    """Calculate activity factors for different conditions"""
    factors = {}
    
    # Temperature factor
    temp = conditions.get('temperature', 25.0)
    optimal_temp = enzyme_data['optimal_temp']
    
    if abs(temp - optimal_temp) <= 5.0:
        factors['temperature'] = 1.0
    elif abs(temp - optimal_temp) <= 15.0:
        factors['temperature'] = 0.7
    elif abs(temp - optimal_temp) <= 30.0:
        factors['temperature'] = 0.3
    else:
        factors['temperature'] = 0.1
    
    # pH factor
    ph = conditions.get('ph', 7.0)
    optimal_ph = enzyme_data['optimal_ph']
    
    if abs(ph - optimal_ph) <= 0.5:
        factors['ph'] = 1.0
    elif abs(ph - optimal_ph) <= 1.5:
        factors['ph'] = 0.8
    elif abs(ph - optimal_ph) <= 3.0:
        factors['ph'] = 0.4
    else:
        factors['ph'] = 0.1
    
    # Substrate concentration factor
    substrate_conc = conditions.get('substrate_concentration', 1.0)  # mM
    km = enzyme_data['km'][list(enzyme_data['km'].keys())[0]]  # Use first substrate's Km
    
    # Michaelis-Menten saturation
    saturation = substrate_conc / (km + substrate_conc)
    factors['substrate_saturation'] = saturation
    
    # Time factor (for stability)
    reaction_time = conditions.get('duration', 60)  # minutes
    if reaction_time <= 60:
        factors['time_stability'] = 1.0
    elif reaction_time <= 240:
        factors['time_stability'] = 0.9
    elif reaction_time <= 1440:  # 24 hours
        factors['time_stability'] = 0.7
    else:
        factors['time_stability'] = 0.5
    
    return factors

def default_kinetics_simulation(enzyme_name: str, substrate: str) -> Dict[str, Any]:
    """Provide default kinetics for unknown enzymes"""
    return {
        'enzyme_name': enzyme_name,
        'substrate': substrate,
        'km': 1.0,  # mM
        'vmax': 20.0,  # μmol/min/mg
        'kcat': 500,  # s⁻¹
        'inhibition_data': {},
        'optimal_conditions': {
            'temperature': 37.0,
            'ph': 7.0,
            'duration': 60,
            'ionic_strength': 0.15
        },
        'activity_factors': {'temperature': 0.8, 'ph': 0.8, 'substrate_saturation': 0.5},
        'molecular_weight': 50000,
        'cofactors': []
    }

@tool
def predict_enzyme_inhibition(enzyme_name: str, inhibitor_name: str,
                            inhibitor_concentration: float,
                            conditions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict enzyme inhibition by specific compounds
    
    Args:
        enzyme_name: Name of the enzyme
        inhibitor_name: Name of the inhibitor
        inhibitor_concentration: Concentration of inhibitor (mM)
        conditions: Reaction conditions
        
    Returns:
        Inhibition prediction results
    """
    
    # Simulate without inhibitor
    baseline_kinetics = simulate_kinetics_parameters(enzyme_name, 'substrate', conditions, load_enzyme_database())
    
    # Simulate with inhibitor
    conditions_with_inhibitor = conditions.copy()
    conditions_with_inhibitor['inhibitors'] = [inhibitor_name]
    
    inhibited_kinetics = simulate_kinetics_parameters(enzyme_name, 'substrate', conditions_with_inhibitor, load_enzyme_database())
    
    # Calculate inhibition metrics
    if inhibitor_name in inhibited_kinetics['inhibition_data']:
        inhibition_info = inhibited_kinetics['inhibition_data'][inhibitor_name]
        ki = inhibition_info['ki']
        inhibition_type = inhibition_info['type']
        
        # Calculate fractional activity based on inhibition type
        if inhibition_type == 'competitive':
            fractional_activity = 1 / (1 + inhibitor_concentration / ki)
        elif inhibition_type == 'non_competitive':
            fractional_activity = 1 / (1 + inhibitor_concentration / ki)
        elif inhibition_type == 'uncompetitive':
            # For simplified calculation
            fractional_activity = 1 / (1 + inhibitor_concentration / ki)
        else:
            fractional_activity = 0.8  # Default moderate inhibition
        
        percent_inhibition = (1 - fractional_activity) * 100
        
    else:
        # Default inhibition for unknown inhibitors
        fractional_activity = 0.7
        percent_inhibition = 30.0
        inhibition_type = 'mixed'
        ki = 1.0
    
    return {
        'enzyme_name': enzyme_name,
        'inhibitor_name': inhibitor_name,
        'inhibitor_concentration': inhibitor_concentration,
        'baseline_activity': baseline_kinetics['vmax'],
        'inhibited_activity': baseline_kinetics['vmax'] * fractional_activity,
        'percent_inhibition': round(percent_inhibition, 2),
        'inhibition_type': inhibition_type,
        'ki_value': ki,
        'fractional_activity': round(fractional_activity, 3)
    }

@tool
def calculate_enzyme_stability(enzyme_name: str, storage_conditions: Dict[str, Any],
                             time_points: List[float]) -> Dict[str, Any]:
    """
    Calculate enzyme stability over time under storage conditions
    
    Args:
        enzyme_name: Name of the enzyme
        storage_conditions: Storage conditions (temperature, pH, etc.)
        time_points: Time points for stability assessment (hours)
        
    Returns:
        Stability analysis results
    """
    # Base stability parameters (half-life in hours at optimal conditions)
    stability_database = {
        'amylase': {'half_life': 72.0, 'temp_sensitivity': 0.1, 'ph_sensitivity': 0.05},
        'protease': {'half_life': 48.0, 'temp_sensitivity': 0.15, 'ph_sensitivity': 0.08},
        'lipase': {'half_life': 96.0, 'temp_sensitivity': 0.08, 'ph_sensitivity': 0.06},
        'peroxidase': {'half_life': 24.0, 'temp_sensitivity': 0.2, 'ph_sensitivity': 0.1},
        'catalase': {'half_life': 120.0, 'temp_sensitivity': 0.05, 'ph_sensitivity': 0.03}
    }
    
    enzyme_stability = stability_database.get(enzyme_name.lower(), 
                                            {'half_life': 48.0, 'temp_sensitivity': 0.1, 'ph_sensitivity': 0.05})
    
    # Extract conditions
    temperature = storage_conditions.get('temperature', 4.0)  # °C
    ph = storage_conditions.get('ph', 7.0)
    
    # Calculate degradation rate constant
    base_k = 0.693 / enzyme_stability['half_life']  # h⁻¹
    
    # Temperature effect (Q10 = 2 for degradation)
    temp_factor = 2 ** ((temperature - 4.0) / 10.0)
    
    # pH effect
    optimal_ph = 7.0  # Assumed optimal storage pH
    ph_factor = 1 + enzyme_stability['ph_sensitivity'] * abs(ph - optimal_ph)
    
    # Combined degradation rate
    k_degradation = base_k * temp_factor * ph_factor
    
    # Calculate remaining activity at each time point
    stability_data = []
    for time_hours in time_points:
        remaining_activity = math.exp(-k_degradation * time_hours)
        stability_data.append({
            'time_hours': time_hours,
            'remaining_activity': round(remaining_activity * 100, 2),  # Percentage
            'half_life_reached': remaining_activity <= 0.5
        })
    
    return {
        'enzyme_name': enzyme_name,
        'storage_conditions': storage_conditions,
        'degradation_rate_constant': round(k_degradation, 6),
        'predicted_half_life': round(0.693 / k_degradation, 2),
        'stability_timeline': stability_data,
        'stability_classification': classify_stability(k_degradation)
    }

def classify_stability(degradation_rate: float) -> str:
    """Classify enzyme stability based on degradation rate"""
    half_life = 0.693 / degradation_rate
    
    if half_life > 168:  # > 1 week
        return 'very_stable'
    elif half_life > 72:  # > 3 days
        return 'stable'
    elif half_life > 24:  # > 1 day
        return 'moderately_stable'
    elif half_life > 6:  # > 6 hours
        return 'unstable'
    else:
        return 'very_unstable'