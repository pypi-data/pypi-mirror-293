from setuptools import setup, find_packages

setup(
    name='vital-agent-eval-env',
    version='0.0.3',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='Vital Agent Eval Env',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vital-agent-eval-env',
    packages=find_packages(exclude=["test"]),
    entry_points={

    },
    scripts=[
        'bin/vitalagenteval'
    ],
    package_data={
        '': ['*.pyi']
    },
    license='Apache License 2.0',
    install_requires=[
        'vital-ai-vitalsigns>=0.1.20',
        'vital-ai-aimp>=0.1.6',
        'vital-agent-container-client>=0.0.3',
        'openpyxl',
        'vital-agent-kg-utils>=0.1.1'
    ],
    extras_require={
        'dev': [
            'twine',
            'setuptools'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
