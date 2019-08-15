# DeepRacer-For-Dummies

## **Content**

* [1. Install Ubuntu](#Install-Ubuntu)

## **Install Ubuntu**

1. Install `gparted`.

    ```terminal
    sudo apt-get install -y gparted
    ```

2. Start `gparted`.

    ```terminal
    sudo gparted
    ```

3. In the top-Right corner of the `gparted` window, select the hard drive that you want to mount.
4. `Right-Click` on the partition that you want to mount and select `information`.
5. Add this partition to your `HOME` directory as the `git` sub-directory:

    ```terminal
    UUID=1f2d0d30-f4c5-4c1c-8de2-f0fd2fdd1cb0 && \
    printf "UUID=${UUID}  ${HOME}/git  ext4  default  0  0\n" | sudo tee -a /etc/fstab && \
    sudo mount -a
    ```
