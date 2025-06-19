from research_crew import researcher_crew
from research_task import research_tasks


food_sample = {
        'food_type': 'dairy_milk',
        'proteins': ['casein', 'whey_protein'],
        'suspected_toxins': ['aflatoxin_b1', 'ochratoxin_a']
    }
    
protein_analyses = {
    'casein': {'stability_score': 7.5},
    'whey_protein': {'stability_score': 6.8}
}


crew = researcher_crew()
tasks = research_tasks(food_sample, protein_analyses)



crew.tasks = tasks
crew.kickoff()
    
    
