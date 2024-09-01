from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ourcustompkg",
    version="0.14",
    author="Brandon & Moshiur",
    author_email="brandon@neuroleapmail.com, moshiur@neuroleapmail.com",
    description="A robust YOLOv7-based package designed for efficient toy car detection and comprehensive dataset management.",
    long_description=long_description,
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
        # Additional dependencies specific to YOLOv7 or other custom requirements can be added here
    ],
    entry_points={
        'console_scripts': [
            'detect_car=ourcustompkg.yolov7.detect_car:main',  # Adjusted to call the main function in detect_car.py
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",  # Change this to "5 - Production/Stable" if your package is production-ready
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",  # Replace with the appropriate license if necessary
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    keywords="YOLOv7, toy car detection, dataset management, computer vision, deep learning",
    project_urls={
        "Bug Tracker": "https://github.com/NeuroLeapTeam/gesture_recognition/issues",  # Replace with the bug tracker URL
        "Documentation": "https://github.com/NeuroLeapTeam/gesture_recognition/wiki",  # Replace with the documentation URL
        "Source Code": "https://github.com/NeuroLeapTeam/gesture_recognition",  # Replace with the source code URL
    },
    python_requires='>=3.6',  # Adjust this based on your project's Python version compatibility
)
