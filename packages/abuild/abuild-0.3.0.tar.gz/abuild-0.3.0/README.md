# Welcome to abuild

When I was looking for a build tool for a (fairly simple) monorepo, I noticed
that although there are many great ones, they all require considerable setup or
they only work with one particular language. I was rather looking for a basic build tool
that needs almost no setup and can handle a handful services in one repository
with some frontend, some backend and maybe a bit of machine learning code.

My goals for this project are
- Setting up abuild for a simple setup should be (almost) no effort.
- Code that hasn't changed shouldn't be re-build (that's kind of the point of a build tool).
- If I write a service in a different language, I should be able to use the same build tool.

To do this, `abuild` acts as a glue between existing language specific tools&mdash;in that
sense calling it a "build tool" might almost be promising too much. It's rather a build tool
manager for monorepos.

<!--
Here is some code to setup the repository so that I can use cram tests
  $ mkdir backend
  $ touch backend/tox.ini
  $ touch backend/Dockerfile
  $ mkdir frontend
  $ echo '{"scripts": {"test": "fake", "build": "fake"}}' > frontend/package.json
  $ mkdir tools
-->

## Getting started

You can install `abuild` from pypi with `pip install abuild`.

This example looks at a very simple monorepo with a python backend that gets build into a docker container and a javascript frontend that gets build with `npm run build`. There is also a tools directory that shouldn't be build:
  $ tree
  .
  |-- backend
  |   |-- Dockerfile
  |   `-- tox.ini
  |-- frontend
  |   `-- package.json
  `-- tools
  
  3 directories, 3 files

To set up `abuild` in a new monorepo, you can run

  $ abuild parse > abuild.yaml
  $ cat abuild.yaml
  components:
  - path: backend
    steps:
    - cmd: tox
    - cmd: docker buildx build .
  - path: frontend
    steps:
    - cmd: npm run test
    - cmd: npm run build
  

As you can see, `abuild` understood the basics of the repository and created the skeleton of a config file. Feel free to update the config file by hand. For example, you could add names for the steps by setting `components.[].steps.[].name`. You could also delete (or add) steps to fit your needs.

To build your services with `abuild`, you simply run `abuild build` in your project root. `abuild` maintains a state file `.abuild_state.json` that tracks your build status. Currently, the state is not synchronized between machines (which can be a bit of a hindrance of CI). However, you can commit the `.abuild_state.json` to your revision control system.

## Changelog

### v0.2.0
# New features
- general:
 - Basic support for tags
 - support for deselecting tags
### v0.3.0
# New features
- General: directory parsing supports makefiles
