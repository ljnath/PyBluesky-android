# BUILD GUIDE

## WINDOWS

Start with the installation of the cs-Freeze package for building the windows binary and package.
Install the following command
```
pip install cx-Freeze==6.1
```

For creating ```msi``` setup file as the final build output, invoke the following command
```
python setup.py bdist_msi
```

## ANDROID
### Pre-requisites
* Ubuntu
* Python 3.7.6 (also works withh 3.8.5) ; need to complile
* virtualenv
* python-for-android python package
* JDK 8


### Steps

Prepare a ubuntu VM with ample disk space and good number of CPU and memory.

1. Install the required packages

```
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y build-essential ccache git zlib1g-dev python3 python3-dev libncurses5:i386 libstdc++6:i386 zlib1g:i386 openjdk-8-jdk unzip ant ccache autoconf libtool libssl-dev libffi-dev
```

2. Download and compile python

```
# install required packages
sudo apt-get update
sudo apt-get install -y build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

# Download python sources to /usr/src
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz

# extarct downloaded python sources
sudo tar xzf Python-3.7.6.tgz

# compile sources
cd Python-3.7.6
sudo ./configure --enable-optimizations

# building python
sudo make altinstall

# verify python
python3.7 --version
```

3. Download Andorid SDK
```
# create directory structure
mkdir -p ~/Desktop/android-sdk/cmdline-tools

# download archive
wget https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip

# extract archive
unzip commandlinetools-linux-7302050_latest.zip

# cleanup file
rm commandlinetools-linux-7302050_latest.zip

# rename extracted directory
mv cmdline-tools tools

# add sdkmanager and future android to PATH variable
export PATH=~/Desktop/android-sdk/tools:~/Desktop/android-sdk/cmdline-tools/tools/bin:$PATH
```

4. Download Android NDK
```
# change directory to user desktop
cd ~/Desktop

# download archive
https://dl.google.com/android/repository/android-ndk-r19c-linux-x86_64.zip

# extract archive
unzip android-ndk-r19c-linux-x86_64.zip

# cleanup file
rm android-ndk-r19c-linux-x86_64.zip
```

5. Download android platform and build-tools
```
sdkmanager "platforms;android-28"
sdkmanager "platforms;android-29"
sdkmanager "build-tools;28.0.2"
sdkmanager "build-tools;29.0.0"
```

6. Setup python virtual environment
```
cd ~/Desktop

# create python virutual environment with python 3.7.6
python3.7 -m venv p4a-env

# activate python virtual environment
source p4a-env/bin/activate

# install required packages
pip instal wheel cython python-for-android

# verify the installation of python-for-android package
p4a --versoin
```

7. Build apk using p4a
```
# python project is places at ~/Desktop/PyBluesky
# --requirements : all the requiremenents packages listed in the requirements.txt file is listed here
#

p4a apk --private ~/Desktop/PyBluesky --requirements=pygame==2.0.0-dev7,aiohttp==3.7.4.post0,multidict==5.1.0,attrs==21.2.0,async-timeout==3.0.1,chardet==4.0.0,idna==3.2,typing-extensions==3.10.0.0,yarl==1.6.3 --icon /home/ljnath/Desktop/PyBluesky/assets/images/jet.png --sdk-dir ~/Desktop/android-sdk --ndk-dir ~/Desktop/android-ndk-r19c --android-api 28 --ndk-api 21 --ignore-setup-py --package=com.ljnath.pybluesky --name "PyBluesky" --version 1.0 --bootstrap=sdl2 --dist_name=PyBluesky --orientation=landscape
```

8. Build apk using setup.py file
```
cd ~/Desktop/PyBluesky
python setup.py apk
```