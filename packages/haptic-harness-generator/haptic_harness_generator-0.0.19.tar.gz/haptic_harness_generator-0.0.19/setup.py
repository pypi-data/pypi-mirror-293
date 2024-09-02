from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="haptic_harness_generator",
    version="0.0.18",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pyvista>=0.43.6",
        "ezdxf",
        "PyQt5",
        "pyvistaqt",
    ],
    entry_points={
        "console_scripts": ["run-haptic-harness = haptic_harness_generator:run_app"]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
