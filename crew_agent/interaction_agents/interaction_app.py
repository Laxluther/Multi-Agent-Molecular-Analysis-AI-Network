from interaction_crew import interaction_crew
from interaction_task import interaction_tasks

# Test the interaction prediction crew
proteins_to_analyze = ['casein', 'whey_protein', 'albumin']
toxins_to_analyze = ['aflatoxin_b1', 'ochratoxin_a', 'fumonisin_b1']

# Mock protein analysis results (would come from protein crew)
protein_results = {
    'structures': {
        'casein': {'confidence': 0.85, 'binding_sites': 3},
        'whey_protein': {'confidence': 0.78, 'binding_sites': 2},
        'albumin': {'confidence': 0.92, 'binding_sites': 4}
    },
    'stability': {
        'casein': 7.5,
        'whey_protein': 6.8,
        'albumin': 8.2
    },
    'binding_sites': {
        'casein': [{'position': 45, 'type': 'hydrophobic'}, {'position': 123, 'type': 'electrostatic'}],
        'whey_protein': [{'position': 25, 'type': 'hydrogen_bond'}],
        'albumin': [{'position': 67, 'type': 'hydrophobic'}, {'position': 89, 'type': 'allosteric'}]
    }
}

processing_conditions = {
    'temperature': 85.0,
    'ph': 6.5,
    'duration': 30,
    'ionic_strength': 0.15
}

research_context = {
    'known_interactions': ['Aflatoxin B1-albumin binding well documented', 'Ochratoxin A-protein interactions studied'],
    'literature_affinities': {'aflatoxin_b1-albumin': -7.2, 'ochratoxin_a-albumin': -6.5}
}

crew = interaction_crew()
tasks = interaction_tasks(proteins_to_analyze, toxins_to_analyze, protein_results, processing_conditions, research_context)

crew.tasks = tasks
crew.kickoff()