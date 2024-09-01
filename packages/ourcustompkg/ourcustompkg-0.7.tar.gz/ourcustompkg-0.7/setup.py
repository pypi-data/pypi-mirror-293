from setuptools import setup, find_packages

setup(
    name="ourcustompkg",
    version="0.7",
    author="Brandon & Moshiur",
    author_email="brandon@neuroleapmail.com",
    description="A custom YOLOv7-based package for toy car detection and dataset management",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NeuroLeapTeam/gesture_recognition.git",  # Replace with your GitHub repository URL
    packages=find_packages(include=['ourcustompkg', 'ourcustompkg.*']),
    include_package_data=True,
    install_requires=[
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "opencv-python>=4.1.2",
        "numpy>=1.18.5",
        "Pillow>=7.2.0",
        "tqdm>=4.41.0",
        "mediapipe>=0.8.9",
        "tensorflow>=2.4.0",
        "matplotlib>=3.2.2",
        "scipy>=1.4.1",
        "pyyaml>=5.3.1",
        "seaborn>=0.11.0",
        "pandas>=1.1.5",
        "scikit-learn>=0.24.1",
        "requests>=2.23.0",
        # Add other dependencies from YOLOv7 or custom requirements if needed
    ],
    entry_points={
        'console_scripts': [
            'detect_car=ourcustompkg.yolov7.detect_car:main',  # Adjusted to call the main function in detect_car.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with the appropriate license if necessary
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust this based on your project's Python version compatibility
)
