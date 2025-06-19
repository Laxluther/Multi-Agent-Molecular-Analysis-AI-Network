from enzyme_crew import enzyme_crew
from enzyme_task import enzyme_tasks

# Test the enzyme simulation crew
enzymes_to_analyze = ['amylase', 'protease', 'lipase', 'lysozyme']

processing_conditions = {
    'temperature': 85.0,
    'ph': 6.5,
    'duration': 30,
    'ionic_strength': 0.15
}

# Mock protein analysis results (would come from protein crew)
protein_results = {
    'stability': {
        'amylase': 6.8,
        'protease': 7.2,
        'lipase': 7.8,
        'lysozyme': 9.1
    },
    'structures': {
        'amylase': {'confidence': 0.82, 'active_sites': 2},
        'protease': {'confidence': 0.75, 'active_sites': 1},
        'lipase': {'confidence': 0.88, 'active_sites': 1},
        'lysozyme': {'confidence': 0.95, 'active_sites': 1}
    }
}

# Mock interaction results (would come from interaction crew)
interaction_results = {
    'interactions': [
        {'toxin_name': 'aflatoxin_b1', 'enzyme_name': 'amylase', 'binding_affinity': -6.2},
        {'toxin_name': 'ochratoxin_a', 'enzyme_name': 'protease', 'binding_affinity': -5.8},
        {'toxin_name': 'heavy_metals', 'enzyme_name': 'lipase', 'binding_affinity': -7.1}
    ],
    'binding_summary': 'Multiple strong interactions detected',
    'interaction_types': 'Competitive and non-competitive inhibition',
    'structural_changes': 'Moderate conformational changes predicted'
}

research_context = {
    'enzyme_studies': ['Amylase thermal stability research', 'Protease inhibition by mycotoxins'],
    'literature_findings': 'Heavy metals significantly inhibit food enzymes'
}

crew = enzyme_crew()
tasks = enzyme_tasks(enzymes_to_analyze, processing_conditions, protein_results, interaction_results, research_context)

crew.tasks = tasks
crew.kickoff()