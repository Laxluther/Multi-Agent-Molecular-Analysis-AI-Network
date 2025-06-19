from typing import List, Dict, Any, Optional
from crewai import Task
from langchain_ollama import ChatOllama
from reporting_crew import agents

from config import llm

A, B, C, D = agents()
        
def reporting_tasks(analysis_context: Dict[str, Any]) -> List[Task]:
    """
    Create report generation tasks
    
    Args:
        analysis_context: Complete analysis results
        
    Returns:
        List of reporting tasks
    """
    
    # Task 1: Executive Summary
    executive_task = Task(
        description=f"""
        Generate executive summary for food safety analysis:
        
        Analysis Results Overview:
        - Safety Score: {analysis_context.get('safety_assessment', {}).get('overall_safety_score', 'TBD')}
        - Risk Level: {analysis_context.get('safety_assessment', {}).get('risk_level', 'TBD')}
        - Proteins Analyzed: {len(analysis_context.get('protein_analyses', {}))}
        - Interactions Assessed: {len(analysis_context.get('interactions', []))}
        
        Requirements:
        1. Create compelling executive summary
        2. Highlight key findings and risks
        3. Provide clear action items
        4. Maintain professional tone
        5. Focus on business implications
        
        Target Audience: Senior management and decision makers
        """,
        expected_output="Professional executive summary with key findings and strategic recommendations"
    )
    
    # Task 2: Technical Documentation
    technical_task = Task(
        description="""
        Format technical analysis results for professional presentation:
        
        Content Requirements:
        1. Protein structure analysis section
        2. Toxin-protein interaction analysis
        3. Enzyme kinetics results
        4. Technical methodology description
        5. Data tables and summaries
        
        Formatting Requirements:
        - Use markdown formatting
        - Include data tables
        - Provide clear section headers
        - Maintain scientific accuracy
        
        Target Audience: Food scientists and technical professionals
        """,
        expected_output="Comprehensive technical documentation with formatted data presentations"
    )
    
    # Task 3: Regulatory Compliance Documentation
    regulatory_task = Task(
        description="""
        Generate regulatory compliance documentation:
        
        Documentation Requirements:
        1. Compliance status assessment
        2. Regulatory recommendations
        3. Action plans for violations
        4. Implementation timelines
        5. Responsible party assignments
        
        Regulatory Standards:
        - FDA regulations (US market)
        - EU regulations (European market)
        - HACCP compliance
        - Good Manufacturing Practices
        
        Target Audience: Regulatory affairs and quality assurance teams
        """,
        expected_output="Regulatory compliance documentation with specific actions and timelines"
    )
    
    # Task 4: Complete Report Compilation
    compilation_task = Task(
        description="""
        Compile complete professional food safety report:
        
        Report Components:
        1. Executive summary
        2. Technical analysis sections
        3. Regulatory recommendations
        4. Methodology and confidence assessment
        5. Appendices and references
        
        Quality Requirements:
        - Professional formatting
        - Consistent style and tone
        - Complete documentation
        - Ready for stakeholder distribution
        
        Final Product: Complete food safety analysis report
        """,
        expected_output="Complete, professional food safety analysis report ready for distribution"
    )
    
    return [executive_task, technical_task, regulatory_task, compilation_task]