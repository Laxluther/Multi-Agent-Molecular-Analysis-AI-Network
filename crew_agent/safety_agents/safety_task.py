from typing import List, Dict, Any, Optional
from crewai import Task
from langchain_ollama import ChatOllama
from safety_crew import agents

from config import llm

A, B, C, D = agents()
        
def safety_tasks(analysis_context: Dict[str, Any]) -> List[Task]:
    """
    Create safety assessment tasks
    
    Args:
        analysis_context: Context with protein analyses, interactions, etc.
        
    Returns:
        List of safety assessment tasks
    """
    
    # Extract data from context with proper defaults
    interactions = analysis_context.get('interactions', [])
    protein_analyses = analysis_context.get('protein_analyses', {})
    detected_compounds = analysis_context.get('detected_compounds', {})
    food_sample = analysis_context.get('food_sample', {})
    processing_conditions = food_sample.get('processing_conditions', {})
    food_type = food_sample.get('food_type', 'Unknown')
    
    # Create regulatory limits structure
    regulatory_limits = {}
    for compound, level in detected_compounds.items():
        regulatory_limits[compound] = {
            'detected_level': level,
            'limit': 20.0,  # Default limit, can be customized
            'unit': 'ppb'
        }
    
    # Task 1: Risk Assessment
    risk_assessment_task = Task(
        description=f"""
        Conduct comprehensive food safety risk assessment for dairy milk processing.
        
        You must use the safety_score tool and assess_critical_control_points tool with the following data:
        
        1. Call safety_score with these exact parameters:
           - interactions: {interactions}
           - protein_analyses: {protein_analyses}
           - regulatory_limits: {regulatory_limits}
        
        2. Call assess_critical_control_points with these exact parameters:
           - food_type: "{food_type}"
           - processing_conditions: {processing_conditions}
           - identified_hazards: {[interaction.get('toxin_name', '') for interaction in interactions]}
        
        Provide a comprehensive risk assessment report including:
        - Overall safety score and risk classification
        - Component risk analysis (interaction, protein stability, regulatory compliance)
        - Critical control points identification
        - Risk factor summary
        - Confidence assessment
        
        Food Type: {food_type}
        Processing Temperature: {processing_conditions.get('temperature', 'Unknown')}°C
        Processing pH: {processing_conditions.get('ph', 'Unknown')}
        Detected Compounds: {list(detected_compounds.keys())}
        """,
        expected_output="Comprehensive risk assessment report with numerical safety scores, risk classifications, and identified critical control points",
        # agent=A
    )
    
    # Task 2: Regulatory Compliance
    compliance_task = Task(
        description=f"""
        Assess regulatory compliance for the food product across different markets.
        
        You must use the assess_regulatory_compliance tool twice:
        
        1. For US market:
           - food_type: "{food_type}"
           - country: "us"
           - detected_compounds: {detected_compounds}
        
        2. For EU market:
           - food_type: "{food_type}"
           - country: "eu"
           - detected_compounds: {detected_compounds}
        
        Provide detailed regulatory compliance assessment including:
        - Overall compliance status for each market
        - Specific violations and warnings
        - Regulatory citations and standards
        - Margin of safety calculations
        - Recommendations for compliance
        
        Target Markets: US, EU
        Food Type: {food_type}
        Detected Compounds: {', '.join(detected_compounds.keys()) if detected_compounds else 'None'}
        Concentration Levels: {detected_compounds}
        """,
        expected_output="Detailed regulatory compliance report with violation status, regulatory citations, and market-specific assessments",
        # agent=B
    )
    
    # Task 3: HACCP Integration
    haccp_task = Task(
        description=f"""
        Develop comprehensive HACCP system recommendations for the food processing operation.
        
        Use the assess_critical_control_points tool with these parameters:
        - food_type: "{food_type}"
        - processing_conditions: {processing_conditions}
        - identified_hazards: {[interaction.get('toxin_name', '') for interaction in interactions]}
        
        Based on the CCP analysis, develop detailed HACCP recommendations including:
        
        1. Critical Control Points (CCPs) identification and justification
        2. Critical limits for each CCP with scientific rationale
        3. Monitoring procedures and frequencies
        4. Corrective actions for deviations
        5. Verification procedures and schedules
        6. Record-keeping requirements
        7. Responsibility assignments
        
        Processing Parameters:
        - Temperature: {processing_conditions.get('temperature', 'Unknown')}°C
        - pH: {processing_conditions.get('ph', 'Unknown')}
        - Food Type: {food_type}
        
        Identified Hazards: {[interaction.get('toxin_name', '') for interaction in interactions]}
        """,
        expected_output="Comprehensive HACCP system recommendations with specific CCPs, monitoring procedures, critical limits, and implementation guidelines",
        # agent=C
    )
    
    # Task 4: Safety Recommendations
    recommendations_task = Task(
        description=f"""
        Generate comprehensive safety recommendations based on risk assessment results.
        
        Use the safety_recommendations tool with the following structure:
        
        safety_analysis (use results from previous tasks or these default values):
        - overall_safety_score: 6.5
        - risk_level: "moderate"
        - component_risks:
          * interaction_risk: 3.2
          * protein_stability_risk: 2.1
          * regulatory_compliance_risk: 1.5
        
        Parameters:
        - processing_conditions: {processing_conditions}
        - food_type: "{food_type}"
        
        Generate prioritized safety recommendations including:
        
        1. Critical immediate actions (if any)
        2. Process optimization recommendations
        3. Monitoring and testing protocols
        4. Staff training requirements
        5. Documentation updates
        6. Supplier management improvements
        7. Implementation timelines and priorities
        8. Responsible party assignments
        9. Success metrics and KPIs
        10. Resource requirements
        
        Context:
        - Food Type: {food_type}
        - Processing Conditions: {processing_conditions}
        - Detected Compounds: {list(detected_compounds.keys()) if detected_compounds else 'None'}
        - Risk Factors: Aflatoxin B1 interaction with dairy proteins
        """,
        expected_output="Comprehensive safety recommendations with priorities, timelines, responsible parties, and implementation guidelines",
        # agent=D
    )
    
    return [risk_assessment_task, compliance_task, haccp_task, recommendations_task]