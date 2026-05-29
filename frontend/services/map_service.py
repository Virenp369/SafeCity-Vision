import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def render_heatmap(df, current_context, height=450):
    required_columns = {'Latitude', 'Longitude'}
    if df.empty or not required_columns.issubset(df.columns):
        return

    map_df = df.dropna(subset=['Latitude', 'Longitude'])
    if map_df.empty:
        return

    center_lat = map_df['Latitude'].mean()
    center_lon = map_df['Longitude'].mean()
    zoom = 5 if "INDIA" in current_context else 10
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB dark_matter", control_scale=True)
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in map_df.iterrows()]
    HeatMap(heat_data, radius=18 if zoom == 10 else 22, blur=15, gradient={0.2: '#0EA5E9', 0.5: '#EAB308', 1: '#EF4444'}).add_to(m)
    
    # Optimize by setting returned_objects=[] to prevent map interactions from causing full app reruns
    st_folium(m, height=height, use_container_width=True, returned_objects=[])
