from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'PressOne Python package'
LONG_DESCRIPTION = 'This package helps you interacts with the pressone backend.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pressone-africa-sdk", 
        version=VERSION,
        author="Afolabi Tope",
        author_email="<tope@pressone.co>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'pressone', 'telephony', 'telephone', 'internet call', 'phone'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)