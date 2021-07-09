# Makefile for PyBluesky android project
# author - ljnath (www.ljnath.com}

# Usage

ADB = adb
PYTHON = python
ARCHITECTURE = armeabi-v7a
VERSION = 1.0.0
APK_NAME = PyBluesky__${ARCHITECTURE}-debug-${VERSION}-.apk
PACKAGE_NAME = com.ljnath.pybluesky
ACTIVITY_NAME = org.kivy.android.PythonActivity

all: compile uninstall_apk install_apk run_apk

compile:
	@echo Compiling project
	${PYTHON} setup.py apk

reinstall: uninstall install

uninstall_apk:
	@echo Un-installing app with package name ${PACKAGE_NAME} from target device
	${ADB} uninstall ${PACKAGE_NAME}

install_apk:
	@echo Installing ${APK_NAME} in target device
	${ADB} install ${APK_NAME}

run_apk:
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
	@echo make uninstall_apk: Uninstall apk from attached android device using adb
	@echo make install_apk	: Install apk into attached android device using adb
	@echo make run_apk	: Start apk in the attached android device using adb
	@echo make reset	: clean + update
	@echo make clean	: Clean up already build apk file
	@echo make update	: Reset local code repo and update with github
	@echo -------------------------------------------
