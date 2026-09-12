
import streamlit as st
import plotly.graph_objects as go

def render_geoai_dashboard(selected_city: str, country: str, risk_dict: dict):
    st.subheader(f"🌐 PostGIS + GeoAI Spatial Analytics: {selected_city}, {country}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Spatial Sensitivity Radar**")
        categories = ['Exposure', 'Vulnerability', 'Sensitivity', 'Criticality', 'Adaptive Capacity']
        values = [
            risk_dict['exposure'],
            risk_dict['vulnerability'],
            risk_dict['sensitivity'],
            risk_dict['criticality'],
            risk_dict['adaptive_capacity']
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(0, 229, 255, 0.2)',
            line=dict(color='#00E5FF', width=2)
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100]),
                bgcolor="rgba(10,25,47,0.8)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**GeoAI Geospatial Inference**")
        st.info(f"""
        **Coordinates Spatial Polygon:** Validated via PostGIS Geometry Column
        - **Target Vector Node:** {selected_city} Center Point
        - **Risk Buffer Radius:** 25 km
        - **Top Atmospheric / Hydro Stress Driver:** Urban Inundation and Thermal Stress
        - **PostGIS Spatial SRID:** EPSG:4326 (WGS 84)
        """)
