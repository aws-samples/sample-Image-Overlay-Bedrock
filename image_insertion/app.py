import streamlit as st
from io import BytesIO
from background_removal import main as background_removal_main
from overlay import overlay_image as overlay_image
from imagetotext import main as imagetotext_main

def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io

st.set_page_config(layout="wide", page_title="Image Overlay")
st.title("Image Overlay")

col1, col2, col3, col4 = st.columns(4)

placement_options_dict = { #Configure mask areas for image insertion
    "Dog image": (100, 0, 1.2), #x, y, width, height
}

placement_options = list(placement_options_dict)

with col1:
    st.subheader("Initial image")
    uploaded_file_pin = st.file_uploader("Upload your image", type=['png', 'jpg'], key='pin')
    
    # Make sure you validate the input image being uploaded
    if uploaded_file_pin:
        uploaded_image_preview = get_bytesio_from_bytes(uploaded_file_pin.getvalue())
        st.image(uploaded_image_preview)
        pin_image_path = './images/' + uploaded_file_pin.name
    else:
        st.image("images/Dog.png") 
        pin_image_path = "./images/Dog.png"
        

with col2:
    st.subheader("Advertiser image")  
    uploaded_file_ad = st.file_uploader("Upload your image", type=['png', 'jpg'], key = 'ad')

    # Make sure you validate the input image being uploaded
    if uploaded_file_ad:
        uploaded_image_preview = get_bytesio_from_bytes(uploaded_file_ad.getvalue())
        st.image(uploaded_image_preview)
        ad_image_path = './images/' + uploaded_file_ad.name
    else:
        st.image("images/gazebo2.jpg")
        ad_image_path = "./images/gazebo2.jpg" 

with col3:
    st.subheader("Mask Settings")
    with st.expander("Mask Settings"):
        mask_x = st.number_input("Mask X Position", value=100, step=10)
        mask_y = st.number_input("Mask Y Position", value=0, step=10)
        scale = st.number_input("Scale Factor", value=1.2, step=0.1, min_value=0.1)
    
    generate_button = st.button("Generate", type="primary")

with col4: 
    st.subheader("Result")
    if generate_button:  
            background_removed_image = background_removal_main (pin_image_path)
            output_image = "./images/dog_output.png"
            coordinates = (mask_x, mask_y)  # x, y position where overlay is placed on the background
            scale_factor = scale  # Example: 1.5 means increasing the size by 50%
            overlayimage = overlay_image(ad_image_path, background_removed_image, output_image, coordinates, scale_factor)
            st.image(output_image)
            # Generate ad copy directly by calling imagetotext_main with the output image path
            ad_copy = imagetotext_main(output_image)
            st.write(ad_copy)

