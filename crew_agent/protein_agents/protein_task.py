from typing import List, Dict, Any, Optional
from crewai import Task
from protein_crew import agents

A, B, C, D, E = agents()

def protein_tasks(proteins: List[str], processing_conditions: Dict[str, Any], 
                 research_context: Dict[str, Any] = None) -> List[Task]:
    """
    Create protein analysis tasks
    
    Args:
        proteins: List of protein names to analyze
        processing_conditions: Processing conditions (pH, temperature, etc.)
        research_context: Research findings from research crew
        
    Returns:
        List of protein analysis tasks
    """
    
    if research_context is None:
        research_context = {}
    
    # Task 1: Structure Analysis with ESMFold
    structure_task = Task(
        description=f"""
        Analyze protein structures using ESMFold neural network:
        
        Proteins to analyze: {', '.join(proteins)}
        
        For each protein:
        1. Predict 3D structure using ESMFold
        2. Analyze secondary structure content
        3. Identify potential binding sites
        4. Calculate structural confidence scores
        5. Predict conformational flexibility
        
        Processing Context:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Ionic Strength: {processing_conditions.get('ionic_strength', 0.15)}M
        
        Research Context: {research_context.get('protein_studies', 'None available')}
        
        Use analyze_protein_structure tool for each protein.
        """,
        expected_output="Detailed structural analysis with ESMFold predictions, binding sites, and conformational data"
    )
    
    # Task 2: Molecular Property Calculations
    property_task = Task(
        description=f"""
        Calculate comprehensive molecular properties for food proteins:
        
        Proteins: {', '.join(proteins)}
        
        Calculate for each protein:
        1. Molecular weight (accurate calculation)
        2. Isoelectric point (pI)
        3. Hydrophobicity index
        4. Amino acid composition analysis
        5. Theoretical extinction coefficient
        6. Instability index
        
        Use the protein sequences and apply physicochemical calculations.
        Consider food safety implications of these properties.
        """,
        expected_output="Complete molecular property profile for each protein with food safety relevance"
    )
    
    # Task 3: Stability Assessment
    stability_task = Task(
        description=f"""
        Assess protein stability under food processing conditions:
        
        Processing Conditions:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Duration: {processing_conditions.get('duration', 60)} minutes
        - Ionic Strength: {processing_conditions.get('ionic_strength', 0.15)}M
        
        For each protein ({', '.join(proteins)}):
        1. Predict thermal stability
        2. Assess pH sensitivity
        3. Evaluate oxidation susceptibility
        4. Calculate processing sensitivity scores
        5. Predict denaturation risks
        
        Use assess_protein_stability_conditions and calculate_processing_sensitivity tools.
        """,
        expected_output="Comprehensive stability assessment with processing recommendations"
    )
    
    # Task 4: Functional Site Prediction
    functional_task = Task(
        description=f"""
        Predict functional sites in food proteins:
        
        Proteins to analyze: {', '.join(proteins)}
        
        For each protein:
        1. Identify active sites
        2. Predict binding sites for small molecules
        3. Locate allosteric sites
        4. Find metal binding sites
        5. Identify sites prone to toxin interaction
        
        Consider:
        - Potential toxin binding locations
        - Sites affecting protein function
        - Regions important for food safety
        
        Use predict_functional_sites_pattern tool.
        """,
        expected_output="Detailed functional site predictions with toxin interaction potential"
    )
    
    # Task 5: Protein Analysis Integration
    integration_task = Task(
        description="""
        Integrate all protein analysis results:
        
        Integration Requirements:
        1. Combine structural predictions with property calculations
        2. Correlate stability data with functional sites
        3. Identify high-risk proteins for toxin interactions
        4. Assess overall protein profile for food safety
        5. Generate protein-specific recommendations
        
        Synthesis Goals:
        - Create comprehensive protein profiles
        - Highlight food safety concerns
        - Provide processing recommendations
        - Identify proteins most at risk
        
        Output Format:
        - Executive summary of protein analysis
        - Individual protein profiles
        - Risk assessment for each protein
        - Processing optimization suggestions
        """,
        expected_output="Integrated protein analysis report with food safety risk assessment"
    )
    
    return [structure_task, property_task, stability_task, functional_task, integration_task]