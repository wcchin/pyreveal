from setuptools import setup, find_packages


setup(
    name="pyreveal",

    version="0.1.4",
    
    author="Benny Chin",
    author_email="wcchin.88@gmail.com",

    packages=['pyreveal', 'pyreveal.docdata', 'pyreveal.reveal_js', 'pyreveal.templates'],
    #package_dir={'':'pyreveal'},

    include_package_data=True,
    
    package_data={'': ['templates/base.html']},
    
    url="https://github.com/wcchin/pyreveal",

    license="LICENSE",
    description="a python package that convert markdown to reveal.js slides.",

    long_description=open("README.md").read(),
    
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Visualization',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
    ],

    keywords='reveal.js, markdown, slides, presentation',

    install_requires=[
        "jinja2",
        "markdown",
        "watchdog",
    ],
    entry_points = {
        "console_scripts": ['pyreveal = pyreveal.pyreveal:main']
        },
)
