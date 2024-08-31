from setuptools import setup, find_packages

setup(
    name='harmonyai',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['SpeechRecognition',
                      'pygame',
                      'gTTS',
                      'beautifulsoup4',
                      'spotipy',
                      'requests',
                      'pyaudio',
                      'distutils-pytest',
                      'pycaw',
                      'comtypes'
                      ],
    include_package_data=True,
    package_data={
        '': ['main.py'],  # Include both files
    },
    description='A package for nothing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='petteer1',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
