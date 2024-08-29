from setuptools import setup, find_packages

setup(
    name='irrelevant-content-detection',  # Paket adınız
    version='0.2',  # Versiyon numarası
    description='A Python package for detecting irrelevant content in text and HTML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Berk Birkan',  # İsminiz
    author_email='info@berkbirkan.com',  # E-posta adresiniz
    url='https://github.com/berkbirkan/irrelevant-content-detection',  # Proje URL'si
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy',
        'beautifulsoup4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python sürümü gereksinimi
)
