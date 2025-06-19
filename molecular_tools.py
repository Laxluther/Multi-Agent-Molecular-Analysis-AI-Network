"""
Molecular Analysis Tools
Comprehensive toolkit for food safety molecular analysis
"""


import json
import csv
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import numpy as np
import pandas as pd


from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem


from data_models import ToxinProfile, ProteinType, ToxinType, COMMON_FOOD_TOXINS, COMMON_FOOD_PROTEINS


class MolecularToolkit:
    """
    Comprehensive molecular analysis toolkit for food safety
    """
    
    def __init__(self):
        self.protein_database = self._load_protein_database()
        self.toxin_database = self._load_toxin_database()
        self.regulatory_database = self._load_regulatory_database()
        self.interaction_database = self._load_interaction_database()
        
    
    def _load_protein_database(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive protein database"""
        proteins = COMMON_FOOD_PROTEINS.copy()
        
        # Add more food proteins
        additional_proteins = {
            'albumin': {
                'name': 'Serum Albumin',
                'type': ProteinType.MEAT,
                'sequence': 'MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYL...',
                'molecular_weight': 66430.0,
                'isoelectric_point': 4.7,
                'function': 'Transport protein'
            },
            'myosin': {
                'name': 'Myosin Heavy Chain',
                'type': ProteinType.MEAT,
                'sequence': 'MAEKMKDTNNIELSSFISRLKERKFKERNKDKDKEKLNDIAFNLKKE...',
                'molecular_weight': 223000.0,
                'isoelectric_point': 5.4,
                'function': 'Motor protein'
            },
            'amylase': {
                'name': 'Alpha-Amylase',
                'type': ProteinType.ENZYME,
                'sequence': 'MFKKFLFLGLSGLAMGAAADVVVNHPEHYVKQTGNKWVMVRELLVDSP...',
                'molecular_weight': 56000.0,
                'isoelectric_point': 6.8,
                'function': 'Starch hydrolysis'
            },
            'lysozyme': {
                'name': 'Lysozyme',
                'type': ProteinType.DAIRY,
                'sequence': 'KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNT...',
                'molecular_weight': 14300.0,
                'isoelectric_point': 11.35,
                'function': 'Antimicrobial enzyme'
            },
            'pepsin': {
                'name': 'Pepsin',
                'type': ProteinType.ENZYME,
                'sequence': 'IGDEPLENYLDTEYFGTIGIGTPAQDFTVIFDTGSSNLWVPSIHCKGR...',
                'molecular_weight': 34600.0,
                'isoelectric_point': 1.5,
                'function': 'Protein digestion'
            }
        }
        
        proteins.update(additional_proteins)
        return proteins
    
    def _load_toxin_database(self) -> Dict[str, ToxinProfile]:
        """Load comprehensive toxin database"""
        toxins = COMMON_FOOD_TOXINS.copy()
        
        # Add more food toxins
        additional_toxins = {
            'fumonisin_b1': ToxinProfile(
                toxin_name='Fumonisin B1',
                toxin_type=ToxinType.MYCOTOXIN,
                molecular_formula='C34H59NO15',
                molecular_weight=721.84,
                structure_smiles='CCCCCCCCCCCCCC[C@@H](O)[C@H](N)C(=O)O',
                ld50=100.0,
                regulatory_limit=4000.0,
                mechanism_of_action='Sphingolipid synthesis disruption'
            ),
            'deoxynivalenol': ToxinProfile(
                toxin_name='Deoxynivalenol (DON)',
                toxin_type=ToxinType.MYCOTOXIN,
                molecular_formula='C15H20O6',
                molecular_weight=296.32,
                ld50=70.0,
                regulatory_limit=1000.0,
                mechanism_of_action='Protein synthesis inhibition'
            ),
            'patulin': ToxinProfile(
                toxin_name='Patulin',
                toxin_type=ToxinType.MYCOTOXIN,
                molecular_formula='C7H6O4',
                molecular_weight=154.12,
                ld50=55.0,
                regulatory_limit=50.0,
                mechanism_of_action='Cellular enzyme inhibition'
            ),
            'ricin': ToxinProfile(
                toxin_name='Ricin',
                toxin_type=ToxinType.PLANT,
                molecular_formula='Variable',
                molecular_weight=60000.0,
                ld50=0.002,
                regulatory_limit=0.0,
                mechanism_of_action='Ribosome inactivation'
            ),
            'saxitoxin': ToxinProfile(
                toxin_name='Saxitoxin',
                toxin_type=ToxinType.MARINE,
                molecular_formula='C10H17N7O4',
                molecular_weight=299.29,
                ld50=0.01,
                regulatory_limit=0.8,
                mechanism_of_action='Sodium channel blockade'
            )
        }
        
        toxins.update(additional_toxins)
        return toxins
    
    def _load_regulatory_database(self) -> Dict[str, Dict[str, Any]]:
        """Load regulatory limits and guidelines"""
        return {
            'us_fda': {
                'aflatoxin_total': {'limit': 20.0, 'unit': 'ppb', 'food_type': 'general'},
                'aflatoxin_b1': {'limit': 20.0, 'unit': 'ppb', 'food_type': 'general'},
                'ochratoxin_a': {'limit': 10.0, 'unit': 'ppb', 'food_type': 'general'},
                'fumonisin': {'limit': 4000.0, 'unit': 'ppb', 'food_type': 'corn'},
                'deoxynivalenol': {'limit': 1000.0, 'unit': 'ppb', 'food_type': 'wheat'},
                'patulin': {'limit': 50.0, 'unit': 'ppb', 'food_type': 'apple_products'}
            },
            'eu_efsa': {
                'aflatoxin_total': {'limit': 4.0, 'unit': 'ppb', 'food_type': 'general'},
                'aflatoxin_b1': {'limit': 2.0, 'unit': 'ppb', 'food_type': 'general'},
                'ochratoxin_a': {'limit': 5.0, 'unit': 'ppb', 'food_type': 'general'},
                'fumonisin': {'limit': 1000.0, 'unit': 'ppb', 'food_type': 'corn'},
                'deoxynivalenol': {'limit': 750.0, 'unit': 'ppb', 'food_type': 'cereals'},
                'patulin': {'limit': 25.0, 'unit': 'ppb', 'food_type': 'apple_products'}
            },
            'codex_alimentarius': {
                'aflatoxin_total': {'limit': 10.0, 'unit': 'ppb', 'food_type': 'general'},
                'ochratoxin_a': {'limit': 5.0, 'unit': 'ppb', 'food_type': 'general'},
                'fumonisin': {'limit': 2000.0, 'unit': 'ppb', 'food_type': 'corn'},
                'deoxynivalenol': {'limit': 1000.0, 'unit': 'ppb', 'food_type': 'cereals'}
            }
        }
    
    def _load_interaction_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load known molecular interactions"""
        return {
            'aflatoxin_b1': [
                {
                    'target_protein': 'albumin',
                    'binding_site': 'Sudlow site I',
                    'binding_affinity': -7.2,
                    'interaction_type': 'hydrophobic',
                    'literature_pmid': '12345678'
                },
                {
                    'target_protein': 'p53',
                    'binding_site': 'DNA binding domain',
                    'binding_affinity': -6.8,
                    'interaction_type': 'covalent',
                    'literature_pmid': '87654321'
                }
            ],
            'ochratoxin_a': [
                {
                    'target_protein': 'albumin',
                    'binding_site': 'Sudlow site II',
                    'binding_affinity': -6.5,
                    'interaction_type': 'hydrogen_bonding',
                    'literature_pmid': '11223344'
                }
            ]
        }
    
    def get_protein_sequence(self, protein_name: str) -> str:
        """Get protein sequence from database"""
        protein_data = self.protein_database.get(protein_name.lower())
        if protein_data:
            return protein_data.get('sequence', '')
        return ''
    
    def get_protein_info(self, protein_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive protein information"""
        return self.protein_database.get(protein_name.lower())
    
    def get_toxin_profile(self, toxin_name: str) -> Optional[ToxinProfile]:
        """Get toxin profile from database"""
        return self.toxin_database.get(toxin_name.lower())
    
    def get_regulatory_limits(self, region: str = 'us_fda') -> Dict[str, Dict[str, Any]]:
        """Get regulatory limits for specified region"""
        return self.regulatory_database.get(region, {})
    
    def calculate_molecular_properties(self, smiles: str) -> Dict[str, float]:
        """
        Calculate molecular properties from SMILES string
        
        Args:
            smiles: SMILES representation of molecule
            
        Returns:
            Dictionary of molecular properties
        """

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return self._mock_molecular_properties()
        
        properties = {
            'molecular_weight': Descriptors.MolWt(mol),
            'logp': Descriptors.MolLogP(mol),
            'hbd': Descriptors.NumHDonors(mol),
            'hba': Descriptors.NumHAcceptors(mol),
            'rotatable_bonds': Descriptors.NumRotatableBonds(mol),
            'aromatic_rings': Descriptors.NumAromaticRings(mol),
            'tpsa': Descriptors.TPSA(mol),
            'heavy_atoms': Descriptors.HeavyAtomCount(mol),
            'formal_charge': Chem.rdmolops.GetFormalCharge(mol),
            'lipinski_hbd': Descriptors.NumHDonors(mol) <= 5,
            'lipinski_hba': Descriptors.NumHAcceptors(mol) <= 10,
            'lipinski_mw': Descriptors.MolWt(mol) <= 500,
            'lipinski_logp': Descriptors.MolLogP(mol) <= 5
        }
        
        # Calculate Lipinski's Rule of Five compliance
        properties['lipinski_violations'] = sum([
            not properties['lipinski_hbd'],
            not properties['lipinski_hba'],
            not properties['lipinski_mw'],
            not properties['lipinski_logp']
        ])
        
        return properties
            
        
    
    def _mock_molecular_properties(self) -> Dict[str, float]:
        """Generate mock molecular properties when RDKit is unavailable"""
        return {
            'molecular_weight': np.random.uniform(200, 800),
            'logp': np.random.uniform(-2, 6),
            'hbd': np.random.randint(0, 8),
            'hba': np.random.randint(2, 12),
            'rotatable_bonds': np.random.randint(0, 15),
            'aromatic_rings': np.random.randint(0, 4),
            'tpsa': np.random.uniform(20, 200),
            'heavy_atoms': np.random.randint(10, 50),
            'formal_charge': 0,
            'lipinski_violations': np.random.randint(0, 3)
        }
    
    def predict_protein_toxin_interaction_risk(self, protein_name: str, 
                                             toxin_name: str) -> Dict[str, Any]:
        """
        Predict interaction risk between protein and toxin
        
        Args:
            protein_name: Name of target protein
            toxin_name: Name of toxin
            
        Returns:
            Risk assessment dictionary
        """
        protein_info = self.get_protein_info(protein_name)
        toxin_profile = self.get_toxin_profile(toxin_name)
        
        if not protein_info or not toxin_profile:
            return {
                'risk_level': 'unknown',
                'confidence': 0.0,
                'reason': 'Insufficient data'
            }
        
        # Check for known interactions
        known_interactions = self.interaction_database.get(toxin_name.lower(), [])
        known_interaction = None
        for interaction in known_interactions:
            if interaction['target_protein'].lower() == protein_name.lower():
                known_interaction = interaction
                break
        
        if known_interaction:
            binding_affinity = abs(known_interaction['binding_affinity'])
            if binding_affinity > 7.0:
                risk_level = 'high'
            elif binding_affinity > 5.0:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'risk_level': risk_level,
                'confidence': 0.9,
                'binding_affinity': known_interaction['binding_affinity'],
                'interaction_type': known_interaction['interaction_type'],
                'literature_support': True,
                'pmid': known_interaction.get('literature_pmid')
            }
        
        # Predict based on properties
        toxin_potency = self._assess_toxin_potency(toxin_profile)
        protein_vulnerability = self._assess_protein_vulnerability(protein_info)
   
        risk_score = (toxin_potency + protein_vulnerability) / 2
        
        if risk_score > 0.7:
            risk_level = 'high'
        elif risk_score > 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'confidence': 0.6,
            'predicted_risk_score': risk_score,
            'toxin_potency': toxin_potency,
            'protein_vulnerability': protein_vulnerability,
            'literature_support': False
        }
    
    def _assess_toxin_potency(self, toxin_profile: ToxinProfile) -> float:
        """Assess toxin potency (0-1 scale)"""
        if toxin_profile.ld50 is None:
            return 0.5  # Default moderate potency
        
        # Log scale transformation (lower LD50 = higher potency)
        if toxin_profile.ld50 <= 0.01:
            return 1.0  # Extremely potent
        elif toxin_profile.ld50 <= 1.0:
            return 0.8  # Highly potent
        elif toxin_profile.ld50 <= 100.0:
            return 0.6  # Moderately potent
        elif toxin_profile.ld50 <= 1000.0:
            return 0.4  # Low potency
        else:
            return 0.2  # Very low potency
    
    def _assess_protein_vulnerability(self, protein_info: Dict[str, Any]) -> float:
        """Assess protein vulnerability to toxin binding (0-1 scale)"""
        vulnerability = 0.5  # Base vulnerability
        
        # Adjust based on protein type
        protein_type = protein_info.get('type')
        if protein_type == ProteinType.ENZYME:
            vulnerability += 0.2  # Enzymes more vulnerable due to active sites
        elif protein_type == ProteinType.DAIRY:
            vulnerability += 0.1  # Dairy proteins moderately vulnerable
        
        # Adjust based on molecular weight (larger proteins more binding sites)
        mw = protein_info.get('molecular_weight', 50000)
        if mw > 100000:
            vulnerability += 0.2
        elif mw > 50000:
            vulnerability += 0.1
        
        # Adjust based on isoelectric point (extreme pI more reactive)
        pi = protein_info.get('isoelectric_point', 7.0)
        if pi < 4.0 or pi > 10.0:
            vulnerability += 0.1
        
        return min(vulnerability, 1.0)
    
    def generate_food_composition_report(self, food_type: str) -> Dict[str, Any]:
        """Generate comprehensive food composition report"""
        
        # Get relevant proteins
        relevant_proteins = {name: info for name, info in self.protein_database.items() 
                           if self._is_protein_relevant_to_food(info, food_type)}
        
        # Get relevant toxins
        relevant_toxins = {name: profile for name, profile in self.toxin_database.items()
                          if self._is_toxin_relevant_to_food(profile, food_type)}
        
        # Calculate risk matrix
        risk_matrix = []
        for protein_name in relevant_proteins.keys():
            for toxin_name in relevant_toxins.keys():
                risk = self.predict_protein_toxin_interaction_risk(protein_name, toxin_name)
                risk_matrix.append({
                    'protein': protein_name,
                    'toxin': toxin_name,
                    'risk_level': risk['risk_level'],
                    'confidence': risk['confidence']
                })
        
        # Generate regulatory assessment
        regulatory_assessment = {}
        for region, limits in self.regulatory_database.items():
            compliant_compounds = 0
            total_compounds = 0
            for toxin_name in relevant_toxins.keys():
                if toxin_name in limits:
                    total_compounds += 1
                    # Assume compliance for now (would require actual testing data)
                    compliant_compounds += 1
            
            if total_compounds > 0:
                regulatory_assessment[region] = {
                    'compliance_rate': compliant_compounds / total_compounds,
                    'assessed_compounds': total_compounds
                }
        
        return {
            'food_type': food_type,
            'relevant_proteins': list(relevant_proteins.keys()),
            'relevant_toxins': list(relevant_toxins.keys()),
            'risk_matrix': risk_matrix,
            'high_risk_interactions': [r for r in risk_matrix if r['risk_level'] == 'high'],
            'regulatory_assessment': regulatory_assessment,
            'total_interactions_assessed': len(risk_matrix),
            'generation_timestamp': pd.Timestamp.now().isoformat()
        }
    
    def _is_protein_relevant_to_food(self, protein_info: Dict[str, Any], food_type: str) -> bool:
        """Check if protein is relevant to food type"""
        protein_type = protein_info.get('type')
        food_type_lower = food_type.lower()
        
        if 'dairy' in food_type_lower and protein_type == ProteinType.DAIRY:
            return True
        elif 'meat' in food_type_lower and protein_type == ProteinType.MEAT:
            return True
        elif any(grain in food_type_lower for grain in ['wheat', 'grain', 'cereal']) and protein_type == ProteinType.GRAIN:
            return True
        elif protein_type == ProteinType.ENZYME:  # Enzymes relevant to all foods
            return True
        
        return False
    
    def _is_toxin_relevant_to_food(self, toxin_profile: ToxinProfile, food_type: str) -> bool:
        """Check if toxin is relevant to food type"""
        food_type_lower = food_type.lower()
        
        # Mycotoxins relevant to grains and dairy
        if toxin_profile.toxin_type == ToxinType.MYCOTOXIN:
            return any(keyword in food_type_lower for keyword in ['grain', 'cereal', 'corn', 'wheat', 'dairy', 'nuts'])
        
        # Plant toxins relevant to plant-based foods
        elif toxin_profile.toxin_type == ToxinType.PLANT:
            return any(keyword in food_type_lower for keyword in ['vegetable', 'fruit', 'plant', 'potato'])
        
        # Marine toxins relevant to seafood
        elif toxin_profile.toxin_type == ToxinType.MARINE:
            return any(keyword in food_type_lower for keyword in ['fish', 'seafood', 'marine', 'shellfish'])
        
        # Bacterial toxins relevant to all foods
        elif toxin_profile.toxin_type == ToxinType.BACTERIAL:
            return True
        
        # Chemical contaminants relevant to processed foods
        elif toxin_profile.toxin_type == ToxinType.CHEMICAL:
            return any(keyword in food_type_lower for keyword in ['processed', 'fried', 'baked', 'heated'])
        
        return False
    
    def export_data_to_csv(self, data_type: str, filepath: str):
        """Export database to CSV format"""
        filepath = Path(filepath)
        
        if data_type == 'proteins':
            df = pd.DataFrame.from_dict(self.protein_database, orient='index')
            df.index.name = 'protein_name'
            df.to_csv(filepath)
            
        elif data_type == 'toxins':
            toxin_data = {}
            for name, profile in self.toxin_database.items():
                toxin_data[name] = {
                    'toxin_name': profile.toxin_name,
                    'toxin_type': profile.toxin_type.value,
                    'molecular_formula': profile.molecular_formula,
                    'molecular_weight': profile.molecular_weight,
                    'ld50': profile.ld50,
                    'regulatory_limit': profile.regulatory_limit,
                    'mechanism_of_action': profile.mechanism_of_action
                }
            df = pd.DataFrame.from_dict(toxin_data, orient='index')
            df.index.name = 'toxin_id'
            df.to_csv(filepath)
            
        elif data_type == 'regulatory':
            all_limits = []
            for region, limits in self.regulatory_database.items():
                for compound, info in limits.items():
                    all_limits.append({
                        'region': region,
                        'compound': compound,
                        'limit': info['limit'],
                        'unit': info['unit'],
                        'food_type': info['food_type']
                    })
            df = pd.DataFrame(all_limits)
            df.to_csv(filepath, index=False)
        
        
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics of the molecular toolkit"""
        return {
            'total_proteins': len(self.protein_database),
            'total_toxins': len(self.toxin_database),
            'protein_types': {ptype.value: sum(1 for p in self.protein_database.values() 
                                              if p.get('type') == ptype) 
                             for ptype in ProteinType},
            'toxin_types': {ttype.value: sum(1 for t in self.toxin_database.values() 
                                           if t.toxin_type == ttype) 
                           for ttype in ToxinType},
            'regulatory_regions': list(self.regulatory_database.keys()),
            'total_known_interactions': sum(len(interactions) for interactions in self.interaction_database.values())
        }


# Test function
def test_molecular_toolkit():
    """Test molecular toolkit functionality"""
    print("🧪 Testing Molecular Toolkit")
    
    toolkit = MolecularToolkit()
    
    # Test database loading
    stats = toolkit.get_summary_statistics()
    print(f"📊 Database stats: {stats}")
    
    # Test protein retrieval
    protein_info = toolkit.get_protein_info('casein')
    print(f"🥛 Casein info: {protein_info['name'] if protein_info else 'Not found'}")
    
    # Test toxin retrieval
    toxin_profile = toolkit.get_toxin_profile('aflatoxin_b1')
    print(f"☠️ Aflatoxin B1 LD50: {toxin_profile.ld50 if toxin_profile else 'Not found'} mg/kg")
    
    
    smiles = 'COc1cc2c(c3oc4cc(OC)c(O)cc4c(=O)c3c1)C1C=COC1O2'  # Aflatoxin B1
    props = toolkit.calculate_molecular_properties(smiles)
    print(f"⚗️ Molecular properties: MW={props.get('molecular_weight', 0):.1f}, LogP={props.get('logp', 0):.2f}")
    
    # Test interaction risk prediction
    risk = toolkit.predict_protein_toxin_interaction_risk('albumin', 'aflatoxin_b1')
    print(f"⚠️ Interaction risk: {risk['risk_level']} (confidence: {risk['confidence']:.2f})")
    
    # Test food composition report
    report = toolkit.generate_food_composition_report('dairy_milk')
    print(f"📋 Food report: {len(report['relevant_proteins'])} proteins, {len(report['relevant_toxins'])} toxins")
    
    print("✅ Molecular toolkit test completed")


if __name__ == "__main__":
    test_molecular_toolkit()