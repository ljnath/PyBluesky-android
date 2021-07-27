import sysconfig

# setting if the current execution environemnt is and android
IS_ANDROID = True if sysconfig.get_config_var('ANDROID_API_LEVEL') else False
