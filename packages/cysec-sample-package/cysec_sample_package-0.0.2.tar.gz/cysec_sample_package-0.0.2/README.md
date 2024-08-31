# Step 1: Set Up Your Project Directory
  ## 1.Create a new directory for your package:
    ```
    mkdir my_sample_package
    cd my_sample_package

    ```
  ## 2. Inside this directory, create a subdirectory with the same name as your package:
   ```
   mkdir my_sample_package
   ```
  ## 3. Create an __init__.py file inside the package subdirectory:
   ```
   touch my_sample_package/__init__.py
   ```

  ## 4. Create a simple Python module, for example, my_module.py:
    ```
    my_sample_package/my_module.py
    def hello_world():
        print("Hello, world!")
    ```

# Step 2: Create setup.py
  ## Create a setup.py file in the root directory:
  ```
  # setup.py
    from setuptools import setup, find_packages

    setup(
        name="my_sample_package",  # Replace with your own package name
        version="0.1.0",
        author="Your Name",
        author_email="your.email@example.com",
        description="A simple example package",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/yourusername/my_sample_package",  # Replace with your URL
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )

   ```

# Step 3: Create a pyproject.toml (Optional)
   This file helps define your build system requirements:
   ```
   [build-system]
    requires = ["setuptools>=42", "wheel"]
    build-backend = "setuptools.build_meta"
   ```

# Step 4: Build Your Package
   Install the necessary tools:

   ```
   pip install setuptools wheel
   ```
   Build the package:
   ```
   python setup.py sdist bdist_wheel
   ```
# Step 5: Upload to PyPI
   Install twine to upload your package:
   ```
   pip install twine
   ```
   Upload the package to PyPI:
   ```
   twine upload dist/*
   ```

# Step 6: Verify Installation
   
   Once uploaded, you can install your package using:
   ```
   pip install my_sample_package
   ```
   


Changes form my side

