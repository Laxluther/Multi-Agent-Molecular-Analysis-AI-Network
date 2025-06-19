

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class RiskLevel(Enum):
    """Risk level enumeration"""
    SAFE = "safe"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ToxinType(Enum):
    """Types of food toxins"""
    MYCOTOXIN = "mycotoxin"
    BACTERIAL = "bacterial"
    PLANT = "plant"
    CHEMICAL = "chemical"
    MARINE = "marine"
    HEAVY_METAL = "heavy_metal"


class ProteinType(Enum):
    """Types of food proteins"""
    DAIRY = "dairy"
    MEAT = "meat"
    GRAIN = "grain"
    LEGUME = "legume"
    FRUIT_VEGETABLE = "fruit_vegetable"
    ENZYME = "enzyme"


@dataclass
class ProcessingConditions:
    """Food processing conditions"""
    temperature: float  # Celsius
    ph: float
    duration: int  # minutes
    pressure: Optional[float] = None  # bar
    humidity: Optional[float] = None  # %
    ionic_strength: Optional[float] = 0.15  # M
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'temperature': self.temperature,
            'ph': self.ph,
            'duration': self.duration,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'ionic_strength': self.ionic_strength
        }


@dataclass
class FoodSample:
    """Represents a food sample for analysis"""
    sample_id: str
    name: str
    food_type: str
    proteins: List[str]
    suspected_toxins: List[str]
    processing_conditions: ProcessingConditions
    composition: Optional[Dict[str, float]] = None  # % composition
    origin: Optional[str] = None
    sample_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.sample_date is None:
            self.sample_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sample_id': self.sample_id,
            'name': self.name,
            'food_type': self.food_type,
            'proteins': self.proteins,
            'suspected_toxins': self.suspected_toxins,
            'processing_conditions': self.processing_conditions.to_dict(),
            'composition': self.composition,
            'origin': self.origin,
            'sample_date': self.sample_date.isoformat() if self.sample_date else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FoodSample':
        return cls(
            sample_id=data['sample_id'],
            name=data['name'],
            food_type=data['food_type'],
            proteins=data['proteins'],
            suspected_toxins=data['suspected_toxins'],
            processing_conditions=ProcessingConditions(**data['processing_conditions']),
            composition=data.get('composition'),
            origin=data.get('origin'),
            sample_date=datetime.fromisoformat(data['sample_date']) if data.get('sample_date') else None
        )


@dataclass
class ProteinStructure:
    """Protein structure information"""
    sequence: str
    secondary_structure: Optional[str] = None
    predicted_structure: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    binding_sites: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sequence': self.sequence,
            'secondary_structure': self.secondary_structure,
            'predicted_structure': self.predicted_structure,
            'confidence_score': self.confidence_score,
            'binding_sites': self.binding_sites
        }


@dataclass
class ProteinAnalysis:
    """Complete protein analysis results"""
    protein_name: str
    protein_type: ProteinType
    structure: ProteinStructure
    stability_score: float
    functional_sites: List[Dict[str, Any]]
    molecular_weight: float
    isoelectric_point: float
    hydrophobicity_index: float
    processing_sensitivity: Dict[str, float]  # temperature, pH, etc.
    analysis_confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'protein_name': self.protein_name,
            'protein_type': self.protein_type.value,
            'structure': self.structure.to_dict(),
            'stability_score': self.stability_score,
            'functional_sites': self.functional_sites,
            'molecular_weight': self.molecular_weight,
            'isoelectric_point': self.isoelectric_point,
            'hydrophobicity_index': self.hydrophobicity_index,
            'processing_sensitivity': self.processing_sensitivity,
            'analysis_confidence': self.analysis_confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProteinAnalysis':
        return cls(
            protein_name=data['protein_name'],
            protein_type=ProteinType(data['protein_type']),
            structure=ProteinStructure(**data['structure']),
            stability_score=data['stability_score'],
            functional_sites=data['functional_sites'],
            molecular_weight=data['molecular_weight'],
            isoelectric_point=data['isoelectric_point'],
            hydrophobicity_index=data['hydrophobicity_index'],
            processing_sensitivity=data['processing_sensitivity'],
            analysis_confidence=data['analysis_confidence']
        )


@dataclass
class ToxinProfile:
    """Toxin molecular profile"""
    toxin_name: str
    toxin_type: ToxinType
    molecular_formula: str
    molecular_weight: float
    structure_smiles: Optional[str] = None
    ld50: Optional[float] = None  # mg/kg
    regulatory_limit: Optional[float] = None  # ppm or ppb
    mechanism_of_action: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'toxin_name': self.toxin_name,
            'toxin_type': self.toxin_type.value,
            'molecular_formula': self.molecular_formula,
            'molecular_weight': self.molecular_weight,
            'structure_smiles': self.structure_smiles,
            'ld50': self.ld50,
            'regulatory_limit': self.regulatory_limit,
            'mechanism_of_action': self.mechanism_of_action
        }


@dataclass
class ToxinInteraction:
    """Toxin-protein interaction analysis"""
    toxin_name: str
    protein_name: str
    binding_affinity: float  # kcal/mol
    binding_sites: List[Dict[str, Any]]
    interaction_type: str  # competitive, non-competitive, allosteric
    structural_changes: Dict[str, float]  # % changes in structure
    toxicity_enhancement: float  # factor of increased toxicity
    confidence_score: float
    literature_support: List[str]  # references
    
    def get_risk_score(self) -> float:
        """Calculate interaction risk score (0-10)"""
        # Higher binding affinity (more negative) = higher risk
        affinity_risk = min(abs(self.binding_affinity) / 2.0, 5.0)
        
        # Structural changes contribute to risk
        structure_risk = sum(self.structural_changes.values()) / len(self.structural_changes) if self.structural_changes else 0
        structure_risk = min(structure_risk / 10.0, 3.0)
        
        # Toxicity enhancement
        toxicity_risk = min(self.toxicity_enhancement, 2.0)
        
        total_risk = affinity_risk + structure_risk + toxicity_risk
        return min(total_risk, 10.0)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'toxin_name': self.toxin_name,
            'protein_name': self.protein_name,
            'binding_affinity': self.binding_affinity,
            'binding_sites': self.binding_sites,
            'interaction_type': self.interaction_type,
            'structural_changes': self.structural_changes,
            'toxicity_enhancement': self.toxicity_enhancement,
            'confidence_score': self.confidence_score,
            'literature_support': self.literature_support,
            'risk_score': self.get_risk_score()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToxinInteraction':
        return cls(
            toxin_name=data['toxin_name'],
            protein_name=data['protein_name'],
            binding_affinity=data['binding_affinity'],
            binding_sites=data['binding_sites'],
            interaction_type=data['interaction_type'],
            structural_changes=data['structural_changes'],
            toxicity_enhancement=data['toxicity_enhancement'],
            confidence_score=data['confidence_score'],
            literature_support=data['literature_support']
        )


@dataclass
class EnzymeKinetics:
    """Enzyme kinetics analysis"""
    enzyme_name: str
    substrate: str
    km: float  # Michaelis constant (mM)
    vmax: float  # Maximum velocity (μmol/min/mg)
    kcat: float  # Catalytic constant (s⁻¹)
    inhibition_data: Dict[str, Dict[str, float]]  # inhibitor -> {Ki, type}
    optimal_conditions: ProcessingConditions
    activity_factors: Dict[str, float]  # condition -> activity factor
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'enzyme_name': self.enzyme_name,
            'substrate': self.substrate,
            'km': self.km,
            'vmax': self.vmax,
            'kcat': self.kcat,
            'inhibition_data': self.inhibition_data,
            'optimal_conditions': self.optimal_conditions.to_dict(),
            'activity_factors': self.activity_factors
        }


@dataclass
class SafetyAnalysis:
    """Complete food safety analysis results"""
    food_sample_id: str
    overall_safety_score: float  # 0-10 (10 = safest)
    risk_level: RiskLevel
    protein_analyses: Dict[str, ProteinAnalysis]
    toxin_interactions: List[ToxinInteraction]
    enzyme_kinetics: Optional[List[EnzymeKinetics]] = None
    safety_recommendations: List[str] = field(default_factory=list)
    regulatory_compliance: Dict[str, bool] = field(default_factory=dict)
    confidence_score: float = 0.0
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    report_data: Optional[Dict[str, Any]] = None
    
    def get_critical_interactions(self) -> List[ToxinInteraction]:
        """Get interactions with high risk scores"""
        return [interaction for interaction in self.toxin_interactions 
                if interaction.get_risk_score() >= 7.0]
    
    def get_safety_summary(self) -> Dict[str, Any]:
        """Get summary of safety analysis"""
        return {
            'overall_score': self.overall_safety_score,
            'risk_level': self.risk_level.value,
            'total_interactions': len(self.toxin_interactions),
            'critical_interactions': len(self.get_critical_interactions()),
            'confidence': self.confidence_score,
            'recommendations_count': len(self.safety_recommendations),
            'timestamp': self.analysis_timestamp.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'food_sample_id': self.food_sample_id,
            'overall_safety_score': self.overall_safety_score,
            'risk_level': self.risk_level.value,
            'protein_analyses': {name: analysis.to_dict() 
                               for name, analysis in self.protein_analyses.items()},
            'toxin_interactions': [interaction.to_dict() 
                                 for interaction in self.toxin_interactions],
            'enzyme_kinetics': [kinetics.to_dict() for kinetics in self.enzyme_kinetics] 
                             if self.enzyme_kinetics else None,
            'safety_recommendations': self.safety_recommendations,
            'regulatory_compliance': self.regulatory_compliance,
            'confidence_score': self.confidence_score,
            'analysis_timestamp': self.analysis_timestamp.isoformat(),
            'report_data': self.report_data,
            'safety_summary': self.get_safety_summary()
        }
    
    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """Save analysis to JSON file"""
        filepath = Path(filepath)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
    
    @classmethod
    def load_from_file(cls, filepath: Union[str, Path]) -> 'SafetyAnalysis':
        """Load analysis from JSON file"""
        filepath = Path(filepath)
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return cls(
            food_sample_id=data['food_sample_id'],
            overall_safety_score=data['overall_safety_score'],
            risk_level=RiskLevel(data['risk_level']),
            protein_analyses={name: ProteinAnalysis.from_dict(analysis_data)
                            for name, analysis_data in data['protein_analyses'].items()},
            toxin_interactions=[ToxinInteraction.from_dict(interaction_data)
                              for interaction_data in data['toxin_interactions']],
            enzyme_kinetics=[EnzymeKinetics(**kinetics_data) 
                           for kinetics_data in data['enzyme_kinetics']] 
                          if data['enzyme_kinetics'] else None,
            safety_recommendations=data['safety_recommendations'],
            regulatory_compliance=data['regulatory_compliance'],
            confidence_score=data['confidence_score'],
            analysis_timestamp=datetime.fromisoformat(data['analysis_timestamp']),
            report_data=data['report_data']
        )


# Common food toxins database
COMMON_FOOD_TOXINS = {
    'aflatoxin_b1': ToxinProfile(
        toxin_name='Aflatoxin B1',
        toxin_type=ToxinType.MYCOTOXIN,
        molecular_formula='C17H12O6',
        molecular_weight=312.27,
        structure_smiles='COc1cc2c(c3oc4cc(OC)c(O)cc4c(=O)c3c1)C1C=COC1O2',
        ld50=0.48,  # mg/kg in rats
        regulatory_limit=2.0,  # ppb in food
        mechanism_of_action='DNA intercalation and adduct formation'
    ),
    'ochratoxin_a': ToxinProfile(
        toxin_name='Ochratoxin A',
        toxin_type=ToxinType.MYCOTOXIN,
        molecular_formula='C20H18ClNO6',
        molecular_weight=403.8,
        ld50=20.0,
        regulatory_limit=5.0,
        mechanism_of_action='Protein synthesis inhibition'
    ),
    'botulinum_toxin': ToxinProfile(
        toxin_name='Botulinum Toxin',
        toxin_type=ToxinType.BACTERIAL,
        molecular_formula='Variable',
        molecular_weight=150000.0,
        ld50=0.000001,  # Extremely toxic
        regulatory_limit=0.0,  # Zero tolerance
        mechanism_of_action='Neurotransmitter release inhibition'
    ),
    'solanine': ToxinProfile(
        toxin_name='Solanine',
        toxin_type=ToxinType.PLANT,
        molecular_formula='C45H73NO15',
        molecular_weight=868.06,
        ld50=590.0,
        regulatory_limit=200.0,  # mg/kg in potatoes
        mechanism_of_action='Cell membrane disruption'
    ),
    'acrylamide': ToxinProfile(
        toxin_name='Acrylamide',
        toxin_type=ToxinType.CHEMICAL,
        molecular_formula='C3H5NO',
        molecular_weight=71.08,
        ld50=150.0,
        regulatory_limit=1000.0,  # μg/kg in various foods
        mechanism_of_action='DNA adduct formation'
    )
}

# Common food proteins database
COMMON_FOOD_PROTEINS = {
    'casein': {
        'name': 'Casein',
        'type': ProteinType.DAIRY,
        'sequence': 'MKLLILTCLVAVALARPKHPIKHQGLPQEVLNENLLRFFVAPFPEVFGK...',  # Abbreviated
        'molecular_weight': 24000.0,
        'isoelectric_point': 4.6
    },
    'whey_protein': {
        'name': 'β-Lactoglobulin',
        'type': ProteinType.DAIRY,
        'sequence': 'MKCLLLALALTCGAQALIVTQTMKGLDIQKVAGTWYSLAMAASDISLLDAQSAPLRVYV...',
        'molecular_weight': 18400.0,
        'isoelectric_point': 5.2
    },
    'gluten': {
        'name': 'Gliadin',
        'type': ProteinType.GRAIN,
        'sequence': 'MQVDPSGQVQWQAQQQPPFSQQQQQPISSQQPQQL...',
        'molecular_weight': 36000.0,
        'isoelectric_point': 8.0
    }
}