from setuptools import setup

setup(
    name='scrapy-scrapedo',
    version='0.1.4',
    url='https://github.com/scrape-do/scrapy-scrapedo',
    description='Fundemantal Scrapy support for Scrape.do API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Scrape.do',
    author_email='hello@scrape.do',
    license='MIT',
    packages=['scrapydo'],
    classifiers=[ 
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
        "Company": "https://scrape.do/?utm_source=pypi&utm_medium=scrapydo",
        "Documentation": "https://scrape.do/documentation/?utm_source=pypi&utm_medium=scrapydo",
        "Source": "https://github.com/scrape-do/scrapy-scrapedo",
    },
    python_requires='>=3.8',
    install_requires=['scrapy'],
)