from setuptools import setup, find_packages

with open('requirements.txt', 'rt') as requirements_file:
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]
def read_version():
    with open("samestr/__init__.py") as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'\"")

setup(name='samestr',
      version=read_version(),
      description='SameStr identifies shared strains between pairs of '
                  'metagenomic samples based on the similarity of SNV profiles.',
      author='Daniel Podlesny',
      author_email='daniel.podlesny@embl.de',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/danielpodlesny/samestr/',
      license=open('LICENSE').read(),
      packages=find_packages(),
      package_data={'samestr': ['samestr', 'LICENSE']},
      install_requires=requirements,
      scripts=['samestr/samestr', 'samestr/convert/kpileup.py', 'samestr/convert/kp2np.py',
               'samestr/convert/dump_file.py', 'samestr/convert/filter_sam.py'],
      include_package_data=True)
