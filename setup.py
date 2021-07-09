"""
MIT License

Copyright (c) 2021 Lakhya Jyoti Nath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Version: 1.0.0
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://ljnath.com
"""

from distutils.core import setup
from setuptools import find_packages


setup(
    name="PyBluesky",
    version='1.0.0',
    author="Lakhya Jyoti Nath (ljnath)",
    author_email='ljnath@ljnath.com',
    description='A simple python game to navigate your jet and fight \
        though a massive missiles attack based on pygame framework',
    url='https://github.com/ljnath/PyBluesky-android',
    packages=find_packages(),
    package_data={
        '.': ['main.py'],
        './*': ['*.py'],
        '*/*': ['*.py', '*.ogg', '*.ttf', '*.png', '*.ico'],
        '*/*/*': ['*.py'],
        '*/*/*/*': ['*.py']
    },
    options={
            'apk': {
                'ignore-setup-py': None,
                # 'release': None,
                'arch': 'arm64-v8a',
                'package': 'com.ljnath.pybluesky',
                'requirements': 'pygame==2.0.1,aiohttp==3.7.4.post0,multidict==5.1.0,\
                    attrs==21.2.0,async-timeout==3.0.1,chardet==4.0.0,idna==3.2,\
                        typing-extensions==3.10.0.0,yarl==1.6.3,Plyer',
                'sdk-dir': '../android-sdk',
                'ndk-dir': '../android-ndk-r19c',
                'presplash': 'assets/images/presplash.png',
                'presplash-color': '#C4E2FF',
                'icon': 'assets/icon/pybluesky.png',
                'dist-name': 'PyBluesky',
                'android-api': 29,
                'bootstrap': 'sdl2',
                'orientation': 'landscape',
                'wakelock': None,
                'permissions':
                    [
                        'VIBRATE',
                        'INTERNET'
                    ]
            }
        }
)
