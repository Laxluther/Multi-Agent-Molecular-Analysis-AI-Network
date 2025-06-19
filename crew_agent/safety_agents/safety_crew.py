
import numpy as np
from datetime import datetime
from crewai import Task,Agent,Crew,Process
from langchain_ollama import ChatOllama
from .safety_tools import safety_score,assess_critical_control_points,assess_regulatory_compliance,safety_recommendations
from config import llm
def agents():
    
    risk_assessor = Agent(
        role="Risk Assessment Specialist",
        goal="Evaluate food safety risks from molecular interactions and processing conditions",
        backstory="""You are a food safety expert with deep knowledge of toxicology, 
        protein biochemistry, and risk assessment methodologies. You specialize in 
        quantitative risk analysis and can translate complex molecular data into 
        actionable safety assessments.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[safety_score, assess_critical_control_points]
    )

    compliance_specialist = Agent(
        role="Regulatory Compliance Specialist",
        goal="Ensure food products meet regulatory standards and safety requirements",
        backstory="""You are a regulatory affairs expert with comprehensive knowledge 
        of food safety regulations across different countries. You understand FDA, 
        EFSA, and other regulatory frameworks, and can assess compliance status and 
        provide guidance on regulatory requirements.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[assess_regulatory_compliance]
    )

    haccp_specialist = Agent(
        role="HACCP System Specialist",
        goal="Implement and optimize Hazard Analysis Critical Control Points systems",
        backstory="""You are a HACCP expert with extensive experience in food safety 
        management systems. You can identify critical control points, establish 
        monitoring procedures, and design corrective actions to ensure food safety.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[assess_critical_control_points, safety_recommendations]
    )

    safety_coordinator = Agent(
        role="Food Safety Coordinator",
        goal="Coordinate safety assessments and provide comprehensive safety recommendations",
        backstory="""You are a senior food safety manager who coordinates 
        multi-disciplinary safety teams. You excel at integrating technical 
        assessments with practical implementation strategies and can communicate 
        complex safety concepts to various stakeholders.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        tools=[safety_recommendations]
    )
    
    return risk_assessor, compliance_specialist, haccp_specialist, safety_coordinator


def safe_crew():
    A,B,C,D = agents()
    safety_crew = Crew(
    agents = [A,B,C,D],
    process= Process.hierarchical,
    verbose = True,
    manager_llm=llm
    )
    return safety_crew