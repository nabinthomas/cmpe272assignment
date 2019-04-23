# Guidelines for directory structure of unit tests:

* The unit tests for this project are all kept under <gitroot>/tests/unittests/
* The test input data for these unit tests are kept under <gitroot>/tests/unittests/data/

## How to add a unit test

1. Create a new bash script as your entry point to the test under  <gitroot>/tests/unittests/
2. Create any other scripts (python, shell script etc) in the same dir or sub dirs as needed, and invoke them from your main test script. 
3. Call the unit test main script from "test_run_all.sh"
4. The test script should return a failure/set error code before exiting so that the caller can detect pass/fail. 
5. All the test input data should be copied to "data" dir and should be referred using the relative path from <gitroot>/tests/unittests/
    eg: importmydata.py ./data/dataToimport.csv
6. All tests scripts should print a "PASS" / "FAIL" message at the end of it. (ALL CAPS like below)
```bash
    echo "PASS" 
```
        OR
```bash
    echo "FAIL"
```
7. "test_run_all.sh" will be later used for Continuous Integration and Testing with Travis-CI. 