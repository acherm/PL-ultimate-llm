*** Settings ***
Documentation    A test suite with a single test for valid login.
...    This test has a workflow that is created using keywords in
...    'Resource' file.
Resource         resource.robot
Test Setup       Open Login Page
Test Teardown    Close Browser

*** Test Cases ***
Valid Login
    Input Username    demo
    Input Password    mode
    Submit Credentials
    Welcome Page Should Be Open