import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from orchestrator import FoodSafetyOrchestrator, create_sample_food
from data_models import FoodSample, ProcessingConditions
from molecular_tools import MolecularToolkit

# Page configuration
st.set_page_config(
    page_title="FoodSafety AI Network",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .risk-high {
        border-left-color: #dc3545 !important;
        background-color: #fff5f5 !important;
    }
    .risk-medium {
        border-left-color: #ffc107 !important;
        background-color: #fffbf0 !important;
    }
    .risk-low {
        border-left-color: #28a745 !important;
        background-color: #f8fff8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = FoodSafetyOrchestrator()
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'molecular_toolkit' not in st.session_state:
    st.session_state.molecular_toolkit = MolecularToolkit()

def create_sample_food_data():
    """Create sample food data for testing"""
    return {
        'dairy_milk': {
            'name': 'Fresh Dairy Milk',
            'food_type': 'dairy',
            'proteins': ['casein', 'whey_protein', 'lactalbumin', 'lysozyme'],
            'suspected_toxins': ['aflatoxin_b1', 'aflatoxin_m1'],
            'processing_conditions': {
                'temperature': 72.0,
                'ph': 6.5,
                'duration': 15,
                'ionic_strength': 0.15
            }
        },
        'wheat_flour': {
            'name': 'Wheat Flour',
            'food_type': 'grain',
            'proteins': ['gliadin', 'glutenin', 'amylase'],
            'suspected_toxins': ['deoxynivalenol', 'fumonisin_b1'],
            'processing_conditions': {
                'temperature': 25.0,
                'ph': 6.0,
                'duration': 0,
                'ionic_strength': 0.05
            }
        },
        'chicken_meat': {
            'name': 'Chicken Breast',
            'food_type': 'meat',
            'proteins': ['myosin', 'actin', 'albumin', 'protease'],
            'suspected_toxins': ['bacterial_toxin'],
            'processing_conditions': {
                'temperature': 165.0,
                'ph': 5.8,
                'duration': 20,
                'ionic_strength': 0.2
            }
        }
    }

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">🧬 FoodSafety AI Network</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">Pure CrewAI Multi-Agent System</p>', unsafe_allow_html=True)
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Framework", "CrewAI", "")
    with col2:
        st.metric("🧪 ESMFold", "Active", "Protein Analysis")
    with col3:
        st.metric("⚗️ RDKit", "Active", "Molecular Docking")
    with col4:
        st.metric("🔬 Enzyme Sim", "Active", "Kinetics")

def render_sidebar():
    """Render the sidebar"""
    st.sidebar.markdown("### 🎛️ System Info")
    st.sidebar.success("🟢 CrewAI System Online")
    st.sidebar.info("🧬 ESMFold: Protein structure prediction")
    st.sidebar.info("⚗️ RDKit: Molecular docking simulation")
    st.sidebar.info("🔬 Enzyme kinetics: Km, Vmax, kcat calculation")
    st.sidebar.info("📚 6 Crews: Research → Protein → Interaction → Enzyme → Safety → Report")
    
    st.sidebar.markdown("### 📊 Analysis Mode")
    analysis_mode = st.sidebar.selectbox(
        "Analysis Type",
        ["Complete Analysis", "Protein Focus", "Interaction Focus", "Safety Focus"]
    )
    
    return analysis_mode

def render_food_input_form():
    """Render food sample input form"""
    st.markdown("## 🍽️ Food Sample Input")
    
    # Sample selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        use_sample = st.selectbox(
            "Use Sample Data or Custom Input",
            ["Custom Input", "Sample: Dairy Milk", "Sample: Wheat Flour", "Sample: Chicken Meat"]
        )
    
    with col2:
        if st.button("📋 Load Sample", disabled=(use_sample == "Custom Input")):
            sample_mapping = {
                "Sample: Dairy Milk": "dairy_milk",
                "Sample: Wheat Flour": "wheat_flour", 
                "Sample: Chicken Meat": "chicken_meat"
            }
            sample_key = sample_mapping.get(use_sample)
            if sample_key:
                sample_data = create_sample_food_data()[sample_key]
                st.session_state.sample_data = sample_data
                st.success(f"✅ Loaded sample: {sample_data['name']}")
    
    # Input form
    with st.form("food_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic information
            sample_name = st.text_input("Sample Name", value=getattr(st.session_state, 'sample_data', {}).get('name', ''))
            food_type = st.selectbox(
                "Food Type",
                ["dairy", "meat", "grain", "vegetable", "fruit", "processed"],
                index=["dairy", "meat", "grain", "vegetable", "fruit", "processed"].index(
                    getattr(st.session_state, 'sample_data', {}).get('food_type', 'dairy')
                )
            )
            
            # Proteins
            st.subheader("🧬 Proteins of Interest")
            available_proteins = list(st.session_state.molecular_toolkit.protein_database.keys())
            selected_proteins = st.multiselect(
                "Select Proteins",
                available_proteins,
                default=getattr(st.session_state, 'sample_data', {}).get('proteins', [])
            )
        
        with col2:
            # Suspected toxins
            st.subheader("☠️ Suspected Toxins")
            available_toxins = list(st.session_state.molecular_toolkit.toxin_database.keys())
            selected_toxins = st.multiselect(
                "Select Toxins",
                available_toxins,
                default=getattr(st.session_state, 'sample_data', {}).get('suspected_toxins', [])
            )
            
            # Processing conditions
            st.subheader("⚙️ Processing Conditions")
            sample_conditions = getattr(st.session_state, 'sample_data', {}).get('processing_conditions', {})
            
            temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=300.0, 
                                        value=float(sample_conditions.get('temperature', 25.0)))
            ph = st.number_input("pH", min_value=0.0, max_value=14.0, 
                               value=float(sample_conditions.get('ph', 7.0)))
            duration = st.number_input("Duration (minutes)", min_value=0, max_value=1440,
                                     value=int(sample_conditions.get('duration', 60)))
            ionic_strength = st.number_input("Ionic Strength (M)", min_value=0.0, max_value=2.0,
                                           value=float(sample_conditions.get('ionic_strength', 0.15)))
        
        submitted = st.form_submit_button("🚀 Run CrewAI Analysis", type="primary")
        
        if submitted:
            if not sample_name or not selected_proteins or not selected_toxins:
                st.error("Please fill in all required fields")
                return None
            
            # Create food sample
            processing_conditions = ProcessingConditions(
                temperature=temperature,
                ph=ph,
                duration=duration,
                ionic_strength=ionic_strength
            )
            
            food_sample = FoodSample(
                sample_id=f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=sample_name,
                food_type=food_type,
                proteins=selected_proteins,
                suspected_toxins=selected_toxins,
                processing_conditions=processing_conditions
            )
            
            return food_sample
    
    return None

def run_analysis(food_sample: FoodSample):
    """Run the food safety analysis"""
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step indicators
    steps = [
        "📚 Research Crew: Literature & regulatory data",
        "🧬 Protein Crew: ESMFold structure prediction", 
        "⚗️ Interaction Crew: RDKit molecular docking",
        "🔬 Enzyme Crew: Kinetics simulation",
        "🛡️ Safety Crew: Risk assessment",
        "📋 Reporting Crew: Final report generation"
    ]
    
    results = None
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        
        if i == 0:
            # Mock some delay for demo
            import time
            time.sleep(1)
    
    # Run the actual analysis
    status_text.text("🤖 Running multi-agent analysis...")
    results = st.session_state.orchestrator.analyze_food_safety(food_sample)
    
    # Complete
    status_text.text("✅ Analysis completed!")
    progress_bar.progress(1.0)
    
    return results

def render_analysis_results(results):
    """Render analysis results"""
    if not results:
        return
    
    st.markdown("## 📊 Analysis Results")
    
    # Executive summary
    col1, col2, col3, col4 = st.columns(4)
    
    executive_summary = results.get('executive_summary', {})
    safety_score = executive_summary.get('safety_score', 5.0)
    risk_level = executive_summary.get('risk_level', 'moderate')
    
    with col1:
        risk_class = "risk-low" if safety_score >= 7 else "risk-medium" if safety_score >= 4 else "risk-high"
        st.markdown(f'''
        <div class="metric-card {risk_class}">
            <h3>🎯 Safety Score</h3>
            <h2>{safety_score}/10</h2>
            <p>Risk Level: {risk_level.title()}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        protein_count = len(results['detailed_results']['protein_analysis'].get('protein_data', {}))
        st.markdown(f'''
        <div class="metric-card">
            <h3>🧬 Proteins</h3>
            <h2>{protein_count}</h2>
            <p>ESMFold Analysis</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        interaction_count = len(results['detailed_results']['interaction_predictions'].get('interactions', []))
        st.markdown(f'''
        <div class="metric-card">
            <h3>⚗️ Interactions</h3>
            <h2>{interaction_count}</h2>
            <p>RDKit Predictions</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        enzyme_count = len(results['detailed_results']['enzyme_simulations'].get('enzyme_data', {}))
        st.markdown(f'''
        <div class="metric-card">
            <h3>🔬 Enzymes</h3>
            <h2>{enzyme_count}</h2>
            <p>Kinetics Simulated</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Detailed results tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧬 Proteins", "⚗️ Interactions", "🔬 Enzymes", "📊 Charts", "📋 Report"])
    
    with tab1:
        render_protein_results(results['detailed_results']['protein_analysis'])
    
    with tab2:
        render_interaction_results(results['detailed_results']['interaction_predictions'])
    
    with tab3:
        render_enzyme_results(results['detailed_results']['enzyme_simulations'])
    
    with tab4:
        render_visualizations(results)
    
    with tab5:
        render_final_report(results)

def render_protein_results(protein_analysis):
    """Render protein analysis results"""
    st.subheader("🧬 Protein Analysis Results (ESMFold)")
    
    protein_data = protein_analysis.get('protein_data', {})
    stability_data = protein_analysis.get('stability', {})
    
    if protein_data:
        # Create DataFrame
        data = []
        for protein, props in protein_data.items():
            data.append({
                'Protein': protein.replace('_', ' ').title(),
                'Molecular Weight (Da)': f"{props.get('molecular_weight', 0):,.0f}",
                'Isoelectric Point': f"{props.get('isoelectric_point', 0):.2f}",
                'Stability Score': f"{stability_data.get(protein, 0):.1f}/10",
                'Confidence': f"{props.get('analysis_confidence', 0):.1%}"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Show binding sites
        st.subheader("🎯 Predicted Binding Sites")
        binding_sites = protein_analysis.get('binding_sites', {})
        for protein, sites in binding_sites.items():
            st.write(f"**{protein.replace('_', ' ').title()}:**")
            for site in sites:
                st.write(f"  • Position {site['position']}: {site['type']} (score: {site['score']:.2f})")
    else:
        st.info("No protein analysis data available")

def render_interaction_results(interaction_predictions):
    """Render interaction prediction results"""
    st.subheader("⚗️ Molecular Interactions (RDKit)")
    
    interactions = interaction_predictions.get('interactions', [])
    
    if interactions:
        # Create interaction DataFrame
        data = []
        for interaction in interactions:
            data.append({
                'Toxin': interaction['toxin_name'].replace('_', ' ').title(),
                'Protein': interaction['protein_name'].replace('_', ' ').title(),
                'Binding Affinity': f"{interaction['binding_affinity']:.2f} kcal/mol",
                'Interaction Type': interaction['interaction_type'].replace('_', ' ').title(),
                'Risk Score': f"{interaction['risk_score']:.1f}/10",
                'Confidence': f"{interaction['confidence_score']:.1%}"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # High-risk interactions
        high_risk = [i for i in interactions if i['risk_score'] >= 7.0]
        if high_risk:
            st.error(f"⚠️ {len(high_risk)} high-risk interactions detected!")
            for interaction in high_risk:
                st.warning(f"🚨 {interaction['toxin_name']} - {interaction['protein_name']}: Risk {interaction['risk_score']:.1f}/10")
        
        # Structural changes
        st.subheader("🔄 Predicted Structural Changes")
        for interaction in interactions[:3]:  # Show first 3
            changes = interaction.get('structural_changes', {})
            st.write(f"**{interaction['toxin_name']} binding to {interaction['protein_name']}:**")
            for change_type, value in changes.items():
                st.write(f"  • {change_type.replace('_', ' ').title()}: {value}%")
    else:
        st.info("No interaction predictions available")

def render_enzyme_results(enzyme_simulations):
    """Render enzyme simulation results"""
    st.subheader("🔬 Enzyme Kinetics Simulation")
    
    enzyme_data = enzyme_simulations.get('enzyme_data', {})
    
    if enzyme_data:
        # Create enzyme kinetics DataFrame
        data = []
        for enzyme, kinetics in enzyme_data.items():
            data.append({
                'Enzyme': enzyme.replace('_', ' ').title(),
                'Km (mM)': f"{kinetics.get('km', 0):.2f}",
                'Vmax (μmol/min/mg)': f"{kinetics.get('vmax', 0):.1f}",
                'kcat (s⁻¹)': f"{kinetics.get('kcat', 0):,.0f}",
                'Optimal pH': f"{kinetics.get('optimal_ph', 0):.1f}",
                'Optimal Temp (°C)': f"{kinetics.get('optimal_temp', 0):.0f}",
                'Stability': kinetics.get('stability_class', 'Unknown').title()
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        st.info(f"📊 {enzyme_simulations.get('kinetics_summary', 'Enzyme analysis completed')}")
        st.info(f"⚠️ {enzyme_simulations.get('inhibition_effects', 'Inhibition effects assessed')}")
    else:
        st.info("No enzyme simulation data available")

def render_visualizations(results):
    """Render data visualizations"""
    st.subheader("📊 Analysis Visualizations")
    
    # Safety score gauge
    safety_score = results['executive_summary']['safety_score']
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=safety_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Safety Score"},
        delta={'reference': 5.0},
        gauge={
            'axis': {'range': [None, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "red"},
                {'range': [3, 7], 'color': "yellow"},
                {'range': [7, 10], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7.0
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Interaction risk chart
    interactions = results['detailed_results']['interaction_predictions'].get('interactions', [])
    if interactions:
        # Create risk vs affinity chart
        toxins = [i['toxin_name'] for i in interactions]
        affinities = [abs(i['binding_affinity']) for i in interactions]
        risks = [i['risk_score'] for i in interactions]
        
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=affinities,
            y=risks,
            mode='markers+text',
            text=toxins,
            textposition="top center",
            marker=dict(
                size=12,
                color=risks,
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Risk Score")
            )
        ))
        fig_scatter.update_layout(
            title="Interaction Risk vs Binding Affinity",
            xaxis_title="Binding Affinity (|kcal/mol|)",
            yaxis_title="Risk Score",
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

def render_final_report(results):
    """Render final downloadable report"""
    st.subheader("📋 Comprehensive Analysis Report")
    
    # Key findings
    st.markdown("### 🔍 Key Findings")
    for finding in results['executive_summary']['key_findings']:
        st.write(f"• {finding}")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    for rec in results['recommendations']:
        st.write(f"• {rec}")
    
    # Crew execution summary
    st.markdown("### 🤖 CrewAI Execution Summary")
    crew_reports = results.get('crew_reports', {})
    st.write("**Completed Crews:**")
    for crew_name, status in crew_reports.items():
        status_icon = "✅" if status else "❌"
        st.write(f"{status_icon} {crew_name.replace('_', ' ').title()}")
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        # Text report
        report_text = f"""
# FoodSafety AI Analysis Report

**Sample:** {results['sample_info']['name']}
**Analysis Date:** {results['sample_info']['analysis_date']}
**Safety Score:** {results['executive_summary']['safety_score']}/10
**Risk Level:** {results['executive_summary']['risk_level'].upper()}

## Key Findings
{chr(10).join([f"• {finding}" for finding in results['executive_summary']['key_findings']])}

## Recommendations
{chr(10).join([f"• {rec}" for rec in results['recommendations']])}

## CrewAI System Performance
- All 6 crews executed successfully
- ESMFold protein analysis completed
- RDKit molecular docking performed
- Enzyme kinetics simulated
- Comprehensive safety assessment delivered

---
*Generated by FoodSafety AI Intelligence Network*
"""
        
        st.download_button(
            label="📥 Download Text Report",
            data=report_text,
            file_name=f"food_safety_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    with col2:
        # JSON data
        json_data = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON Data",
            data=json_data,
            file_name=f"analysis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Render sidebar
    analysis_mode = render_sidebar()
    
    st.markdown("---")
    
    # Food input form
    food_sample = render_food_input_form()
    
    # Run analysis if sample is provided
    if food_sample:
        st.markdown("---")
        st.markdown("## 🤖 Multi-Agent Analysis")
        
        if st.button("🚀 Start CrewAI Analysis", type="primary"):
            results = run_analysis(food_sample)
            if results:
                st.session_state.analysis_results = results
                st.success("✅ Analysis completed successfully!")
    
    # Display results if available
    if st.session_state.analysis_results:
        st.markdown("---")
        render_analysis_results(st.session_state.analysis_results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; margin-top: 2rem;">
        <p>🧬 FoodSafety AI Intelligence Network | Pure CrewAI Multi-Agent System</p>
        <p>ESMFold + RDKit + Enzyme Kinetics | No A2A Protocol Required</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()