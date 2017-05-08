from setuptools import setup, find_packages

setup(
    name='kiskadee',
    version='0.1',
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
            install_requires=[
                'docker==2.0.0',
                'psycopg2',
                'firehose',
                'sqlalchemy',
                'python-debian',
                'chardet'
                ],
            test_suite='nose.collector',
            tests_require=['nose']
                )
