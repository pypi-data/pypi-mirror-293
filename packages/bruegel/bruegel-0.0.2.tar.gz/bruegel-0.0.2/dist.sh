python -m setuptools_git_versioning

version="0.0.2"

git add .
git commit -m "version v${version}"

git tag -a v${version} -m "v${version}"

python -m build

# optional: upload test
# twine upload --repository testpypi dist/bruegel-${version}.tar.gz --verbose

git push --tags
git push

# conda install gh --channel conda-forge
gh release create v${version} -t "v${version}" -n "v${version}" dist/bruegel-${version}.tar.gz

# pip install twine
twine upload dist/bruegel-${version}.tar.gz --verbose

python -m build --wheel
