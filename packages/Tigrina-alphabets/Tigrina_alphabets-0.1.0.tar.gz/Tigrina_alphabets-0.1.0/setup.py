from setuptools import setup, find_packages
# Attempt to read README.md with UTF-8 encoding
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except UnicodeDecodeError:
    # If there's a UnicodeDecodeError, attempt to read it with a different encoding
    with open("README.md", "r", encoding="latin-1") as fh:
        long_description = fh.read()

setup(
    name="Tigrina_alphabets",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['pandas'],  # List your dependencies here
    author="Gide Segid",
    author_email="gidesegid@gmail.com",
    description="Tigrina alphabet manupilations",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Correct content type
    url="https://github.com/gidesegid/Tigrina_alphabets_coder_decoder_python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)