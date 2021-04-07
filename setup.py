import ast
import re
from setuptools import setup, find_packages



_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('messages/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


# load README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='messages',
    version=version,
    url='https://github.com/trp07/messages',
    keywords=['message', 'messages', 'wrapper', 'email', 'text', 'SMS', 'MMS',
              'chat', 'chats', 'slack', 'twilio', 'async', 'asynchronous',
              'telegram', 'bot', 'telegrambot', 'whatsapp'],

    author='Tim Phillips',
    author_email='phillipstr@gmail.com',

    description=('A package designed to make sending messages '
                 'easy and efficient!'),
    long_description=readme,
    long_description_content_type='text/markdown',

    packages=find_packages(include=['messages']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],

    python_requires='>=3.5',

    install_requires=[
        'click>=6.0',
        'requests',
        'jsonconfig-tool',
        'validus>=0.3.0',
    ],

    test_suite='tests',
    test_requires=[
        'pytest-cov',
        'pytest-mock',
    ],

    setup_requires=['pytest-runner'],

    entry_points={
        'console_scripts': ['messages=messages.cli:main']
    },

)
