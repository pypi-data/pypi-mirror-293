This example is about using tags to structure runs globally. We first create a
simple directory structure:
  $ mkdir component1
  $ touch component1/file1.txt
  $ touch component1/file2.txt
  $ echo 'components:' > abuild.yaml
  $ echo '  - path: component1' >> abuild.yaml
  $ echo '    steps:' >> abuild.yaml
  $ echo '    - cmd: echo "Testing application (fake)"' >> abuild.yaml
  $ echo '      tag: test' >> abuild.yaml
  $ echo '    - cmd: echo "Building application (fake)"' >> abuild.yaml
  $ echo '      tag: build' >> abuild.yaml

We can now use abuild to build the full application
  $ abuild build
  Building component: component1
  Running step: echo "Testing application (fake)"
  Output:
  Testing application (fake)
  
  Running step: echo "Building application (fake)"
  Output:
  Building application (fake)
  

However, we can also just select individual tags to run (note that I delete the state file here to ensure that abuild treats this as a new directory)
  $ rm .abuild_state
  $ abuild build -t test
  Building component: component1
  Running step: echo "Testing application (fake)"
  Output:
  Testing application (fake)
  
  Not running step: echo "Building application (fake)" - tag build was not selected

And
  $ rm .abuild_state
  $ abuild build -t build
  Building component: component1
  Not running step: echo "Testing application (fake)" - tag test was not selected
  Running step: echo "Building application (fake)"
  Output:
  Building application (fake)
  

You can also deselect tags
  $ rm .abuild_state
  $ abuild build -t !build
  Building component: component1
  Running step: echo "Testing application (fake)"
  Output:
  Testing application (fake)
  
  Not running step: echo "Building application (fake)" - tag build was not selected


You are entirely free to choose tags any way you like. However, it's a good idea to avoid tags that start with an exclamation mark.
