from protein_crew import protein_crew
from protein_task import protein_tasks

# Test the protein analysis crew
proteins_to_analyze = ['casein', 'whey_protein', 'lactalbumin']

processing_conditions = {
    'temperature': 85.0,
    'ph': 6.5,
    'duration': 30,
    'ionic_strength': 0.15
}

research_context = {
    'protein_studies': ['ESMFold accuracy study', 'Dairy protein stability research'],
    'literature_findings': 'Casein shows high thermal stability'
}

crew = protein_crew()
tasks = protein_tasks(proteins_to_analyze, processing_conditions, research_context)

crew.tasks = tasks
crew.kickoff()