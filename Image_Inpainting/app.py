import streamlit as st
import torch
import numpy as np
from PIL import Image
from PIL import ImageEnhance
import torchvision.transforms as transforms
from model import PartialConvUNet
import cv2

# Set up the app
st.set_page_config(page_title="Image Inpainting", layout="wide")
st.title("Image Inpainting with Partial Convolutional UNet")

@st.cache_resource
def load_model():
    model = PartialConvUNet()
    model.load_state_dict(torch.load("model.pth", map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()

def create_random_mask(image_dims, n_channels=3):
    """Create random mask with lines similar to the Dataset class"""
    mask = np.full((image_dims[0], image_dims[1], n_channels), 255, dtype=np.uint8)
    for _ in range(np.random.randint(1, 10)):
        x1, x2 = np.random.randint(1, image_dims[0]), np.random.randint(1, image_dims[0])
        y1, y2 = np.random.randint(1, image_dims[1]), np.random.randint(1, image_dims[1])
        thickness = np.random.randint(10, 13)
        cv2.line(mask, (x1, y1), (x2, y2), (1, 1, 1), thickness)
    return mask

def preprocess_image(image, mask=None):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2470, 0.2435, 0.2616])
    ])
    
    image = transform(image)
    if mask is not None:
        mask = transforms.Resize((256, 256))(Image.fromarray(mask))
        mask = transforms.ToTensor()(mask)
        return image.unsqueeze(0), mask.unsqueeze(0)
    return image.unsqueeze(0)

def postprocess_image(tensor):
    tensor = tensor.squeeze(0).cpu().detach()
    tensor = tensor * 0.5 + 0.5  # Un-normalize
    tensor = torch.clamp(tensor, 0, 1)
    image = transforms.ToPILImage()(tensor)

    # Increase color saturation
    enhancer = ImageEnhance.Color(image)
    enhanced_image = enhancer.enhance(2)  # >1 boosts saturation (1.5 = 50% more)

    return enhanced_image

# Main app
col1, col2 = st.columns(2)

with col1:
    st.header("Input Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Original Image")
        
        if st.button("Generate Random Mask and Inpaint"):
            # Create random mask
            original_size = image.size
            mask = create_random_mask((original_size[1], original_size[0]))  # (height, width)
            
            # Display the mask
            st.image(mask, caption="Generated Mask")


            st.image(image, caption="Original Image")

            
            # Preprocess image and mask
            input_image, input_mask = preprocess_image(image, mask)
            
            # Run inference
            with st.spinner("Inpainting in progress..."):
                with torch.no_grad():
                    output = model(input_image, input_mask)
                
                # Postprocess and display
                result_image = postprocess_image(output)
                
                
                st.header("Inpainted Result")
                st.image(result_image, caption="Inpainted Image")

# Add some app info
st.sidebar.markdown("""
### About this app
This app uses a Partial Convolutional UNet to perform image inpainting.

1. Upload an image
2. Click "Generate Random Mask and Inpaint" to:
   - Automatically create a random mask
   - Show the inpainted result

The mask is generated with random lines similar to the training process.
""")