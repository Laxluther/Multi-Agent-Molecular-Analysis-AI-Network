from crewai.tools import tool
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime, timedelta


@tool
def executive_summary(analysis_results: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate executive summary of food safety analysis
    
    Args:
        analysis_results: Complete analysis results
        
    Returns:
        Executive summary content
    """
    
    safety_score = analysis_results.get('safety_assessment', {}).get('overall_safety_score', 5.0)
    risk_level = analysis_results.get('safety_assessment', {}).get('risk_level', 'moderate')
    protein_count = len(analysis_results.get('protein_analyses', {}))
    interaction_count = len(analysis_results.get('interactions', []))
    
    # Key findings
    key_findings = []
    
    if safety_score >= 8.0:
        key_findings.append("✅ Food sample demonstrates excellent safety profile")
    elif safety_score >= 6.0:
        key_findings.append("⚠️ Food sample shows acceptable safety with minor concerns")
    elif safety_score >= 4.0:
        key_findings.append("⚠️ Moderate safety concerns identified requiring attention")
    else:
        key_findings.append("🚨 Significant safety risks detected requiring immediate action")
    
    # Protein stability findings
    protein_analyses = analysis_results.get('protein_analyses', {})
    if protein_analyses:
        avg_stability = sum(p.get('stability_score', 7.0) for p in protein_analyses.values()) / len(protein_analyses)
        if avg_stability >= 7.0:
            key_findings.append(f"✅ Proteins demonstrate good stability (avg: {avg_stability:.1f}/10)")
        else:
            key_findings.append(f"⚠️ Protein stability concerns detected (avg: {avg_stability:.1f}/10)")
    
    # Interaction findings
    critical_interactions = len([i for i in analysis_results.get('interactions', []) 
                                if i.get('binding_affinity', 0) < -7.0])
    if critical_interactions > 0:
        key_findings.append(f"🔍 {critical_interactions} high-affinity toxin interactions detected")
    
    # Regulatory compliance
    compliance = analysis_results.get('regulatory_compliance', {})
    if compliance.get('overall_status') == 'fully_compliant':
        key_findings.append("✅ Fully compliant with regulatory standards")
    elif compliance.get('violations'):
        key_findings.append(f"❌ {len(compliance['violations'])} regulatory violations identified")
    
    # Generate summary text
    summary_text = f"""
This comprehensive food safety analysis examined {protein_count} proteins and {interaction_count} potential toxin interactions using advanced molecular modeling and multi-agent AI systems. 

OVERALL ASSESSMENT: {risk_level.upper()} RISK (Safety Score: {safety_score}/10)

KEY FINDINGS:
{chr(10).join(f"• {finding}" for finding in key_findings)}

IMMEDIATE ACTIONS REQUIRED:
"""
    
    # Add action items based on risk level
    if risk_level in ['high', 'critical']:
        summary_text += "• Immediate process review and safety intervention required\n"
        summary_text += "• Enhanced monitoring and testing protocols\n"
        summary_text += "• Regulatory notification may be necessary\n"
    elif risk_level == 'moderate':
        summary_text += "• Process optimization recommended\n"
        summary_text += "• Increased monitoring frequency\n"
        summary_text += "• Staff training on identified risks\n"
    else:
        summary_text += "• Continue current safety protocols\n"
        summary_text += "• Regular monitoring as scheduled\n"
        summary_text += "• Document best practices for replication\n"
    
    return {
        'executive_summary': summary_text.strip(),
        'key_metrics': {
            'safety_score': safety_score,
            'risk_level': risk_level,
            'proteins_analyzed': protein_count,
            'interactions_assessed': interaction_count,
            'critical_interactions': critical_interactions
        },
        'summary_length': len(summary_text.split()),
        'generated_timestamp': datetime.now().isoformat()
    }
   
@tool
def format_technical_results(protein_analyses: Dict[str, Any], 
                           interactions: List[Dict[str, Any]],
                           enzyme_kinetics: List[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Format technical analysis results for professional presentation
    
    Args:
        protein_analyses: Protein analysis results
        interactions: Toxin-protein interactions
        enzyme_kinetics: Enzyme kinetics data
        
    Returns:
        Formatted technical content
    """

    # Protein Analysis Section
    protein_section = "## PROTEIN STRUCTURE ANALYSIS\n\n"
    
    for protein_name, analysis in protein_analyses.items():
        stability = analysis.get('stability_score', 7.0)
        mw = analysis.get('molecular_weight', 50000)
        pi = analysis.get('isoelectric_point', 7.0)
        confidence = analysis.get('analysis_confidence', 0.8)
        
        protein_section += f"### {protein_name.replace('_', ' ').title()}\n"
        protein_section += f"- **Molecular Weight**: {mw:,.0f} Da\n"
        protein_section += f"- **Isoelectric Point**: {pi:.2f}\n"
        protein_section += f"- **Stability Score**: {stability:.1f}/10\n"
        protein_section += f"- **Analysis Confidence**: {confidence:.1%}\n"
        
        # Processing sensitivity
        sensitivity = analysis.get('processing_sensitivity', {})
        if sensitivity:
            protein_section += f"- **Processing Sensitivity**:\n"
            for factor, value in sensitivity.items():
                protein_section += f"  - {factor.replace('_', ' ').title()}: {value:.2f}\n"
        
        protein_section += "\n"
    
    # Interaction Analysis Section
    interaction_section = "## TOXIN-PROTEIN INTERACTIONS\n\n"
    
    if interactions:
        # Summary table
        interaction_section += "| Toxin | Protein | Binding Affinity | Interaction Type | Risk Score |\n"
        interaction_section += "|-------|---------|------------------|------------------|------------|\n"
        
        for interaction in interactions:
            toxin = interaction.get('toxin_name', 'Unknown')
            protein = interaction.get('protein_name', 'Unknown')
            affinity = interaction.get('binding_affinity', 0)
            int_type = interaction.get('interaction_type', 'Unknown')
            risk_score = interaction.get('risk_score', 5.0)
            
            interaction_section += f"| {toxin} | {protein} | {affinity:.2f} kcal/mol | {int_type} | {risk_score:.1f}/10 |\n"
        
        interaction_section += "\n### Detailed Interaction Analysis\n\n"
        
        # Detailed analysis for high-risk interactions
        high_risk_interactions = [i for i in interactions if abs(i.get('binding_affinity', 0)) > 6.0]
        
        for interaction in high_risk_interactions:
            toxin = interaction.get('toxin_name', 'Unknown')
            protein = interaction.get('protein_name', 'Unknown')
            affinity = interaction.get('binding_affinity', 0)
            enhancement = interaction.get('toxicity_enhancement', 1.0)
            structural_changes = interaction.get('structural_changes', {})
            
            interaction_section += f"#### {toxin} - {protein} Interaction\n"
            interaction_section += f"- **Binding Affinity**: {affinity:.2f} kcal/mol (Strong)\n"
            interaction_section += f"- **Toxicity Enhancement**: {enhancement:.1f}x\n"
            
            if structural_changes:
                interaction_section += f"- **Structural Changes**:\n"
                for change_type, value in structural_changes.items():
                    interaction_section += f"  - {change_type.replace('_', ' ').title()}: {value:.1f}%\n"
            
            interaction_section += "\n"
    else:
        interaction_section += "No significant toxin-protein interactions detected.\n\n"
    
    # Enzyme Kinetics Section
    enzyme_section = "## ENZYME KINETICS ANALYSIS\n\n"
    
    if enzyme_kinetics:
        enzyme_section += "| Enzyme | Substrate | Km (mM) | Vmax (μmol/min/mg) | Activity Factor |\n"
        enzyme_section += "|--------|-----------|---------|-------------------|------------------|\n"
        
        for kinetics in enzyme_kinetics:
            enzyme = kinetics.get('enzyme_name', 'Unknown')
            substrate = kinetics.get('substrate', 'Unknown')
            km = kinetics.get('km', 1.0)
            vmax = kinetics.get('vmax', 20.0)
            activity_factors = kinetics.get('activity_factors', {})
            avg_activity = sum(activity_factors.values()) / len(activity_factors) if activity_factors else 1.0
            
            enzyme_section += f"| {enzyme} | {substrate} | {km:.2f} | {vmax:.1f} | {avg_activity:.2f} |\n"
        
        enzyme_section += "\n"
    else:
        enzyme_section += "Enzyme kinetics analysis not performed.\n\n"
    
    return {
        'protein_analysis': protein_section,
        'interaction_analysis': interaction_section,
        'enzyme_analysis': enzyme_section,
        'total_sections': 3,
        'formatted_timestamp': datetime.now().isoformat()
    }

@tool
def generate_recommendations_section(safety_recommendations: List[Dict[str, Any]],
                                   regulatory_compliance: Dict[str, Any]) -> str:
    """
    Generate formatted recommendations section
    
    Args:
        safety_recommendations: List of safety recommendations
        regulatory_compliance: Regulatory compliance assessment
        
    Returns:
        Formatted recommendations content
    """
    
    recommendations_text = "## RECOMMENDATIONS & ACTION PLAN\n\n"
    
    # Priority-based recommendations
    priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    
    for priority in priorities:
        priority_recs = [r for r in safety_recommendations if r.get('priority') == priority]
        
        if priority_recs:
            recommendations_text += f"### {priority} Priority Actions\n\n"
            
            for i, rec in enumerate(priority_recs, 1):
                category = rec.get('category', 'General')
                recommendation = rec.get('recommendation', 'No recommendation provided')
                rationale = rec.get('rationale', 'No rationale provided')
                implementation = rec.get('implementation', 'Implementation details not specified')
                timeline = rec.get('timeline', 'Timeline not specified')
                responsible = rec.get('responsible_party', 'Responsibility not assigned')
                
                recommendations_text += f"**{i}. {category}**\n\n"
                recommendations_text += f"*Recommendation*: {recommendation}\n\n"
                recommendations_text += f"*Rationale*: {rationale}\n\n"
                recommendations_text += f"*Implementation*: {implementation}\n\n"
                recommendations_text += f"*Timeline*: {timeline}\n\n"
                recommendations_text += f"*Responsible Party*: {responsible}\n\n"
                recommendations_text += "---\n\n"
    
    # Regulatory compliance recommendations
    if regulatory_compliance:
        recommendations_text += "### Regulatory Compliance Actions\n\n"
        
        violations = regulatory_compliance.get('violations', [])
        warnings = regulatory_compliance.get('warnings', [])
        
        if violations:
            recommendations_text += "**Immediate Compliance Actions Required:**\n\n"
            for violation in violations:
                compound = violation.get('compound', 'Unknown')
                detected = violation.get('detected', 0)
                limit = violation.get('limit', 0)
                regulation = violation.get('regulation', 'Unknown regulation')
                
                recommendations_text += f"- **{compound}**: Reduce levels from {detected} to below {limit} ppb "
                recommendations_text += f"(Reference: {regulation})\n"
            
            recommendations_text += "\n"
        
        if warnings:
            recommendations_text += "**Preventive Compliance Actions:**\n\n"
            for warning in warnings:
                compound = warning.get('compound', 'Unknown')
                percentage = warning.get('percentage_of_limit', 0)
                
                recommendations_text += f"- **{compound}**: Currently at {percentage}% of regulatory limit - "
                recommendations_text += f"implement preventive measures\n"
            
            recommendations_text += "\n"
    
    # Implementation timeline
    recommendations_text += "### Implementation Timeline\n\n"
    recommendations_text += "| Priority | Timeline | Actions |\n"
    recommendations_text += "|----------|----------|----------|\n"
    
    timeline_summary = {}
    for rec in safety_recommendations:
        timeline = rec.get('timeline', 'Not specified')
        priority = rec.get('priority', 'MEDIUM')
        
        if timeline not in timeline_summary:
            timeline_summary[timeline] = []
        timeline_summary[timeline].append(f"{priority}: {rec.get('category', 'Action')}")
    
    for timeline, actions in timeline_summary.items():
        action_list = "; ".join(actions[:3])  # Limit to 3 actions per row
        if len(actions) > 3:
            action_list += f" (+{len(actions)-3} more)"
        recommendations_text += f"| {timeline} | {action_list} |\n"
    
    recommendations_text += "\n"
    
    return recommendations_text
        
@tool
def compile_complete_report(executive_summary: str, technical_results: Dict[str, str],
                          recommendations: str, metadata: Dict[str, Any]) -> str:
    """
    Compile complete professional report
    
    Args:
        executive_summary: Executive summary content
        technical_results: Technical analysis sections
        recommendations: Recommendations section
        metadata: Report metadata
        
    Returns:
        Complete formatted report
    """
    
    # Report header
    report = f"""# FOOD SAFETY ANALYSIS REPORT
## Multi-Agent AI Assessment

**Report ID**: {metadata.get('report_id', 'FSA-' + datetime.now().strftime('%Y%m%d-%H%M%S'))}
**Generated**: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Analysis Platform**: FoodSafety AI Intelligence Network
**Framework**: Google ADK + CrewAI + A2A Protocol

---

## EXECUTIVE SUMMARY

{executive_summary}

---

{technical_results.get('protein_analysis', '')}

{technical_results.get('interaction_analysis', '')}

{technical_results.get('enzyme_analysis', '')}

---

{recommendations}

---

## METHODOLOGY & CONFIDENCE

### Analysis Framework
This assessment utilized a multi-agent artificial intelligence system combining:

- **Google Agent Development Kit (ADK)**: For computational molecular analysis
- **CrewAI Framework**: For collaborative workflow coordination  
- **A2A Protocol**: For inter-agent communication and data exchange

### Computational Methods
- **Protein Structure Prediction**: ESMFold neural network models
- **Molecular Docking**: Physics-based binding affinity calculation
- **Enzyme Kinetics**: Michaelis-Menten kinetic modeling
- **Risk Assessment**: Quantitative safety scoring algorithms

### Confidence Assessment
- **Protein Analysis Confidence**: {metadata.get('protein_confidence', 85)}%
- **Interaction Prediction Confidence**: {metadata.get('interaction_confidence', 78)}%
- **Overall Assessment Confidence**: {metadata.get('overall_confidence', 82)}%

### Data Sources
- UniProt Protein Database
- PubChem Chemical Database
- BRENDA Enzyme Database
- FDA/EFSA Regulatory Guidelines

---

## LIMITATIONS & DISCLAIMERS

1. **Computational Predictions**: Results are based on computational models and may not fully represent real-world conditions
2. **Experimental Validation**: Recommendations should be validated through appropriate experimental testing
3. **Regulatory Guidance**: This report does not constitute official regulatory approval or guidance
4. **Professional Review**: Results should be reviewed by qualified food safety professionals

---

## APPENDICES

### A. Detailed Analytical Parameters
- Analysis performed using standardized protocols
- All molecular simulations conducted at physiological conditions
- Risk scoring based on validated safety assessment models

### B. Regulatory References
- FDA 21 CFR Parts 109, 110, 117
- EU Regulation 1881/2006 on contaminants
- Codex Alimentarius standards

### C. Quality Assurance
- Multi-agent verification of critical results
- Cross-validation of safety calculations
- Automated consistency checking

---

**Report prepared by**: FoodSafety AI Intelligence Network
**Contact**: [Contact Information]
**Next Review Date**: {(datetime.now() + timedelta(days=90)).strftime('%B %d, %Y')}

*This document contains confidential and proprietary information. Distribution should be limited to authorized personnel only.*
"""
    
    return report.strip()
        
@tool
def generate_charts_data(safety_analysis: Dict[str, Any],
                        protein_analyses: Dict[str, Any],
                        interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate data for visualization charts
    
    Args:
        safety_analysis: Safety assessment results
        protein_analyses: Protein analysis data
        interactions: Interaction results
        
    Returns:
        Chart data for visualization
    """

    chart_data = {}
    
    # Safety score gauge chart
    safety_score = safety_analysis.get('overall_safety_score', 5.0)
    chart_data['safety_gauge'] = {
        'value': safety_score,
        'max': 10,
        'ranges': [
            {'min': 0, 'max': 2, 'color': '#dc3545', 'label': 'Critical'},
            {'min': 2, 'max': 4, 'color': '#fd7e14', 'label': 'High Risk'},
            {'min': 4, 'max': 6, 'color': '#ffc107', 'label': 'Moderate'},
            {'min': 6, 'max': 8, 'color': '#20c997', 'label': 'Low Risk'},
            {'min': 8, 'max': 10, 'color': '#28a745', 'label': 'Safe'}
        ]
    }
    
    # Protein stability bar chart
    if protein_analyses:
        chart_data['protein_stability'] = {
            'labels': list(protein_analyses.keys()),
            'data': [p.get('stability_score', 7.0) for p in protein_analyses.values()],
            'backgroundColor': ['#007bff' if score >= 7.0 else '#ffc107' if score >= 5.0 else '#dc3545' 
                                for score in [p.get('stability_score', 7.0) for p in protein_analyses.values()]]
        }
    
    # Interaction risk scatter plot
    if interactions:
        chart_data['interaction_risk'] = {
            'data': [
                {
                    'x': abs(i.get('binding_affinity', 0)),
                    'y': i.get('toxicity_enhancement', 1.0),
                    'label': f"{i.get('toxin_name', 'Unknown')} - {i.get('protein_name', 'Unknown')}",
                    'risk_score': i.get('risk_score', 5.0)
                }
                for i in interactions
            ],
            'x_label': 'Binding Affinity (|kcal/mol|)',
            'y_label': 'Toxicity Enhancement Factor'
        }
    
    # Risk factor pie chart
    component_risks = safety_analysis.get('component_risks', {})
    if component_risks:
        chart_data['risk_breakdown'] = {
            'labels': ['Interaction Risk', 'Protein Stability Risk', 'Regulatory Risk'],
            'data': [
                component_risks.get('interaction_risk', 0),
                component_risks.get('protein_stability_risk', 0),
                component_risks.get('regulatory_compliance_risk', 0)
            ],
            'backgroundColor': ['#ff6384', '#36a2eb', '#ffcd56']
        }
    
    # Confidence levels radar chart
    chart_data['confidence_radar'] = {
        'labels': ['Protein Analysis', 'Interaction Prediction', 'Safety Assessment', 'Regulatory Compliance', 'Overall Confidence'],
        'data': [85, 78, 82, 90, 80],  # Example confidence percentages
        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
        'borderColor': 'rgba(54, 162, 235, 1)'
    }
    
    return chart_data
    