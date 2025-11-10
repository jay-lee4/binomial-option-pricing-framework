import streamlit as st
from src.export import (
    export_results_to_csv,
    export_parameters_to_json,
    export_optimization_to_csv,
    export_simulation_data_to_csv,
    create_full_export_package
)


def display_export_section(results, inputs, opt_results=None):
    """
    Display export options for all data.
    
    Args:
        results: Calculation results
        inputs: User inputs
        opt_results: Optimization results (optional)
    """
    st.markdown("### Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Results")
        results_csv = export_results_to_csv(results, inputs)
        st.download_button(
            label="Download Results (CSV)",
            data=results_csv.to_csv(index=False),
            file_name="options_results.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("#### Parameters")
        params_json = export_parameters_to_json(inputs)
        st.download_button(
            label="Download Parameters (JSON)",
            data=params_json,
            file_name="options_parameters.json",
            mime="application/json"
        )
    
    with col3:
        st.markdown("#### Simulation Data")
        sim_csv = export_simulation_data_to_csv(results['simulation'])
        st.download_button(
            label="Download Simulation (CSV)",
            data=sim_csv.to_csv(index=False),
            file_name="options_simulation.csv",
            mime="text/csv"
        )
    
    # Optimization export if available
    if opt_results:
        st.divider()
        st.markdown("#### Optimization Results")
        opt_csv = export_optimization_to_csv(opt_results)
        st.download_button(
            label="Download Optimization (CSV)",
            data=opt_csv.to_csv(index=False),
            file_name="options_optimization.csv",
            mime="text/csv"
        )
    
    st.divider()
    
    # Full package export
    st.markdown("#### Complete Export Package")
    st.info("Download all data in a single ZIP file")
    
    if st.button("Prepare Full Export"):
        package = create_full_export_package(results, inputs, opt_results)
        
        # For now, just show what would be exported
        st.success("Export package prepared!")
        st.write("Package includes:")
        st.write("- Results CSV")
        st.write("- Parameters JSON")
        st.write("- Simulation CSV")
        if opt_results:
            st.write("- Optimization CSV")
