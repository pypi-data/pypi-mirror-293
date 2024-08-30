This is about parsing a repository
  $ mkdir comp1
  $ mkdir comp2
  $ mkdir comp3
  $ echo '[build-system]' > comp1/pyproject.toml
  $ echo 'build-backend = "setuptools.build_meta"' >> comp1/pyproject.toml
  $ touch comp1/tox.ini
  $ echo '{"scripts": {"test": "fake", "build": "fake"}}' > comp2/package.json
  $ touch comp3/Dockerfile
  $ abuild parse
  components:
  - path: comp1
    steps:
    - cmd: tox
    - cmd: python -m build
  - path: comp2
    steps:
    - cmd: npm run test
    - cmd: npm run build
  - path: comp3
    steps:
    - cmd: docker buildx build .
  
