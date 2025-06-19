import numpy as np
from datetime import datetime
from crewai import Task,Agent,Crew,Process
from langchain_ollama import ChatOllama
from .reporting_tools import executive_summary,format_technical_results,generate_recommendations_section,generate_charts_data,compile_complete_report
from config import llm

def agents():
    """
    Create report generation crew
    
    Args:
        ollama_base_url: Base URL for Ollama server
        
    Returns:
        Configured CrewAI crew for reporting
    """
    
    # Technical Writer Agent
    technical_writer = Agent(
        role="Technical Documentation Specialist",
        goal="Create clear, comprehensive technical documentation from complex analysis results",
        backstory="""You are an expert technical writer specializing in food science and safety 
        documentation. You excel at translating complex molecular analysis data into clear, 
        professional reports that meet regulatory and industry standards.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[format_technical_results, generate_charts_data]
    )
    
    # Executive Communicator Agent
    executive_communicator = Agent(
        role="Executive Communications Specialist",
        goal="Create executive-level summaries and strategic recommendations",
        backstory="""You are a senior communications professional who specializes in 
        executive-level reporting for food safety and regulatory affairs. You can distill 
        complex technical findings into actionable business insights and strategic recommendations.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[executive_summary, generate_recommendations_section]
    )
    
    # Regulatory Documentation Agent
    regulatory_writer = Agent(
        role="Regulatory Documentation Specialist",
        goal="Ensure compliance documentation meets regulatory standards and requirements",
        backstory="""You are a regulatory affairs specialist with deep knowledge of food safety 
        documentation requirements. You understand FDA, EFSA, and international standards for 
        food safety reporting and can ensure all documentation meets regulatory expectations.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[generate_recommendations_section]
    )
    
    # Report Coordinator Agent
    report_coordinator = Agent(
        role="Report Coordination Manager",
        goal="Coordinate report generation and ensure quality and completeness",
        backstory="""You are a documentation manager who coordinates technical writing teams 
        and ensures report quality, consistency, and completeness. You understand the needs 
        of different stakeholders and can manage complex documentation projects.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[compile_complete_report]
    )

    return [technical_writer, executive_communicator, regulatory_writer, report_coordinator]


def report_crew():
    A,B,C,D = agents()
    report_crew = Crew(
    agents = [A,B,C,D],
    process= Process.hierarchical,
    verbose = True,
    manager_llm=llm
    )
    return report_crew