from setuptools import setup

# Условие для определения платформы
import sys
is_windows = sys.platform.startswith('win')

# Основные зависимости
install_requires = [
    'aiohttp',
    'pandas',
    'PyJWT',
    'requests'
]

if is_windows:
    install_requires.append('pywin32')

setup(
    name='py_cz_api',
    version='0.2.6',
    description='Библиотека для автоматизации работы с Честным Знаком через True API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jqxl/py_cz_api',
    download_url='https://codeload.github.com/jqxl/py_cz_api/zip/refs/heads/main',
    author='jqxl',
    author_email='jqxl+git@ya.ru',
    license='GNU General Public License v3.0',
    packages=['py_cz_api'],
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.10',
)
