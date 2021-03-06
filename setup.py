from distutils.core import setup

setup(
    name="RTMLCore",  # How you named your package folder (MyLib)
    packages=["rtml_core"],  # Chose the same as "name"
    version="0.2.1",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="For generating Resource Tag objects",  # Give a short description about your library
    author="DeadMeme5441",  # Type in your name
    author_email="deadunderscorememe@gmail.com",  # Type in your E-Mail
    url="https://github.com/DeadMeme5441/RTMLCore",  # Provide either the link to your github or to your website
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.7",
    ],
)
