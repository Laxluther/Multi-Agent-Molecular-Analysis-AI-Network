from typing import List, Dict, Any, Optional
from crewai import Task
from langchain_ollama import ChatOllama
from .research_crew import agents

from config import llm

A, B, C, D = agents()


def research_tasks(food_sample: Dict[str, Any], 
                        protein_analyses: Dict[str, Any]) -> List[Task]:
    """
    Create research tasks for the crew
    
    Args:
        food_sample: Food sample information
        protein_analyses: Protein analysis results
        
    Returns:
        List of research tasks
    """
    
    # Task 1: Literature Review
    literature_task = Task(
        description=f"""
        Conduct a comprehensive literature review for food safety analysis:
        
        Food Information:
        - Type: {food_sample.get('food_type', 'Unknown')}
        - Proteins: {', '.join(food_sample.get('proteins', []))}
        - Suspected toxins: {', '.join(food_sample.get('suspected_toxins', []))}
        
        Research Requirements:
        1. Find recent studies (last 5 years) on food safety for this food type
        2. Search for protein-toxin interaction studies
        3. Identify regulatory guidelines and safety limits
        4. Look for processing methods that reduce toxin risks
        5. Find detection and analysis methods
        
        Deliverable: Comprehensive literature review with at least 15 relevant studies
        """,
        expected_output="Detailed literature review with study summaries, key findings, and references"
    )
    
    # Task 2: Database Research
    database_task = Task(
        description=f"""
        Extract comprehensive data from databases:
        
        Data Requirements:
        1. Food composition data for {food_sample.get('food_type', 'Unknown')}
        2. Toxin safety data for each suspected toxin: {', '.join(food_sample.get('suspected_toxins', []))}
        3. Regulatory limits and guidelines
        4. Detection methods and sensitivity
        5. Processing effects on toxin levels
        
        Deliverable: Structured database with all relevant safety information
        """,
        expected_output="Complete database report with food composition, toxin data, and regulatory information"
    )
    
    # Task 3: Interaction Analysis
    interaction_task = Task(
        description=f"""
        Analyze protein-toxin interactions:
        
        Proteins to analyze: {', '.join(protein_analyses.keys())}
        Toxins to analyze: {', '.join(food_sample.get('suspected_toxins', []))}
        
        Analysis Requirements:
        1. Find experimental binding data for each protein-toxin pair
        2. Identify binding mechanisms and affinities
        3. Assess structural impacts of binding
        4. Evaluate functional consequences
        5. Predict safety implications
        
        Deliverable: Interaction analysis report with binding data and safety assessment
        """,
        expected_output="Detailed interaction analysis with binding affinities, mechanisms, and safety implications"
    )
    
    # Task 4: Research Synthesis
    synthesis_task = Task(
        description="""
        Synthesize all research findings:
        
        Integration Requirements:
        1. Combine literature findings with database data
        2. Integrate interaction analysis results
        3. Identify key safety concerns and knowledge gaps
        4. Provide evidence-based recommendations
        5. Assess confidence levels for each finding
        
        Deliverable: Integrated research report with executive summary
        """,
        expected_output="Comprehensive research synthesis with key findings, recommendations, and confidence assessments"
    )
    
    return [literature_task, database_task, interaction_task, synthesis_task]