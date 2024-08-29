from setuptools import setup, find_packages

setup(name='recommender_ibmws',
      version='0.1.2',
      author= 'Joana Martins dos Santos',
      author_email= 'joanamlmsantos@gmail.com',
      description='User article recommender system for IBM Watson Studio',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[  # Add this line to specify dependencies
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'scikit-learn>=0.22.0'
        ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    url = "https://github.com/joanamdsantos/recommender_ibmws_pkg",
    zip_safe=False)
