from typing import List, Dict, Any, Optional
from crewai import Task
from enzyme_crew import agents

A, B, C, D, E = agents()

def enzyme_tasks(enzymes: List[str], processing_conditions: Dict[str, Any],
                protein_results: Dict[str, Any], interaction_results: Dict[str, Any],
                research_context: Dict[str, Any] = None) -> List[Task]:
    """
    Create enzyme simulation tasks
    
    Args:
        enzymes: List of enzyme names to analyze
        processing_conditions: Processing conditions
        protein_results: Results from protein analysis crew
        interaction_results: Results from interaction prediction crew
        research_context: Research findings from research crew
        
    Returns:
        List of enzyme simulation tasks
    """
    
    if research_context is None:
        research_context = {}
    
    # Extract inhibitors from interaction results
    inhibitors = []
    if interaction_results and 'interactions' in interaction_results:
        for interaction in interaction_results['interactions']:
            if interaction.get('binding_affinity', 0) < -5.0:  # Strong binding
                inhibitors.append(interaction.get('toxin_name', ''))
    
    # Task 1: Enzyme Kinetics Simulation
    kinetics_task = Task(
        description=f"""
        Simulate enzyme kinetics using Michaelis-Menten equations:
        
        Enzymes to analyze: {', '.join(enzymes)}
        
        Processing Conditions:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Duration: {processing_conditions.get('duration', 60)} minutes
        - Ionic Strength: {processing_conditions.get('ionic_strength', 0.15)}M
        
        From Protein Analysis:
        - Protein stability data: {protein_results.get('stability', 'Available')}
        - Structural information: {protein_results.get('structures', 'Available')}
        
        From Interaction Analysis:
        - Potential inhibitors: {', '.join(inhibitors) if inhibitors else 'None detected'}
        
        For each enzyme:
        1. Calculate Km (Michaelis constant)
        2. Determine Vmax (maximum velocity)
        3. Calculate kcat (catalytic constant)
        4. Apply temperature and pH corrections
        5. Account for ionic strength effects
        6. Consider substrate availability
        
        Use simulate_enzyme_kinetics tool for each enzyme.
        Focus on food processing relevant substrates.
        """,
        expected_output="Comprehensive enzyme kinetics simulation with Km, Vmax, and kcat values under processing conditions"
    )
    
    # Task 2: Inhibition Analysis
    inhibition_task = Task(
        description=f"""
        Analyze enzyme inhibition by toxins and other compounds:
        
        Enzyme-Inhibitor Combinations:
        {chr(10).join([f"- {enzyme} vs {inhibitor}" for enzyme in enzymes for inhibitor in inhibitors])}
        
        From Interaction Results:
        - Binding affinities: {interaction_results.get('binding_summary', 'Available')}
        - Interaction types: {interaction_results.get('interaction_types', 'Classified')}
        - Structural changes: {interaction_results.get('structural_changes', 'Predicted')}
        
        Processing Context:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Inhibitor concentrations: Variable (food relevant levels)
        
        For each enzyme-inhibitor pair:
        1. Determine inhibition mechanism (competitive/non-competitive/uncompetitive)
        2. Calculate inhibition constant (Ki)
        3. Predict percent activity reduction
        4. Assess concentration-dependent effects
        5. Consider processing condition influences
        
        Use predict_enzyme_inhibition tool.
        Focus on food safety relevant inhibition levels.
        """,
        expected_output="Detailed enzyme inhibition analysis with Ki values, mechanisms, and activity reduction predictions"
    )
    
    # Task 3: Enzyme Stability Assessment
    stability_task = Task(
        description=f"""
        Calculate enzyme stability under processing and storage conditions:
        
        Enzymes: {', '.join(enzymes)}
        
        Processing Conditions:
        - Temperature: {processing_conditions.get('temperature', 25)}°C
        - pH: {processing_conditions.get('ph', 7.0)}
        - Duration: {processing_conditions.get('duration', 60)} minutes
        
        Storage Conditions to Test:
        - Refrigeration: 4°C, pH 7.0
        - Room temperature: 25°C, pH 7.0
        - Processing temperature: {processing_conditions.get('temperature', 25)}°C
        
        Time Points for Analysis:
        - Short term: 1, 6, 12, 24 hours
        - Medium term: 48, 72, 168 hours (1 week)
        - Long term: 336, 720 hours (1 month)
        
        For each enzyme:
        1. Calculate degradation rate constants
        2. Predict half-life under each condition
        3. Determine stability classification
        4. Assess activity retention over time
        5. Identify critical stability factors
        
        Use calculate_enzyme_stability tool.
        """,
        expected_output="Comprehensive enzyme stability assessment with half-lives, degradation rates, and stability classifications"
    )
    
    # Task 4: Environmental Effects Analysis
    environmental_task = Task(
        description=f"""
        Analyze environmental effects on enzyme activity:
        
        Environmental Variables:
        - Temperature range: 4°C to {processing_conditions.get('temperature', 25) + 20}°C
        - pH range: 4.0 to 10.0
        - Ionic strength: 0.05M to 0.5M
        - Processing duration effects
        
        From Research Context: {research_context.get('enzyme_studies', 'Limited data available')}
        
        Analysis Requirements:
        1. Temperature-activity relationships (Q10 effects)
        2. pH profile optimization
        3. Salt concentration effects
        4. Processing time impacts
        5. Optimal condition identification
        6. Processing window determination
        
        For each enzyme:
        - Map activity profiles across conditions
        - Identify optimal operating ranges
        - Predict processing effects
        - Recommend condition optimization
        - Assess food safety implications
        
        Use both kinetics and stability tools.
        """,
        expected_output="Environmental effects analysis with optimal conditions and processing recommendations"
    )
    
    # Task 5: Enzyme Activity Integration
    integration_task = Task(
        description="""
        Integrate all enzyme simulation results:
        
        Integration Requirements:
        1. Combine kinetics with inhibition data
        2. Correlate stability with activity profiles
        3. Link environmental effects to processing conditions
        4. Assess overall enzyme performance
        5. Generate enzyme-specific recommendations
        
        Analysis Goals:
        - Create comprehensive enzyme profiles
        - Identify high-risk enzyme activities
        - Optimize processing conditions
        - Predict food safety impacts
        - Recommend monitoring strategies
        
        Output Format:
        - Executive summary of enzyme analysis
        - Individual enzyme activity profiles
        - Processing optimization recommendations
        - Food safety risk assessment
        - Quality control protocols
        
        Consider:
        - Enzyme interactions with toxins
        - Processing condition optimization
        - Food safety monitoring needs
        - Quality preservation strategies
        """,
        expected_output="Integrated enzyme analysis report with comprehensive activity profiles and processing recommendations"
    )
    
    return [kinetics_task, inhibition_task, stability_task, environmental_task, integration_task]