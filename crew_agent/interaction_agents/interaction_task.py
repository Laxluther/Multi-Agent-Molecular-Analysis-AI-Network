from typing import List, Dict, Any, Optional
from crewai import Task
from .interaction_crew import agents

A, B, C, D, E, F = agents()

def interaction_tasks(proteins: List[str], toxins: List[str], 
                     protein_results: Dict[str, Any], processing_conditions: Dict[str, Any],
                     research_context: Dict[str, Any] = None) -> List[Task]:
    """
    Create interaction prediction tasks
    
    Args:
        proteins: List of protein names
        toxins: List of toxin names
        protein_results: Results from protein analysis crew
        processing_conditions: Processing conditions
        research_context: Research findings from research crew
        
    Returns:
        List of interaction prediction tasks
    """
    
    if research_context is None:
        research_context = {}
    
    # Task 1: Molecular Docking Simulations
    docking_task = Task(
        description=f"""
        Perform molecular docking simulations using RDKit:
        
        Protein-Toxin Pairs to Analyze:
        {chr(10).join([f"- {protein} vs {toxin}" for protein in proteins for toxin in toxins])}
        
        From Protein Analysis Results:
        - Protein structures: {protein_results.get('structures', 'Available')}
        - Binding sites: {protein_results.get('binding_sites', 'Identified')}
        - Stability scores: {protein_results.get('stability', 'Calculated')}
        
        Processing Conditions:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Ionic Strength: {processing_conditions.get('ionic_strength', 0.15)}M
        
        Research Context: {research_context.get('known_interactions', 'None available')}
        
        For each protein-toxin pair:
        1. Use RDKit to dock toxin molecules to protein binding sites
        2. Calculate binding poses and scores
        3. Identify contact residues
        4. Rank poses by binding affinity
        5. Consider environmental conditions effects
        
        Use predict_toxin_protein_interaction tool for each pair.
        """,
        expected_output="Comprehensive molecular docking results with binding poses, affinities, and contact analyses"
    )
    
    # Task 2: Binding Affinity Prediction
    affinity_task = Task(
        description=f"""
        Predict binding affinities using molecular properties and ML models:
        
        Toxin-Protein Combinations: {len(proteins)} proteins × {len(toxins)} toxins = {len(proteins) * len(toxins)} interactions
        
        Protein Properties (from protein crew):
        {chr(10).join([f"- {protein}: MW, pI, hydrophobicity, stability" for protein in proteins])}
        
        For each interaction:
        1. Extract molecular descriptors
        2. Apply ML binding affinity models
        3. Consider protein stability effects
        4. Account for hydrophobic/electrostatic contributions
        5. Validate against known data
        
        Use molecular property calculations and ML prediction models.
        Focus on food safety relevant binding strengths.
        """,
        expected_output="Detailed binding affinity predictions with confidence scores and property correlations"
    )
    
    # Task 3: Interaction Type Classification
    classification_task = Task(
        description=f"""
        Classify molecular interaction types and mechanisms:
        
        Interaction Pairs to Classify:
        {chr(10).join([f"- {protein}-{toxin}" for protein in proteins for toxin in toxins])}
        
        Classification Categories:
        1. Competitive inhibition
        2. Allosteric binding
        3. Strong hydrophobic binding
        4. Electrostatic interactions
        5. Hydrogen bonding networks
        6. Weak/non-specific binding
        
        Consider:
        - Binding site types from protein analysis
        - Molecular properties of toxins
        - Known interaction mechanisms from research
        - Food safety implications of each type
        
        Use classify_interaction_type_detailed tool.
        """,
        expected_output="Complete interaction classification with mechanisms and food safety implications"
    )
    
    # Task 4: Structural Change Prediction
    structural_task = Task(
        description=f"""
        Predict protein structural changes upon toxin binding:
        
        Processing Conditions Impact:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Duration: {processing_conditions.get('duration', 60)} minutes
        
        From Protein Stability Data:
        - Base stability scores for each protein
        - pH and temperature sensitivities
        - Processing vulnerabilities
        
        For each binding interaction:
        1. Predict secondary structure changes
        2. Calculate conformational flexibility alterations
        3. Assess overall structural integrity
        4. Consider environmental stress factors
        5. Evaluate functional site impacts
        
        Use predict_structural_changes_binding tool.
        Focus on changes that affect food safety.
        """,
        expected_output="Detailed structural change predictions with processing condition effects"
    )
    
    # Task 5: Toxicity Enhancement Assessment
    toxicity_task = Task(
        description=f"""
        Assess toxicity enhancement due to protein binding:
        
        Toxin Safety Profiles:
        {chr(10).join([f"- {toxin}: LD50, mechanism, regulatory limits" for toxin in toxins])}
        
        Protein Functional Importance:
        {chr(10).join([f"- {protein}: Food function, processing role" for protein in proteins])}
        
        Enhancement Factors to Evaluate:
        1. Bioavailability changes
        2. Target organ concentration
        3. Metabolic pathway alterations
        4. Synergistic toxicity effects
        5. Protective or detoxification impacts
        
        For each interaction:
        - Calculate enhancement factors
        - Assess safety margin changes
        - Predict regulatory implications
        - Recommend safety measures
        
        Use calculate_toxicity_enhancement_factor tool.
        """,
        expected_output="Comprehensive toxicity enhancement assessment with safety recommendations"
    )
    
    # Task 6: Interaction Analysis Integration
    integration_task = Task(
        description="""
        Integrate all interaction prediction results:
        
        Integration Requirements:
        1. Combine docking results with affinity predictions
        2. Correlate interaction types with structural changes
        3. Link toxicity enhancement to binding mechanisms
        4. Identify highest risk interactions
        5. Generate comprehensive interaction profiles
        
        Analysis Goals:
        - Create interaction risk matrix
        - Highlight critical safety concerns
        - Provide mechanistic insights
        - Recommend monitoring strategies
        
        Output Format:
        - Executive summary of interaction analysis
        - Individual interaction profiles
        - Risk ranking of all combinations
        - Processing optimization recommendations
        - Safety monitoring protocols
        """,
        expected_output="Integrated interaction analysis report with comprehensive risk assessment"
    )
    
    return [docking_task, affinity_task, classification_task, structural_task, toxicity_task, integration_task]