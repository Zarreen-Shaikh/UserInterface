import streamlit as st
import requests
from PIL import Image
import io
import matplotlib.pyplot as plt # type: ignore
import geopandas as gpd # type: ignore

# Set title for the app
st.title("SAR Image Colorization Web App")

# Sidebar info
st.sidebar.header("Upload SAR Image")
st.sidebar.markdown("Please upload your SAR image to be colorized.")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Choose a SAR Image", type=["png", "jpg", "jpeg"])

# Add a button to start the colorization process
if uploaded_file is not None:
    # Display the uploaded image in the main area
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded SAR Image", use_column_width=True)
    
    # Colorization button
    if st.sidebar.button('Start Colorization'):
        # Display spinner while processing
        with st.spinner('Processing...'):
            # Convert image to bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            # Send image to Flask API for processing
            response = requests.post("http://127.0.0.1:5000/colorize", files={"file": img_bytes})

            # If request is successful
            if response.status_code == 200:
                # Load colorized image from response
                colorized_img = Image.open(io.BytesIO(response.content))
                
                # Display colorized image
                st.image(colorized_img, caption="Colorized SAR Image", use_column_width=True)
            else:
                st.error("Error processing the image. Please try again.")
else:
    st.warning("Please upload an image to proceed.")

# Display geo data or any additional visualizations using GeoPandas
st.sidebar.header("Visualization Options")
show_geospatial_data = st.sidebar.checkbox("Show Geospatial Data")

if show_geospatial_data:
    st.markdown("### Geospatial Data")
    # Load and display some sample geospatial data (replace with actual data in the future)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    st.write(world[["name", "continent", "geometry"]])
    
    # Plot geospatial data
    fig, ax = plt.subplots(figsize=(10, 6))
    world.boundary.plot(ax=ax)
    st.pyplot(fig)
