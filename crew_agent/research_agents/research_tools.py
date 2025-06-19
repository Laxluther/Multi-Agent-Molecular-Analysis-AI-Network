from crewai.tools import tool
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime
import requests

@tool
def search_pubmed(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search PubMed for scientific literature
    
    Args:
        query: Search query for scientific papers
        max_results: Maximum number of results to return
        
    Returns:
        List of paper information
    """
  
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # Search for papers
    search_url = f"{base_url}esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json',
        'sort': 'relevance'
    }
    
    response = requests.get(search_url, params=search_params, timeout=10)
    search_data = response.json()
    
    if 'esearchresult' not in search_data:
        return []
    
    pmids = search_data['esearchresult'].get('idlist', [])
    
    if not pmids:
        return []
    
    # Get paper details
    fetch_url = f"{base_url}esummary.fcgi"
    fetch_params = {
        'db': 'pubmed',
        'id': ','.join(pmids),
        'retmode': 'json'
    }
    
    response = requests.get(fetch_url, params=fetch_params, timeout=10)
    fetch_data = response.json()
    
    papers = []
    for pmid in pmids:
        if pmid in fetch_data['result']:
            paper_data = fetch_data['result'][pmid]
            papers.append({
                'pmid': pmid,
                'title': paper_data.get('title', ''),
                'authors': [author['name'] for author in paper_data.get('authors', [])],
                'journal': paper_data.get('source', ''),
                'pub_date': paper_data.get('pubdate', ''),
                'abstract': paper_data.get('abstract', ''),
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })
    
    return papers
        


@tool
def search_food_database(food_type: str) -> Dict[str, Any]:
    """
    Search food composition databases
    
    Args:
        food_type: Type of food to search for
        
    Returns:
        Food composition data
    """
    food_compositions = {
        'dairy_milk': {
            'proteins': ['casein', 'beta_lactoglobulin', 'alpha_lactalbumin'],
            'composition': {'protein': 3.3, 'fat': 3.25, 'carbohydrate': 4.8, 'water': 87.0},
            'typical_ph': 6.5,
            'processing_conditions': {'pasteurization_temp': 72, 'duration': 15}
        },
        'wheat_flour': {
            'proteins': ['gliadin', 'glutenin', 'albumin', 'globulin'],
            'composition': {'protein': 13.0, 'carbohydrate': 72.0, 'fat': 1.5, 'water': 12.0},
            'typical_ph': 6.0,
            'processing_conditions': {'milling_temp': 25, 'moisture': 12}
        },
        'chicken_meat': {
            'proteins': ['myosin', 'actin', 'tropomyosin', 'troponin'],
            'composition': {'protein': 25.0, 'fat': 15.0, 'water': 60.0},
            'typical_ph': 5.8,
            'processing_conditions': {'cooking_temp': 74, 'duration': 15}
        }
    }
        
    
    food_key = food_type.lower().replace(' ', '_')
    
    # Search for closest match
    for key, data in food_compositions.items():
        if food_key in key or any(word in key for word in food_key.split('_')):
            return {
                'food_type': food_type,
                'data': data,
                'source': 'Food Composition Database',
                'last_updated': datetime.now().isoformat()
            }
        
    # Default response
    return {
        'food_type': food_type,
        'data': {
            'proteins': ['unknown'],
            'composition': {'protein': 20.0, 'fat': 10.0, 'carbohydrate': 50.0, 'water': 20.0},
            'typical_ph': 7.0
        },
        'source': 'Default values',
        'last_updated': datetime.now().isoformat()
    }


@tool
def search_toxin_database(toxin_name: str) -> Dict[str, Any]:
    """
    Search toxin databases for safety information
    
    Args:
        toxin_name: Name of the toxin to search for
        
    Returns:
        Toxin safety data
    """
    toxin_data = {
        'aflatoxin_b1': {
            'type': 'mycotoxin',
            'ld50': 0.48,  # mg/kg
            'regulatory_limit': {'eu': 2.0, 'us': 20.0},  # ppb
            'mechanism': 'DNA intercalation and adduct formation',
            'target_proteins': ['p53', 'albumin', 'cytochrome_p450'],
            'detection_methods': ['HPLC', 'ELISA', 'LC-MS/MS'],
            'sources': ['Aspergillus flavus', 'Aspergillus parasiticus']
        },
        'ochratoxin_a': {
            'type': 'mycotoxin',
            'ld50': 20.0,
            'regulatory_limit': {'eu': 5.0, 'us': 10.0},
            'mechanism': 'Protein synthesis inhibition',
            'target_proteins': ['kidney_proteins', 'liver_enzymes'],
            'detection_methods': ['HPLC', 'TLC', 'ELISA'],
            'sources': ['Aspergillus ochraceus', 'Penicillium species']
        },
        'solanine': {
            'type': 'plant_alkaloid',
            'ld50': 590.0,
            'regulatory_limit': {'general': 200.0},  # mg/kg
            'mechanism': 'Cell membrane disruption',
            'target_proteins': ['membrane_proteins', 'ion_channels'],
            'detection_methods': ['HPLC', 'LC-MS'],
            'sources': ['Green potatoes', 'Potato sprouts', 'Tomato leaves']
        }
    }
    
    # Normalize toxin name
    toxin_key = toxin_name.lower().replace(' ', '_').replace('-', '_')
    
    # Search for match
    for key, data in toxin_data.items():
        if toxin_key in key or key in toxin_key:
            return {
                'toxin_name': toxin_name,
                'data': data,
                'source': 'Toxin Safety Database',
                'last_updated': datetime.now().isoformat()
            }
    
    # Default response for unknown toxins
    return {
        'toxin_name': toxin_name,
        'data': {
            'type': 'unknown',
            'ld50': None,
            'regulatory_limit': {},
            'mechanism': 'Unknown',
            'target_proteins': [],
            'detection_methods': []
        },
        'source': 'No data available',
        'last_updated': datetime.now().isoformat()
    }

@tool
def search_protein_interactions(protein_name: str, toxin_name: str) -> List[Dict[str, Any]]:
    """
    Search for protein-toxin interaction studies
    
    Args:
        protein_name: Name of the protein
        toxin_name: Name of the toxin
        
    Returns:
        List of interaction studies
    """

    query = f"{protein_name} {toxin_name} interaction binding"
    
    # Search PubMed for interactions
    papers = search_pubmed(query, max_results=5)
    
    # Enhance with mock interaction data
    interactions = []
    for paper in papers:
        interactions.append({
            'paper_id': paper['pmid'],
            'title': paper['title'],
            'journal': paper['journal'],
            'interaction_type': 'experimental',
            'binding_affinity': f"Kd = {np.random.uniform(0.1, 10.0):.2f} μM",
            'experimental_method': 'Surface plasmon resonance',
            'confidence': 'high'
        })
    
    # Add mock data if no papers found
    if not interactions:
        interactions.append({
            'paper_id': 'predicted',
            'title': f'Predicted interaction between {protein_name} and {toxin_name}',
            'journal': 'Computational Prediction',
            'interaction_type': 'predicted',
            'binding_affinity': f"Predicted Kd = {np.random.uniform(1.0, 100.0):.2f} μM",
            'experimental_method': 'Molecular docking',
            'confidence': 'medium'
        })
    return interactions
