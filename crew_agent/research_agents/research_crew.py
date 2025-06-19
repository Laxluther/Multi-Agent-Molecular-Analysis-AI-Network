import numpy as np
from datetime import datetime
from crewai import Task,Agent,Crew,Process
from langchain_ollama import ChatOllama
from .research_tools import search_pubmed, search_food_database, search_toxin_database, search_protein_interactions
from config import llm

def agents():
    """
    Create research coordination crew
    
    Args:
        ollama_base_url: Base URL for Ollama server
        
    Returns:
        Configured CrewAI crew for research
    """

    literature_researcher = Agent(
        role="Literature Researcher",
        goal="Find and analyze relevant scientific literature for food safety research",
        backstory="""You are an expert in scientific literature research with deep knowledge 
        of food science, toxicology, and protein biochemistry. You excel at finding relevant 
        studies, extracting key information, and identifying research gaps.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[search_pubmed]
    )
    
    # Database Specialist Agent
    database_specialist = Agent(
        role="Database Specialist",
        goal="Extract comprehensive data from food and toxin databases",
        backstory="""You are a data specialist with expertise in food composition databases,
        toxin safety databases, and regulatory information systems. You know how to find
        accurate, up-to-date information about food components and safety limits.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_food_database, search_toxin_database]
    )
    
    # Interaction Analyst Agent
    interaction_analyst = Agent(
        role="Interaction Analyst", 
        goal="Analyze protein-toxin interactions and their safety implications",
        backstory="""You are a biochemist specializing in protein-small molecule interactions.
        You understand binding mechanisms, structure-activity relationships, and can predict
        the safety implications of molecular interactions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_protein_interactions, search_pubmed]
    )
    
    # Research Coordinator Agent
    research_coordinator = Agent(
        role="Research Coordinator",
        goal="Coordinate research activities and synthesize findings",
        backstory="""You are a senior food safety researcher who coordinates multi-disciplinary
        research teams. You excel at integrating findings from different sources, identifying
        critical knowledge gaps, and prioritizing research needs.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[]
    )
    
    
    

    return literature_researcher, database_specialist,interaction_analyst,research_coordinator


def researcher_crew():
    A,B,C,D = agents()
    researcher_crew = Crew(
    agents = [A,B,C,D],
    process= Process.hierarchical,
    verbose = True,
    manager_llm=llm
    )
    return researcher_crew