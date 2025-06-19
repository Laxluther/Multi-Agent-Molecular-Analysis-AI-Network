from reporting_crew import report_crew
from reporting_task import reporting_tasks


# Mock analysis context
analysis_context = {
    'safety_assessment': {
        'overall_safety_score': 7.2,
        'risk_level': 'low',
        'component_risks': {
            'interaction_risk': 2.1,
            'protein_stability_risk': 1.5,
            'regulatory_compliance_risk': 0.3
        }
    },
    'protein_analyses': {
        'casein': {'stability_score': 7.5, 'molecular_weight': 24000, 'analysis_confidence': 0.9},
        'whey_protein': {'stability_score': 6.8, 'molecular_weight': 18400, 'analysis_confidence': 0.85}
    },
    'interactions': [
        {'toxin_name': 'aflatoxin_b1', 'protein_name': 'casein', 'binding_affinity': -6.5, 'risk_score': 6.2}
    ],
    'regulatory_compliance': {
        'overall_status': 'compliant_with_warnings',
        'warnings': [{'compound': 'aflatoxin_b1', 'percentage_of_limit': 85}]
    }
}


crew = report_crew()
tasks = reporting_tasks(analysis_context)



crew.tasks = tasks
crew.kickoff()
    
    
