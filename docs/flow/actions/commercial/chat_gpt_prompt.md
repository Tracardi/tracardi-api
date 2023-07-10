# ChatGPT prompt

The ChatGPT prompt plugin sends a request to ChatGPT and returns the response.

## Description

The ChatGPT prompt plugin utilizes the OpenAI GPT-3 model to generate text based on a given prompt. It sends a request
to the ChatGPT API, providing a prompt as input, and retrieves the generated response. The prompt can include references
to data from the payload using the `{{ }}` placeholder syntax. The generated response is returned as the output of the
plugin.

This documentation is for version 0.8.1 of the ChatGPT prompt plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the generated response from ChatGPT if the request is successful. The response is provided as a
  dictionary with two fields:
    - "answer": Contains the generated text.
    - "response": Contains the raw response from the ChatGPT API.
- **error**: Returns an error message if an error occurs during the execution of the plugin.

# Configuration

The ChatGPT prompt plugin has the following configuration parameters:

- **ChatGPT Resource**: Select the ChatGPT resource from the available options. This resource represents the API key
  required to access the ChatGPT API.
- **ChatGPT Prompt**: Enter the prompt to be used for generating the response. The prompt can include references to data
  from the payload using the `{{ }}` placeholder syntax.
- **Select engine type**: Select the engine type to be used for generating the response. Available options are:
    - Davinci
    - Curie
    - Babbage
    - Ada
- **Temperature**: Set the sampling temperature to control the randomness of the generated text. Higher values (e.g.,
  0.8) make the output more random, while lower values (e.g., 0.2) make it more focused and deterministic.

# Required resources

This plugin requires the configuration of a ChatGPT resource. The ChatGPT resource represents the API key required to
access the ChatGPT API.

# Errors

The ChatGPT prompt plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the execution of the plugin. The error message
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.