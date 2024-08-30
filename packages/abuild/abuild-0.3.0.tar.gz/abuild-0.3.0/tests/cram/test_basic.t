  $ mkdir code
  $ echo content > code/file1
  $ echo other content > code/file2
  $ echo "components:" > abuild.yaml
  $ echo "  - path: code" >> abuild.yaml
  $ echo "    steps:" >> abuild.yaml
  $ echo "      - name: List files" >> abuild.yaml
  $ echo "        cmd: ls -1"  >> abuild.yaml
  $ cat abuild.yaml
  components:
    - path: code
      steps:
        - name: List files
          cmd: ls -1
  $ abuild build
  Building component: code
  Running step: List files
  Output:
  file1
  file2
  

Now rerun
  $ abuild build

And then change a file
  $ echo changed > code/file1
  $ abuild build
  Building component: code
  Running step: List files
  Output:
  file1
  file2
  
Next add an ignore file and ignore it
  $ echo .abuildignore > .abuildignore
  $ abuild build

Now add another file to the ignore file and edit it
  $ echo file1 >> .abuildignore
  $ echo changed again > file1
  $ abuild build
