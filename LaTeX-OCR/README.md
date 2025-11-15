#LaTex-OCR

## Latex OCR build with DeepSeek-OCR hosted locally

LaTeX-OCR is a tool that leverages DeepSeek-OCR to automatically extract LaTeX code from images of mathematical content. This project enables users to quickly convert screenshots, handwritten notes, or printed formulas into editable LaTeX format with high accuracy, all running locally without requiring cloud services. This project is meant for educational purposes and configured to process one request at a time

# Installation for Ubuntu

You need to have an NVIDIA (or compatible) driver with the Nvidia Container Toolkit (NC) installed on your host machine. You can find detailed description of how to install it down below. I'm currently using a third-party Docker image for running DeepSeek-OCR that has slightly older versions of Python (3.10) and CUDA (12.1.1). If you want to run the app directly on your machine, or wish to use the versions recommended by DeepSeek, please refer to the official [DeepSeek-OCR HuggingFace page](https://huggingface.co/deepseek-ai/DeepSeek-OCR). 

Follow these steps to build and run the LaTeX-OCR application using Docker. It might take quite some time to build and run the model first time.
It's no where near optimized and takes 23.4GB of disc space after build:

1.  **Navigate to the Application Directory**:
    Open your terminal and change to the `app` directory within the `LaTeX-OCR` folder.
    ```bash
    cd LaTeX-OCR/app
    ```

2.  **Build the Docker Image**:
    Run the following command to build the Docker image. We'll tag it as `latex-ocr-app` for easy reference.
    ```bash
    docker build -t latex-ocr-app .
    ```

3.  **Run the Docker Container**:
    Once the image is built, you can start the container. The `--gpus all` flag is essential as it gives the container access to your NVIDIA GPU, which is required by `vllm`.
    ```bash
    docker run --gpus all -p 8501:8501 latex-ocr-app
    ```

4.  **Access the Application**:
    Open your web browser and navigate to `http://localhost:8501` to use the LaTeX-OCR application.

# Docker setup

This guide will walk you through installing Docker Engine and the NVIDIA Container Toolkit on Ubuntu.

### Docker Engine

1.  **Set up Docker's `apt` repository**:
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

2.  **Install the Docker packages**:
    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

3.  **Verify the installation**:
    Run the `hello-world` image to confirm that Docker is installed correctly.
    ```bash
    sudo docker run hello-world
    ```

### NVIDIA Container Toolkit

1.  **Set up the NVIDIA repository**:
    ```bash
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```

2.  **Install the toolkit**:
    This pins the toolkit to a specific version for stability.
    ```bash
    sudo apt-get update
    export NVIDIA_CONTAINER_TOOLKIT_VERSION=1.17.8-1
    sudo apt-get install -y \
      nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}
    ```

3.  **Configure Docker**:
    Restart the Docker daemon to apply the new configuration.
    ```bash
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    ```

4.  **Verify the installation**:
    Run a base CUDA container and execute `nvidia-smi` to confirm that the GPU is accessible.
    ```bash
    sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
    ```

    

## call for action.

feel free to contact me with any questions

