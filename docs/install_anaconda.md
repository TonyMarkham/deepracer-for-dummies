# **DeepRacer-For-Dummies - Install Anaconda**

1. Download Anaconda:

    ```terminal
    sudo apt-get update -y && \
        sudo apt-get upgrade -y && \
        cd /tmp/ && \
        sudo wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
    ```

2. Install Anaconda:

    ```terminal
    bash Anaconda3-2019.03-Linux-x86_64.sh
    ```

3. Go back to your `HOME` directory:

    ```terminal
    cd ~
    ```

4. Activating Anaconda:

    ```terminal
    source ~/.bashrc
    ```

5. Verifying the conda package manager works:

    ```terminal
    conda list
    ```

6. Installing CUDA/CUDNN:

    ```terminal
    conda install cudnn==7.3.1 && conda install -c fragcolor cuda10.0
    ```

[Back to readme](../README.md)
