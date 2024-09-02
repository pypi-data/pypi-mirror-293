from setuptools import setup, find_packages

description = 'Pwgv (password generation and verification) генерация и проверка паролей'
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='percent_password',  # Замените на имя вашего пакета
    version='1.0',    # Задайте версию вашего пакета
    long_description=long_description,  # Содержимое README.md
    long_description_content_type='text/markdown',
    description=description,
    author='testg1',
    author_email='radan85669@avashost.com',
    url='https://github.com/G0ga1/percent_password',  # Замените на URL вашего репозитория
    packages=find_packages(),  # Найдет все пакеты в проекте
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.12',  # Минимальная версия Python
)
