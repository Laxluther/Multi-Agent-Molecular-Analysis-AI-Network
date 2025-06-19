import numpy as np
from datetime import datetime
from crewai import Task, Agent, Crew, Process
from langchain_ollama import ChatOllama
from .interaction_tools import predict_toxin_protein_interaction, classify_interaction_type_detailed, predict_structural_changes_binding, calculate_toxicity_enhancement_factor
from config import llm

def agents():

    molecular_docker = Agent(
        role="Molecular Docking Specialist",
        goal="Perform molecular docking simulations using RDKit and predict binding poses",
        backstory="""You are an expert in computational chemistry and molecular docking 
        with deep knowledge of RDKit, binding site identification, and protein-ligand 
        interactions. You excel at predicting how toxin molecules bind to protein targets 
        and can calculate binding affinities and interaction energies.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[predict_toxin_protein_interaction]
    )
    
    # Binding Affinity Predictor Agent
    binding_predictor = Agent(
        role="Binding Affinity Predictor",
        goal="Predict binding affinities using machine learning and molecular properties",
        backstory="""You are a computational biophysicist specializing in protein-ligand
        binding affinity prediction. You understand how molecular properties like molecular
        weight, LogP, hydrogen bonding, and protein characteristics affect binding strength.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[predict_toxin_protein_interaction]
    )
    
    # Interaction Classifier Agent
    interaction_classifier = Agent(
        role="Interaction Type Classifier", 
        goal="Classify types of molecular interactions and binding mechanisms",
        backstory="""You are an expert in molecular interaction classification who can
        identify different types of binding mechanisms: competitive inhibition, allosteric
        binding, hydrophobic interactions, electrostatic interactions, and hydrogen bonding.
        You understand how these affect food safety.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[classify_interaction_type_detailed]
    )
    
    # Structural Change Predictor Agent
    structural_predictor = Agent(
        role="Structural Change Predictor",
        goal="Predict protein structural changes upon toxin binding",
        backstory="""You are a structural biochemist who can predict how protein binding
        affects protein conformation, secondary structure content, and overall stability.
        You understand how environmental conditions influence structural changes.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[predict_structural_changes_binding]
    )
    
    # Toxicity Enhancement Assessor Agent
    toxicity_assessor = Agent(
        role="Toxicity Enhancement Assessor",
        goal="Assess how protein binding enhances or modifies toxicity",
        backstory="""You are a toxicologist who understands how protein-toxin interactions
        can enhance toxicity, alter bioavailability, or change toxin distribution. You can
        predict the safety implications of molecular interactions in food systems.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[calculate_toxicity_enhancement_factor]
    )
    
    # Interaction Analysis Coordinator Agent
    interaction_coordinator = Agent(
        role="Interaction Analysis Coordinator",
        goal="Coordinate interaction prediction activities and synthesize findings",
        backstory="""You are a senior computational toxicologist who coordinates 
        multi-disciplinary interaction prediction teams. You excel at integrating 
        docking results, binding predictions, structural analyses, and toxicity 
        assessments into comprehensive interaction profiles.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[]
    )
    
    return molecular_docker, binding_predictor, interaction_classifier, structural_predictor, toxicity_assessor, interaction_coordinator


def interaction_crew():
    """Create interaction prediction crew"""
    A, B, C, D, E, F = agents()
    interaction_crew = Crew(
        agents=[A, B, C, D, E, F],
        process=Process.hierarchical,
        verbose=True,
        manager_llm=llm
    )
    return interaction_crew