from setuptools import setup, find_packages

with open('README_PYPI.md') as f:
    long_description = f.read()

setup(
    name='jaxlem',
    url='https://github.com/amavrits/jax-lem',
    author='Antonis Mavritsakis',
    author_email='amavrits@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "jax",
        "jaxtyping",
        "jax-tqdm",
        "optax",
        "jaxopt",
        "numpy",
        "scipy",
        "matplotlib",
        "pytest",
        ],
    extras_require={
        "dev": []
    },
    python_requires=">=3.9.0",
    version='0.1.4',
    license='MIT',
    description='LEM slope stability analysis using JAX',
)