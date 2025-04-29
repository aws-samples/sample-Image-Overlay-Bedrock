## Overview

> **⚠️ WARNING: This application is for demonstration and learning purposes only. It is NOT intended for production use.**

# Image Overlay Bedrock

A web application that uses AWS Bedrock AI services to remove image backgrounds, overlay images, and generate AI-powered advertising content.

![Image Overlay Example](image_insertion/images/Image-Overlay-Bedrock.gif)

## Overview

Image Overlay Bedrock is a Streamlit-based web application that demonstrates the power of AWS Bedrock AI services for image manipulation and content generation. The application allows users to:

1. Upload a foreground image (Initial image)
2. Upload a background image (Advertiser image)
3. Remove the background from the foreground image using Amazon Titan Image Generator
4. Overlay the foreground onto the background with customizable positioning and scaling
5. Generate advertising content for the combined image using Claude 3.5 Sonnet

## Features

- **Background Removal**: Uses Amazon Titan Image Generator V2 to automatically remove backgrounds from images
- **Image Overlay**: Positions and scales foreground images onto background images
- **AI-Generated Ad Content**: Leverages Claude 3.5 Sonnet to create advertising content for the combined image
- **Interactive UI**: Streamlit-based interface with controls for image positioning and scaling

## Prerequisites

- Python 3.8+
- AWS account with access to Bedrock services
- AWS CLI configured with appropriate permissions

## Installation

1. Clone the repository:
   ```
   git clone https://gitlab.aws.dev/sidvan/Image-Overlay-Bedrock.git
   cd Image-Overlay-Bedrock
   ```

2. Install the required dependencies:
   ```
   pip install -r image_insertion/requirements.txt
   pip install streamlit
   ```

3. Configure AWS credentials:
   ```
   aws configure
   ```
   Ensure your AWS credentials have access to Bedrock services.

## Usage

1. Start the Streamlit application:
   ```
   cd image_insertion
   streamlit run app.py
   ```

2. Access the application in your web browser (typically at http://localhost:8501)

3. Upload your initial image and Advertiser image, or use the default images. Make sure to validate that the file uploaded are in a supported image format. (jpg, jpeg, png)

4. Adjust the mask settings to position and scale the foreground image

5. Click "Generate" to process the images and create the advertising copy

## Project Structure

```
image_insertion/
├── app.py                  # Main Streamlit application
├── background_removal.py   # Background removal using Amazon Titan Image Generator V2
├── overlay.py              # Image overlay functionality
├── imagetotext.py          # Ad content generation using Claude 3.5 Sonnet
├── requirements.txt        # Python dependencies
├── images/                 # Sample and output images
└── output.txt              # Generated ad copy output
```

## AWS Services Used

- **Amazon Bedrock**: Foundation model service for AI capabilities
- **Amazon Titan Image Generator V2**: For background removal
- **Anthropic Claude 3.5 Sonnet**: For generating advertising content

## Examples

The repository includes sample images for testing:
- Dog.png: Sample image
- gazebo2.jpg: Sample advertiser image
- dog_output.png: Sample output of the combined images

## Contributing

Contributions to improve Image Overlay Bedrock are welcome. Please feel free to submit a pull request or open an issue to discuss potential changes or enhancements.


