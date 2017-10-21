from setuptools import setup

setup(
    name='steem-watchdog',
    version='0.0.2',
    py_modules=['steem_watchdog'],
    url='http://github.com/emre/steem-watchdog',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Automates claiming process of author/curation rewards',
    entry_points={
        'console_scripts': [
            'steem_watchdog = steem_watchdog:main',
        ],
    },
    install_requires=['steem', ]
)
