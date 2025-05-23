# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate an image with background removal with the
Amazon Titan Image Generator G1 V2 model (on demand).
"""
import base64
import io
import json
import logging
import boto3
import sys
import os
from PIL import Image

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator V2"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_image(model_id, body):
    """
    Generate an image using Amazon Titan Image Generator V2 model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        image_bytes (bytes): The image generated by the model.
    """

    logger.info(
        "Generating image with Amazon Titan Image Generator V2 model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator V2 model %s", model_id)

    return image_bytes


def main(pin_image_path):
    """
    Entrypoint for Amazon Titan Image Generator V2 example.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-image-generator-v2:0'

        # Read image from file and encode it as base64 string.
        with open(pin_image_path, "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": input_image,
            }
        })

        image_bytes = generate_image(model_id=model_id,
                                     body=body)
        image = Image.open(io.BytesIO(image_bytes))
        # image.show()
        #image.save("images/Dog_edit.png")
        output_image_path = os.path.join(os.path.dirname(pin_image_path), os.path.basename(pin_image_path).split('.')[0] + '_edit.png').replace('\\', '/')
        print ("output path: " + output_image_path)
        image.save(output_image_path)
        #print(f"output image path {output_image_path}.")
        #return output_image_path
       

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(f"Finished generating image with Amazon Titan Image Generator V2 model {model_id}.")
        print(f"output image path {output_image_path}.")
        return output_image_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the input image file as an argument.")
        sys.exit(1)

    input_image_path = sys.argv[1]
    main(input_image_path)