# Makefile for PyBluesky android project
# author - ljnath (www.ljnath.com}

# variables used for building project
ACTIVITY_NAME   = org.kivy.android.PythonActivity
ADB				= adb
ARCHITECTURE    = arm64-v8a
APK_NAME        = PyBluesky
PACKAGE_NAME    = com.ljnath.pybluesky
PYTHON			= python
RELEASE_TYPE    = debug
VERSION         = 1.0.0

ifeq (${RELEASE_TYPE}, debug)
	APK_FILE    = ${APK_NAME}__${ARCHITECTURE}-${RELEASE_TYPE}-${VERSION}-.apk
else ifeq (${RELEASE_TYPE}, release)
	APK_FILE    = ${APK_NAME}__${ARCHITECTURE}-${RELEASE_TYPE}-unsigned-${VERSION}-.apk
endif

# variables used for signing
JAR_SIGNER      = jarsigner
SIGALG          = 
DIGESTALG       = 
KEYSTORE_FILE   = 
KEYSTORE_ALIAS  = 

# variables used for zipalign
ZIPALIGN        = 
FINAL_APK       = ${APK_NAME}_${ARCHITECTURE}-${RELEASE_TYPE}-signed-${VERSION}.apk


# Targets

all: compile uninstall install run

compile:
	@echo Compiling project
	${PYTHON} setup.py apk

reinstall: uninstall install

uninstall:
	@echo Un-installing app with package name ${PACKAGE_NAME} from target device
	${ADB} uninstall ${PACKAGE_NAME}

install:
	@echo Installing ${APK_FILE} in target device
	${ADB} install ${APK_FILE}

run:
	@echo Starting ${APK_FILE} in target device
	${ADB} shell am start -n ${PACKAGE_NAME}/${ACTIVITY_NAME}

reset: clean update

clean:
	@echo Deleting all apk files
	rm -f *.apk

update:
	@echo Cleaning local changes before updating codebase
	git reset --hard
	@echo Updating codebase
	git pull

sign:
	@echo Signing apk
	${JAR_SIGNER} -verbose -sigalg ${SIGALG} -digestalg ${DIGESTALG} -keystore ${KEYSTORE_FILE} ${APK_FILE} ${KEYSTORE_ALIAS}

zipalign:
	@echo Running zipalign on ${APK_FILE}
	${ZIPALIGN} -f -v 4 ${APK_FILE} ${FINAL_APK}
