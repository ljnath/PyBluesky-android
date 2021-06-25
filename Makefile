# Makefile for PyBluesky android project
# author - ljnath (www.ljnath.com}

# Usage

ADB = adb
PYTHON = python
APK_NAME = PyBluesky__armeabi-v7a-debug-1.0.0-.apk
PACKAGE_NAME = com.ljnath.pybluesky
ACTIVITY_NAME = org.kivy.android.PythonActivity

all: compile uninstall install start

compile:
	@echo Compiling project
	${PYTHON} setup.py apk

reinstall: uninstall install

uninstall:
	@echo Un-installing app with package name ${PACKAGE_NAME} from target device
	${ADB} uninstall ${PACKAGE_NAME}

install:
	@echo Installing ${APK_NAME} in target device
	${ADB} install ${APK_NAME}

start:
	@echo Starting ${APK_NAME} in target device
	${ADB} shell am start -n ${PACKAGE_NAME}/${ACTIVITY_NAME}

reset: clean update

clean:
	@echo Deleting ${APK_NAME}
	rm -f ${APK_NAME} 

update:
	@echo Cleaning local changes before updating codebase
	git reset --hard
	@echo Updating codebase
	git pull

help:
	@echo -------------------------------------------
	@echo PyBluesky makefile : available usages
	@echo -------------------------------------------
	@echo make 			: Default operations to compile project, uninstall apk from attached device, install new apk and start it
	@echo make -k		: Same as default, but it will configure with the next dependency even if a dependency fails
	@echo make compile	: Compile PyBluesky project using setup.pyc
	@echo make uninstall: Uninstall apk from attached android device using adb
	@echo make install	: Install apk into attached android device using adb
	@echo make start	: Start apk in the attached android device using adb
	@echo make clean	: Clean up already build apk file
	@echo -------------------------------------------
