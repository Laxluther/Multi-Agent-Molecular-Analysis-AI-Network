import numpy as np
from datetime import datetime
from crewai import Task, Agent, Crew, Process
from langchain_ollama import ChatOllama
from enzyme_tools import simulate_enzyme_kinetics, predict_enzyme_inhibition, calculate_enzyme_stability
from config import llm

def agents():


    kinetics_simulator = Agent(
        role="Enzyme Kinetics Simulator",
        goal="Simulate enzyme kinetics and calculate Km, Vmax, and kcat parameters",
        backstory="""You are an expert in enzyme biochemistry and kinetics simulation 
        with deep knowledge of Michaelis-Menten kinetics, enzyme mechanisms, and 
        environmental effects on enzyme activity. You excel at calculating kinetic 
        parameters and predicting enzyme behavior under various conditions.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[simulate_enzyme_kinetics]
    )
    
   
    inhibition_analyst = Agent(
        role="Enzyme Inhibition Analyst",
        goal="Analyze enzyme inhibition mechanisms and calculate inhibition constants",
        backstory="""You are a biochemist specializing in enzyme inhibition analysis.
        You understand competitive, non-competitive, and uncompetitive inhibition 
        mechanisms. You can predict how toxins and other compounds affect enzyme 
        activity and calculate Ki values.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[predict_enzyme_inhibition]
    )
    
    # Stability Calculator Agent
    stability_calculator = Agent(
        role="Enzyme Stability Calculator", 
        goal="Calculate enzyme stability and degradation under processing conditions",
        backstory="""You are an expert in enzyme stability and protein degradation
        kinetics. You can predict enzyme half-lives, calculate degradation rates,
        and assess how temperature, pH, and storage conditions affect enzyme
        stability in food systems.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[calculate_enzyme_stability]
    )
    
    # Environmental Effects Specialist Agent
    environmental_specialist = Agent(
        role="Environmental Effects Specialist",
        goal="Assess environmental effects on enzyme activity and stability",
        backstory="""You are an expert in food processing biochemistry who understands
        how temperature, pH, ionic strength, and other environmental factors affect
        enzyme activity. You can predict optimal conditions and processing effects.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[simulate_enzyme_kinetics, calculate_enzyme_stability]
    )
    
    # Enzyme Analysis Coordinator Agent
    enzyme_coordinator = Agent(
        role="Enzyme Analysis Coordinator",
        goal="Coordinate enzyme simulation activities and synthesize findings",
        backstory="""You are a senior enzyme biochemist who coordinates enzyme
        analysis teams. You excel at integrating kinetic simulations, inhibition
        analyses, and stability assessments into comprehensive enzyme profiles
        for food safety applications.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[]
    )
    
    return kinetics_simulator, inhibition_analyst, stability_calculator, environmental_specialist, enzyme_coordinator


def enzyme_crew():
    """Create enzyme simulation crew"""
    A, B, C, D, E = agents()
    enzyme_crew = Crew(
        agents=[A, B, C, D, E],
        process=Process.hierarchical,
        verbose=True,
        manager_llm=llm
    )
    return enzyme_crew