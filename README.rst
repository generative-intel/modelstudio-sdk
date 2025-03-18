=================
ModelStudio SDK
=================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License
    :target: https://opensource.org/licenses/MIT

A Python SDK for interacting with ModelStudio, a platform for generative AI model management and deployment.

Description
==========

ModelStudio SDK is a Python client library that provides a convenient interface to the ModelStudio platform. It enables developers to programmatically manage, deploy, and interact with generative AI models within the ModelStudio ecosystem.

This SDK simplifies the process of integrating generative AI capabilities into your applications, allowing you to:

* Manage model deployments and configurations
* Run inference on deployed models
* Monitor model performance and usage
* Automate workflows for model training and deployment
* Access ModelStudio's features through a Pythonic API

The SDK is designed for data scientists, ML engineers, and developers who want to incorporate ModelStudio's generative AI capabilities into their applications or workflows.

Installation
===========

From GitHub
----------

Install the latest version directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/generative-intel/modelstudio-sdk.git@master

For development installation (editable mode):

.. code-block:: bash

    pip install -e git+https://github.com/generative-intel/modelstudio-sdk.git@master#egg=modelstudio-sdk

Alternatively, clone the repository and install:

.. code-block:: bash

    git clone https://github.com/generative-intel/modelstudio-sdk.git
    cd modelstudio-sdk
    pip install -e .

Usage
=====

Command Line Interface
--------------------

The ModelStudio SDK includes a command-line tool for image prediction. After installation, you can use the `modelstudio` command:

.. code-block:: bash

    # Get help and available commands
    modelstudio --help

    # View version information
    modelstudio --version

    # Predict using images
    modelstudio predict --url "<YOUR-MODELSTUDIO-PROJECT-URL>" \
                        --api_key "<YOUR-MODELSTUDIO-PROJECT-API_KEY>" \
                        --images image1.jpg image2.png \
                        --timeout 10 \
                        --max_retries 3 \
                        --base_delay 2

Command options for `predict`:

* ``--url``: Project specific API URL (required)
* ``--api_key``: Project specific API key (required)
* ``--images``: List of image paths to analyze (required)
* ``--timeout``: Request timeout in seconds (default: 10)
* ``--max_retries``: Maximum number of retry attempts (default: 3)
* ``--base_delay``: Base delay between retries in seconds (default: 2)

Logging options:

* ``-v, --verbose``: Set log level to INFO
* ``-vv, --very-verbose``: Set log level to DEBUG

Python SDK Examples
------------------

.. code-block:: python

    from modelstudio_sdk.predictor import ModelStudioPredictor

    # Initialize predictor with your API credentials
    predictor = ModelStudioPredictor(
        url="https://<YOUR_URL>",
        api_key="<YOUR_KEY>",
        timeout=10,
        max_retries=3,
        base_delay=2
    )

    # Run prediction on an image
    prediction = predictor.predict("path/to/image.jpg")
    print(prediction)

    # Process multiple images
    from modelstudio_sdk.predictor import read_images

    for name, img_path in read_images(["image1.jpg", "image2.png"]):
        prediction = predictor.predict(img_path)
        print(name, prediction)

Requirements
===========

* Python 3.7+
* Dependencies are automatically installed with the package

Contributing
===========

Contributions are welcome! Please feel free to submit a Pull Request.

License
=======

This project is licensed under the terms of the MIT license.