from setuptools import setup,find_packages

setup(
    name='GOPIRAJ-STT',
    version='0.1',
    author='Gopi Raj',
    description='this is a speech to text package created by Gopi Raj'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'speech_recognition',
    'pyttsx3',
    'webdriver_manager'
]