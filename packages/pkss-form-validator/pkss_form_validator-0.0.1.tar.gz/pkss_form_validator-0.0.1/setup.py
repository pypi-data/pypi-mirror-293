from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

with open('README.txt', 'r') as f:
    long_description = f.read()
with open('CHANGELOG.txt', 'r') as f:
    long_description += '\n\n' + f.read()

setup(
    name='pkss_form_validator',
    version='0.0.1',
    description='A Form Inputs Validator',
    long_description=long_description,
    long_description_content_type='text/plain',  # Change this to 'text/x-rst' or 'text/markdown' if using reStructuredText or Markdown
    url='',
    author='Vinoth',
    author_email='vinothmoorthy1397@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='validator',
    packages=find_packages(),
    install_requires=[]
)
