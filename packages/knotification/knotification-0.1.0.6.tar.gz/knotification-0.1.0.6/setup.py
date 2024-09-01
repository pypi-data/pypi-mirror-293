from setuptools import setup, find_packages

setup(
    name="knotification",
    version="0.1.0.6",
    packages=find_packages(),
    description="Notification",
    author="kokaito",
    author_email="kokaito.git@gmail.com",
    url="https://github.com/kokaito-git/knotification",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "pygame",
        "py-notifier",
    ],
    extras_require={
        "Windows": ["WinToaster"],
        "Linux": [],
    },
    package_data={
        "knotification.sound": ["error.wav", "error2.aiff", "notification.wav"],
        "knotification.image": ["error.png", "info.png"],
    },
    include_package_data=True,
    python_requires=">=3.6",
)
