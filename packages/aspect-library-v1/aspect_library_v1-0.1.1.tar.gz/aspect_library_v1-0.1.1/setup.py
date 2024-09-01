from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='aspect_library_v1',  # Replace with your library name
    version='0.1.1',  # Initial release version
    description='A Python library for aspect-based sentiment analysis with translation capabilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    url='https://github.com/yourusername/my_aspect_library',  # Replace with the URL of your project (if any)
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'pandas',
        'deep_translator',
        'unlimited_machine_translator',
        'pyabsa',
        'nltk',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # You can choose a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    include_package_data=True,
)
