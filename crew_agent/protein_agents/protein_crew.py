import numpy as np
from datetime import datetime
from crewai import Task, Agent, Crew, Process
from langchain_ollama import ChatOllama
from protein_tools import analyze_protein_structure, assess_protein_stability_conditions, calculate_processing_sensitivity, predict_functional_sites_pattern
from config import llm

def agents():
    """
    Create protein analysis crew agents
    
    Returns:
        Tuple of protein analysis agents
    """

    # Structure Analysis Agent (replaces ESMFold functionality from ADK)
    structure_analyzer = Agent(
        role="Protein Structure Analyst",
        goal="Analyze protein structures using ESMFold and predict 3D conformations",
        backstory="""You are an expert in protein structural biology with deep knowledge 
        of protein folding, secondary structure prediction, and ESMFold neural networks. 
        You excel at analyzing protein sequences and predicting their 3D structures, 
        binding sites, and conformational properties.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[analyze_protein_structure]
    )
    
    # Property Calculator Agent
    property_calculator = Agent(
        role="Protein Property Calculator",
        goal="Calculate molecular properties and physicochemical characteristics",
        backstory="""You are a biochemist specializing in protein physicochemical properties.
        You can calculate molecular weights, isoelectric points, hydrophobicity indices,
        and other important protein characteristics that affect food safety and processing.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[analyze_protein_structure]
    )
    
    # Stability Assessment Agent
    stability_assessor = Agent(
        role="Protein Stability Assessor", 
        goal="Evaluate protein stability under various processing conditions",
        backstory="""You are a food protein scientist who understands how processing
        conditions affect protein stability. You can predict how temperature, pH,
        ionic strength, and other factors influence protein structure and function.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[assess_protein_stability_conditions, calculate_processing_sensitivity]
    )
    
    # Functional Site Predictor Agent
    functional_predictor = Agent(
        role="Functional Site Predictor",
        goal="Identify and predict functional sites in food proteins",
        backstory="""You are an expert in protein function prediction and site identification.
        You can identify active sites, binding sites, allosteric sites, and other functional
        regions in proteins that are important for food safety and toxin interactions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[predict_functional_sites_pattern]
    )
    
    # Protein Analysis Coordinator Agent
    protein_coordinator = Agent(
        role="Protein Analysis Coordinator",
        goal="Coordinate protein analysis activities and synthesize findings",
        backstory="""You are a senior protein biochemist who coordinates multi-disciplinary
        protein analysis teams. You excel at integrating structural data, property calculations,
        stability assessments, and functional predictions into comprehensive protein profiles.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[]
    )
    
    return structure_analyzer, property_calculator, stability_assessor, functional_predictor, protein_coordinator


def protein_crew():
    """Create protein analysis crew"""
    A, B, C, D, E = agents()
    protein_crew = Crew(
        agents=[A, B, C, D, E],
        process=Process.hierarchical,
        verbose=True,
        manager_llm=llm
    )
    return protein_crew