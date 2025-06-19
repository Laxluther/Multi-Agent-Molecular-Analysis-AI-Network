from safety_crew import safe_crew
from safety_task import safety_tasks


analysis_context = {
    'food_sample': {
        'food_type': 'dairy_milk',
        'processing_conditions': {'temperature': 85, 'ph': 6.5}
    },
    'protein_analyses': {
        'casein': {'stability_score': 7.5, 'analysis_confidence': 0.9},
        'whey_protein': {'stability_score': 6.8, 'analysis_confidence': 0.85}
    },
    'interactions': [
        {'toxin_name': 'aflatoxin_b1', 'binding_affinity': -6.5, 'toxicity_enhancement': 2.1, 'confidence_score': 0.8}
    ],
    'detected_compounds': {'aflatoxin_b1': 1.5}  # ppb
}


crew = safe_crew()
tasks = safety_tasks(analysis_context)



crew.tasks = tasks
crew.kickoff()
    
    
