cd python
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
deactivate

to run locally
pip install -e .

pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/
