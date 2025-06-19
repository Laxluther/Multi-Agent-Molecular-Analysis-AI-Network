from crewai.tools import tool
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime


def assessment_confidence(interactions, protein_analyses):
    """Fixed function name and logic"""
    confidence_factors = []
    
    if interactions:
        interaction_confidences = [i.get("confidence_score", 0.5) for i in interactions]
        confidence_factors.append(np.mean(interaction_confidences))
        
    if protein_analyses:
        # Fixed: protein_analyses is a dict, not a list
        protein_confidences = [p.get("analysis_confidence", 0.7) for p in protein_analyses.values()]
        confidence_factors.append(np.mean(protein_confidences))
    
    data_completeness = len(confidence_factors) / 2
    confidence_factors.append(data_completeness)
    
    overall_confidence = np.mean(confidence_factors) if confidence_factors else 0.5
    return overall_confidence

@tool
def safety_score(interactions: List[Dict[str, Any]], 
                 protein_analyses: Dict[str, Any],
                 regulatory_limits: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall food safety score based on multiple factors
    
    Args:
        interactions: List of toxin-protein interactions
        protein_analyses: Protein analysis results
        regulatory_limits: Regulatory safety limits
        
    Returns:
        Safety score analysis
    """
    # Initialize scoring components
    interaction_risk = 0.0
    protein_stability_risk = 0.0
    regulatory_compliance = 0.0
    
    # Analyze toxin-protein interactions
    if interactions and len(interactions) > 0:
        interaction_scores = []
        for interaction in interactions:
            # Extract risk factors with proper error handling
            binding_affinity = abs(interaction.get('binding_affinity', 0))
            toxicity_enhancement = interaction.get('toxicity_enhancement', 1.0)
            structural_changes = interaction.get('structural_changes', {})
            
            # Calculate interaction risk (0-10 scale)
            affinity_risk = min(binding_affinity / 2.0, 5.0)  # Strong binding = high risk
            enhancement_risk = min(toxicity_enhancement - 1.0, 3.0)  # Enhancement = risk
            
            # Structural change risk
            overall_change = structural_changes.get('overall_change', 0) if isinstance(structural_changes, dict) else 0
            structure_risk = min(overall_change / 10.0, 2.0)
            
            total_risk = affinity_risk + enhancement_risk + structure_risk
            interaction_scores.append(total_risk)
        
        interaction_risk = np.mean(interaction_scores)
    
    # Analyze protein stability
    if protein_analyses and len(protein_analyses) > 0:
        stability_scores = []
        for protein_name, analysis in protein_analyses.items():
            if isinstance(analysis, dict):
                stability_score = analysis.get('stability_score', 7.0)
                # Convert to risk (lower stability = higher risk)
                risk_score = max(0, (7.0 - stability_score) / 7.0 * 5.0)
                stability_scores.append(risk_score)
        
        protein_stability_risk = np.mean(stability_scores) if stability_scores else 0.0
    
    # Check regulatory compliance
    compliance_violations = 0
    total_limits = len(regulatory_limits)
    
    for compound, limit_info in regulatory_limits.items():
        if isinstance(limit_info, dict):
            detected_level = limit_info.get('detected_level', 0)
            safety_limit = limit_info.get('limit', float('inf'))
            
            if detected_level > safety_limit:
                compliance_violations += 1
    
    if total_limits > 0:
        regulatory_compliance = (compliance_violations / total_limits) * 5.0
    
    # Calculate overall safety score (10 = safest, 0 = most dangerous)
    total_risk = interaction_risk + protein_stability_risk + regulatory_compliance
    safety_score_val = max(0, 10.0 - total_risk)
    
    # Determine risk level
    if safety_score_val >= 8.0:
        risk_level = "Safe"
    elif safety_score_val >= 6.0:
        risk_level = "Low"
    elif safety_score_val >= 4.0:
        risk_level = "Moderate"
    elif safety_score_val >= 2.0:
        risk_level = "High"
    else:
        risk_level = "Dangerous"
    
    return {
        'overall_safety_score': round(safety_score_val, 2),
        'risk_level': risk_level,
        'component_risks': {
            'interaction_risk': round(interaction_risk, 2),
            'protein_stability_risk': round(protein_stability_risk, 2),
            'regulatory_compliance_risk': round(regulatory_compliance, 2)
        },
        'risk_factors': len([r for r in [interaction_risk, protein_stability_risk, regulatory_compliance] if r > 2.0]),
        'confidence_score': assessment_confidence(interactions, protein_analyses),
        'assessment_timestamp': datetime.now().isoformat()
    }
        
@tool 
def assess_critical_control_points(food_type: str, processing_conditions: Dict[str, Any],
                                 identified_hazards: List[str]) -> List[Dict[str, Any]]:
    """
    Identify Critical Control Points (CCPs) for HACCP compliance
    
    Args:
        food_type: Type of food product
        processing_conditions: Processing parameters
        identified_hazards: List of identified hazards
        
    Returns:
        List of Critical Control Points
    """
    ccps = []
    
    # Ensure processing_conditions is a dict
    if not isinstance(processing_conditions, dict):
        processing_conditions = {}
        
    # Ensure identified_hazards is a list
    if not isinstance(identified_hazards, list):
        identified_hazards = []
    
    # Temperature-based CCPs
    temperature = processing_conditions.get('temperature', 25.0)
    if isinstance(temperature, (int, float)) and temperature > 60.0:  # Heat treatment
        ccps.append({
            'ccp_id': 'CCP-1',
            'control_point': 'Heat Treatment Temperature',
            'hazard_addressed': 'Pathogenic microorganisms',
            'critical_limit': f'>= 70°C for 2 minutes or equivalent',
            'current_value': f"{temperature}°C",
            'monitoring_method': 'Continuous temperature monitoring',
            'corrective_action': 'Increase temperature or extend time',
            'verification': 'Daily calibration of temperature sensors',
            'compliance_status': 'compliant' if temperature >= 70.0 else 'non_compliant'
        })
    
    # pH-based CCPs
    ph = processing_conditions.get('ph', 7.0)
    if isinstance(ph, (int, float)) and ph < 4.6:  # Acidic foods
        ccps.append({
            'ccp_id': 'CCP-2',
            'control_point': 'pH Control',
            'hazard_addressed': 'Clostridium botulinum growth',
            'critical_limit': '<= 4.6',
            'current_value': str(ph),
            'monitoring_method': 'pH measurement every batch',
            'corrective_action': 'Adjust acid levels',
            'verification': 'Weekly pH meter calibration',
            'compliance_status': 'compliant' if ph <= 4.6 else 'non_compliant'
        })
    
    # Water activity CCPs (for shelf-stable products)
    if food_type and food_type.lower() in ['dried', 'dehydrated', 'powder']:
        ccps.append({
            'ccp_id': 'CCP-3',
            'control_point': 'Water Activity',
            'hazard_addressed': 'Mold growth and mycotoxins',
            'critical_limit': '<= 0.85 aw',
            'current_value': '0.75 aw (estimated)',
            'monitoring_method': 'Water activity measurement',
            'corrective_action': 'Additional drying',
            'verification': 'Instrument calibration',
            'compliance_status': 'compliant'
        })
    
    # Chemical hazard CCPs
    for hazard in identified_hazards:
        if isinstance(hazard, str) and ('toxin' in hazard.lower() or 'contaminant' in hazard.lower()):
            ccps.append({
                'ccp_id': f'CCP-CHEM-{len(ccps)+1}',
                'control_point': f'{hazard} Control',
                'hazard_addressed': hazard,
                'critical_limit': 'Below regulatory limits',
                'current_value': 'To be determined',
                'monitoring_method': 'Periodic testing',
                'corrective_action': 'Reject/reprocess batch',
                'verification': 'Third-party testing',
                'compliance_status': 'requires_testing'
            })
    
    # Metal detection CCP (if applicable)
    if food_type and food_type.lower() in ['processed', 'packaged']:
        ccps.append({
            'ccp_id': 'CCP-METAL',
            'control_point': 'Metal Detection',
            'hazard_addressed': 'Physical contamination',
            'critical_limit': 'No metal particles > 2mm',
            'current_value': 'Not detected',
            'monitoring_method': 'Metal detector on production line',
            'corrective_action': 'Remove contaminated product',
            'verification': 'Daily metal detector testing',
            'compliance_status': 'compliant'
        })
        
    return ccps

@tool
def safety_recommendations(safety_analysis: Dict[str, Any],
                          processing_conditions: Dict[str, Any],
                          food_type: str) -> List[Dict[str, Any]]:
    """
    Generate specific safety recommendations based on analysis
    
    Args:
        safety_analysis: Results of safety assessment
        processing_conditions: Current processing parameters
        food_type: Type of food product
        
    Returns:
        List of safety recommendations
    """

    recommendations = []
    
    # Ensure inputs are correct types
    if not isinstance(safety_analysis, dict):
        safety_analysis = {}
    if not isinstance(processing_conditions, dict):
        processing_conditions = {}
    if not isinstance(food_type, str):
        food_type = "unknown"
        
    safety_score_val = safety_analysis.get('overall_safety_score', 5.0)
    risk_level = safety_analysis.get('risk_level', 'moderate')
    component_risks = safety_analysis.get('component_risks', {})
    
    # High-priority recommendations based on risk level
    if risk_level.lower() in ['high', 'critical', 'dangerous']:
        recommendations.append({
            'priority': 'CRITICAL',
            'category': 'Immediate Action Required',
            'recommendation': 'Immediate review and modification of processing parameters required',
            'rationale': f'Safety score ({safety_score_val}) indicates significant risk',
            'implementation': 'Stop production until issues resolved',
            'timeline': 'Immediate',
            'responsible_party': 'Food Safety Manager'
        })
    
    # Interaction-specific recommendations
    interaction_risk = component_risks.get('interaction_risk', 0)
    if interaction_risk > 3.0:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Toxin Mitigation',
            'recommendation': 'Implement toxin reduction strategies during processing',
            'rationale': f'High interaction risk detected ({interaction_risk}/10)',
            'implementation': 'Add detoxification steps or binding agents',
            'timeline': '1-2 weeks',
            'responsible_party': 'Process Engineer'
        })
    
    # Protein stability recommendations
    stability_risk = component_risks.get('protein_stability_risk', 0)
    if stability_risk > 2.0:
        temperature = processing_conditions.get('temperature', 25)
        ph = processing_conditions.get('ph', 7.0)
        
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Processing Optimization',
            'recommendation': f'Optimize processing conditions to maintain protein stability',
            'rationale': f'Protein stability risk detected ({stability_risk}/10)',
            'implementation': f'Consider reducing temperature from {temperature}°C or adjusting pH from {ph}',
            'timeline': '2-4 weeks',
            'responsible_party': 'R&D Team'
        })
    
    # Food-specific recommendations
    if 'dairy' in food_type.lower():
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Dairy Safety',
            'recommendation': 'Implement enhanced mycotoxin monitoring for dairy products',
            'rationale': 'Dairy proteins show vulnerability to aflatoxin binding',
            'implementation': 'Regular testing of feed and milk for mycotoxins',
            'timeline': 'Ongoing',
            'responsible_party': 'Quality Assurance'
        })
    
    elif any(term in food_type.lower() for term in ['grain', 'cereal']):
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Grain Safety',
            'recommendation': 'Implement pre-harvest and post-harvest mycotoxin control',
            'rationale': 'Grain products susceptible to multiple mycotoxins',
            'implementation': 'Proper storage conditions, mold inhibitors',
            'timeline': '1 month',
            'responsible_party': 'Supply Chain Manager'
        })
    
    # General safety recommendations
    recommendations.extend([
        {
            'priority': 'MEDIUM',
            'category': 'Monitoring & Testing',
            'recommendation': 'Establish routine toxin monitoring program',
            'rationale': 'Proactive detection of contamination',
            'implementation': 'Monthly testing of raw materials and products',
            'timeline': '2 months',
            'responsible_party': 'Laboratory Manager'
        },
        {
            'priority': 'LOW',
            'category': 'Training',
            'recommendation': 'Train staff on food safety hazards and controls',
            'rationale': 'Human factor in food safety management',
            'implementation': 'Quarterly training sessions',
            'timeline': '3 months',
            'responsible_party': 'HR & Food Safety'
        },
        {
            'priority': 'MEDIUM',
            'category': 'Documentation',
            'recommendation': 'Update HACCP plan with molecular interaction data',
            'rationale': 'Incorporate advanced safety analysis methods',
            'implementation': 'Revise hazard analysis and CCPs',
            'timeline': '1 month',
            'responsible_party': 'Food Safety Team'
        }
    ])
    
    # Sort by priority
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    return recommendations
@tool
def assess_regulatory_compliance(food_type: str, country: str,
                            detected_compounds: Dict[str, float]) -> Dict[str, Any]:
    """
    Assess regulatory compliance for food safety

    Args:
        food_type: Type of food product
        country: Target market country
        detected_compounds: Detected compounds with concentrations
        
    Returns:
        Regulatory compliance assessment
    """
    regulatory_limits = {
        'us': {
            'aflatoxin_b1': {'limit': 20.0, 'unit': 'ppb', 'regulation': 'FDA 21 CFR 109.15'},
            'aflatoxin_total': {'limit': 20.0, 'unit': 'ppb', 'regulation': 'FDA 21 CFR 109.15'},
            'ochratoxin_a': {'limit': 10.0, 'unit': 'ppb', 'regulation': 'FDA Guidance'},
            'fumonisin': {'limit': 4000.0, 'unit': 'ppb', 'regulation': 'FDA Guidance'},
            'deoxynivalenol': {'limit': 1000.0, 'unit': 'ppb', 'regulation': 'FDA Guidance'},
            'patulin': {'limit': 50.0, 'unit': 'ppb', 'regulation': 'FDA 21 CFR 109.35'}
        },
        'eu': {
            'aflatoxin_b1': {'limit': 2.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'},
            'aflatoxin_total': {'limit': 4.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'},
            'ochratoxin_a': {'limit': 5.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'},
            'fumonisin': {'limit': 1000.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'},
            'deoxynivalenol': {'limit': 750.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'},
            'patulin': {'limit': 25.0, 'unit': 'ppb', 'regulation': 'EC 1881/2006'}
        }
    }
    
    # Ensure inputs are correct types
    if not isinstance(detected_compounds, dict):
        detected_compounds = {}
    if not isinstance(country, str):
        country = "us"
    if not isinstance(food_type, str):
        food_type = "unknown"
    
    # Food-specific adjustments
    food_specific_limits = {
        'infant_food': {
            'aflatoxin_b1': 0.1,  # Much stricter for baby food
            'ochratoxin_a': 0.5
        },
        'dairy': {
            'aflatoxin_m1': 0.5  # Specific limit for milk
        }
    }
    
    country_limits = regulatory_limits.get(country.lower(), regulatory_limits['us'])
    
    # Apply food-specific adjustments
    if food_type.lower() in food_specific_limits:
        country_limits.update(food_specific_limits[food_type.lower()])
    
    compliance_results = {}
    violations = []
    warnings = []
    
    for compound, detected_level in detected_compounds.items():
        if not isinstance(detected_level, (int, float)):
            continue
            
        compound_clean = compound.lower().replace(' ', '_').replace('-', '_')
        
        if compound_clean in country_limits:
            limit_info = country_limits[compound_clean]
            limit_value = limit_info['limit']
            regulation = limit_info['regulation']
            
            # Check compliance
            if detected_level > limit_value:
                status = 'violation'
                violations.append({
                    'compound': compound,
                    'detected': detected_level,
                    'limit': limit_value,
                    'excess_factor': round(detected_level / limit_value, 2),
                    'regulation': regulation,
                    'severity': 'high' if detected_level > limit_value * 2 else 'medium'
                })
            elif detected_level > limit_value * 0.8:  # Warning threshold
                status = 'warning'
                warnings.append({
                    'compound': compound,
                    'detected': detected_level,
                    'limit': limit_value,
                    'percentage_of_limit': round((detected_level / limit_value) * 100, 1),
                    'regulation': regulation
                })
            else:
                status = 'compliant'
            
            compliance_results[compound] = {
                'status': status,
                'detected_level': detected_level,
                'regulatory_limit': limit_value,
                'unit': limit_info['unit'],
                'regulation': regulation,
                'margin_of_safety': round((limit_value - detected_level) / limit_value * 100, 1) if detected_level <= limit_value else 0
            }
    
    # Overall compliance status
    if violations:
        overall_status = 'non_compliant'
    elif warnings:
        overall_status = 'compliant_with_warnings'
    else:
        overall_status = 'fully_compliant'
    
    return {
        'overall_status': overall_status,
        'country': country.upper(),
        'food_type': food_type,
        'compliance_results': compliance_results,
        'violations': violations,
        'warnings': warnings,
        'total_compounds_assessed': len(detected_compounds),
        'compliant_compounds': len([r for r in compliance_results.values() if r['status'] == 'compliant']),
        'assessment_date': datetime.now().isoformat(),
        'next_review_date': (datetime.now().replace(month=min(datetime.now().month + 3, 12))).isoformat()
    }
    