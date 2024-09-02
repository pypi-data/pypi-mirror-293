
# conda activate py3
rm dist/*.tar.gz
rm dist/*.whl
python -m build
twine upload dist/*
pip install --upgrade es_simple