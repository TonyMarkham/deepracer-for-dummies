# DeepRacer-For-Dummies

## **Content**

* [1. Install Ubuntu](#Install-Ubuntu)

## **Install Ubuntu**

1. Create a `git` sub-directory in your `HOME` directory:

    ```terminal
    sudo mkdir $HOME/git && \
    sudo chown $USER:$USER $HOME/git
    ```

2. Install `gparted`.

    ```terminal
    sudo apt-get install -y gparted
    ```

3. Start `gparted`.

    ```terminal
    sudo gparted
    ```

4. In the top-Right corner of the `gparted` window, select the hard drive that you want to mount.
5. `Right-Click` on the partition that you want to mount and select `information`.
6. Add this partition to your `git` sub-directory:

    ```terminal
    UUID=1f2d0d30-f4c5-4c1c-8de2-f0fd2fdd1cb0 && \
    echo "UUID=\"${UUID}\"  ${HOME}/git  ext4  defaults  0  0" | sudo tee -a /etc/fstab && \
    sudo mount -a
    ```

7. Confirm that it allocated properly:

    ```terminal
    sudo df -h $HOME/git
    ```

    You should see output that looks like this:

    ```terminal
    abc
    ```
