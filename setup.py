from setuptools import setup, find_packages


# Thanks to Pagure:
# https://pagure.io/pagure/blob/master/f/setup.py#_26
def get_requirements(requirements_file='requirements.txt'):
    """Get the contents of a file listing the requirements.

    :arg requirements_file: path to a requirements file
    :type requirements_file: string
    :returns: the list of requirements, or an empty list if
              `requirements_file` could not be opened or read
    :return type: list
    """

    with open(requirements_file) as f:
        return [
                line.rstrip().split('#')[0]
                for line in f.readlines()
                if not line.startswith('#')
                ]

setup(
    name='kiskadee',
    version='0.1.dev0',
    description='Continuous static analysis tool',
    long_description='Continuous static analysis tool \
            which writes the analyses \
            results into a Firehose database.',
            classifiers=[
                'Development Status :: 1 - Planning',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Programming Language :: Python :: 3.5',
                'Topic :: Security',
                ],
            keywords='static analysis software assurance',
            author='Athos Ribeiro, David Carlos',
            author_email='athoscr@fedoraproject.org, ddavidcarlos1392@gmail.com',
            url='https://github.com/LSS-USP/kiskadee',
            license='GPLv3',
            packages=find_packages(),
            include_package_data=False,
            entry_points={'console_scripts': [
                'kiskadee = kiskadee.monitor:daemon']},
            install_requires=get_requirements(),
            test_suite='nose.collector',
            tests_require=['nose']
                )
