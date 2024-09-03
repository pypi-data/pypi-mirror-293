from setuptools import setup, find_packages

setup(
    name="plasmid_detector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "plasmid_detector=plasmid_detector.anomaly_detector:main",
        ],
    },
)