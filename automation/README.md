Prerequisites:
==============
* Install latest python3
* Install Firefox
* Install geckodriver for firefox using below steps 
   * Download latest geckdriver from https://github.com/mozilla/geckodriver/releases/latest
   * Extract it and move geckodriver
   * Provide executable permissions to the geckodriver executable file 
   * Set geckodriver file path in PATH variable or move this file to a path in PATH variable
     ```
     wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
     tar -xvzf geckodriver*
     tar -xvzf geckodriver-v0.31.0-linux64.tar.gz 
     sudo mv geckodriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/geckodriver
     ```
* Install all python packages from this git repo using
  ```
  pip install -r requirements.txt
  or 
  pip3 install -r requirements.txt
  ```

Run Tests:
=========
* Run Tests in a folder
  ```
  pytest tests/sanity --capture=no -T testbeds/functional/testbed1.yaml -R '{}'
  pytest tests/sanity --capture=no -T testbeds/functional/testbed1.yaml -R /tmp/runparams.yaml
  
  Note: --capture=no option make pytest to show print output at runtime.
  ```
* Run all tests in a file
  ```
  pytest tests/sanity/functional/test_device.py --capture=no -T testbeds/functional/testbed1.yaml -R '{}'
  pytest tests/sanity/functional/test_device.py --capture=no -T testbeds/functional/testbed1.yaml -R /tmp/runparams.yaml
  
  Note: --capture=no option make pytest to show print output at runtime.
  ```

Useful Links:
============
* Selinium Record and reply: https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/
* PyTest-bdd: https://pypi.org/project/pytest-bdd/
* Python Selenium: https://www.geeksforgeeks.org/selenium-python-tutorial/