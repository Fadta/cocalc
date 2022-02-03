from distutils.core import setup

setup(
    # Application name:
    name="cocalc",

    version="0.0.1",

    author="Francisco Vicente",
    author_email="fvpan01@gmail.com",

    # Packages
    packages=["cocalc", "cocalc.prettifier"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/Fadta/cocalc",

    #
    license="LICENSE",
    # description="",

    # long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "sympy",
    ],

    entry_points={
        "console_scripts": [
            "cocalc=cocalc.__main__:main"
        ],
    }
)
