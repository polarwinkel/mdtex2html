from setuptools import setup, find_packages
import pathlib
setup(
    keywords='TeX, LaTeX, Markdown, HTML markdown2html, latex2mathml',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=['markdown', 'latex2mathml'],
    project_urls={
        'Bug Reports': 'https://github.com/polarwinkel/mdtex2html/issues',
        'Source': 'https://github.com/polarwinkel/mdtex2html',
    },
)
