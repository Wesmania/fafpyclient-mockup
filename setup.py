from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_reqs = f.read().splitlines()

long_desc = """
A prototype slash mockup of a FAF python client. Probably won't go anywhere.
"""

print(find_packages("src"))

setup(
    name="faf_client",
    version=open('VERSION').read().strip(),
    description="FAF python client, take 2",
    long_description=long_desc,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    author="Igor Kotrasiński",
    author_email="i.kotrasinsk@gmail.com",
    url="https://github.com/Wesmania/fafpyclient-mockup",
    keywords="FAForever client",
    license="GPL3",
    package_dir = {"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "faf_client = faf.main:main",
        ],
    },
    install_requires=install_reqs
)
