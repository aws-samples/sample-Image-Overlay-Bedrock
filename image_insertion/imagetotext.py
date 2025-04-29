# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to send an image with the <noloc>Converse</noloc> API to Anthropic Claude 3 Sonnet (on demand).
"""

import logging
import boto3


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_conversation(bedrock_client,
                          model_id,
                          input_text,
                          input_image):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        input text : The input message.
        input_image : The input image.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Message to send.

    with open(input_image, "rb") as f:
        image = f.read()

    message = {
        "role": "user",
        "content": [
            {
                "text": input_text
            },
            {
                    "image": {
                        "format": 'png',
                        "source": {
                            "bytes": image
                        }
                    }
            }
        ]
    }

    messages = [message]

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages
    )

    return response


def main(input_image_path=None):
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    
    Args:
        input_image_path (str, optional): Path to the input image. Defaults to "./images/dog_output.png".
        
    Returns:
        str: The generated advertisement text
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    #model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    input_text = """Create a Pinterest-style advertisement for {input_text}. The ad should include:

STRUCTURE:
- Attention-grabbing opening line with emojis
- 3-4 key product features as bullet points 
- Main use cases prefixed with ✨
- Relevant hashtags
- Clear call-to-action

STYLE REQUIREMENTS:
- Use aspirational, luxury-focused tone
- Include emojis strategically
- Keep text scannable and concise
- Focus on lifestyle benefits
- Highlight materials and dimensions
- Emphasize ambiance/aesthetics
- Use power words (premium, elegant, stunning)

FORMAT:
- Bold all lines
- Organized bullet points
- Strategic spacing
- Hashtags at end

The final output should read like an engaging social media post that drives interest and engagement.**
"""

    # Use provided image path or default
    if input_image_path is None:
        input_image = "./images/dog_output.png"
    else:
        input_image = input_image_path

    generated_text = ""
    
    try:
        bedrock_client = boto3.client(service_name="bedrock-runtime")

        response = generate_conversation(
            bedrock_client, model_id, input_text, input_image)

        output_message = response['output']['message']

        print(f"Role: {output_message['role']}")

        for content in output_message['content']:
            generated_text = content['text']
            # print(f"Text: {generated_text}")
            # save Text to file
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(generated_text)

        token_usage = response['usage']
        # print(f"Input tokens:  {token_usage['inputTokens']}")
        # print(f"Output tokens:  {token_usage['outputTokens']}")
        # print(f"Total tokens:  {token_usage['totalTokens']}")
        # print(f"Stop reason: {response['stopReason']}")

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")
        return "Error generating advertisement text."

    else:
        print(f"Finished generating text with model {model_id}.")
        
    return generated_text


if __name__ == "__main__":
    main()
