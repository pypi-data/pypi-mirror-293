from setuptools import setup, find_packages

setup(
    name='nlxcaptcha',
    version='1.5',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tk',
    ],
    description='Tell "iPad Kids" and "Non-iPad Kids" apart using OpenAI API in this easy-to-integrate captcha.',
    author='Nlcky Solutions',
    author_email='nicky@nlcky.com',
    url='https://github.com/nlckysolutions/NLX-Captcha',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
