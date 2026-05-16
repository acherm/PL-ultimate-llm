*** Settings ***
Documentation     A test suite with a single test for valid login
...
...               This test follows the example using keywords from
...               the SeleniumLibrary
Resource          login.resource
Resource          prenuptial.resource
Test Teardown     Close Browser

*** Test Cases ***
Navigate to Edit Prenuptial Record (Level 1):
    Open Browser to Login Page
    Login Level 1 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Add Prenuptial Page Should Be Open

Navigate to Edit Prenuptial Record (Level 2):
    Open Browser to Login Page
    Login Level 2 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Prenuptial Main Page From View Prenuptial Page
    Prenuptial Main Page Should Be Open
    Navigate to View Prenuptial Page From Prenuptial Main Page
    View Prenuptial Page Should Be Open
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open

Navigate to Edit Prenuptial Record (Level 3):
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Prenuptial Main Page From View Prenuptial Page
    Prenuptial Main Page Should Be Open
    Navigate to View Prenuptial Page From Prenuptial Main Page
    View Prenuptial Page Should Be Open
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open

Edit Non-Member Bride From Non-Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Bride Details
    Select Non-Member Bride Form
    Input Non Member Bride Details    Natalia    N    Silang
    Save Bride Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Non-Member Bride From Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Member Bride Form
    Select Non-Member Groom Form
    Select Random Member Bride
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Bride Details
    Select Non-Member Bride Form
    Input Non Member Bride Details    Natalia    N    Silang
    Save Bride Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Member Bride From Non-Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Bride Details
    Select Member Bride Form
    Select Random Member Bride
    Save Bride Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Member Bride From Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Member Bride Form
    Select Non-Member Groom Form
    Select Random Member Bride
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Bride Details
    Select Member Bride Form
    Select Random Member Bride
    Save Bride Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Non-Member Groom From Non-Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Maximo Sr.    K    De Leon
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Groom Details
    Select Non-Member Groom Form
    Input Non Member Groom Details    Jonathan Jr.    J    Dela Pena
    Save Groom Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Non-Member Groom From Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Select Random Member Groom
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Groom Details
    Select Non-Member Groom Form
    Input Non Member Groom Details    Jonathan Jr.    J    Dela Pena
    Save Groom Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Member Groom From Non-Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Maximo Sr.    K    De Leon
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Groom Details
    Select Member Groom Form
    Select Random Member Groom
    Save Groom Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Member Groom From Member Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Select Random Member Groom
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Select Edit Groom Details
    Select Member Groom Form
    Select Random Member Groom
    Save Groom Detail Changes
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Wedding Date Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to View Prenuptial Page From Prenuptial Main Page
    View Prenuptial Page Should Be Open
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Edit Prenuptial Page Should Be Open
    Input Wedding Date    08    14    2023
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Edit Every Field Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Maximo Sr.    K    De Leon
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Edit Prenuptial Page From View Prenuptial Page
    Select Edit Bride Details
    Select Non-Member Bride Form
    Input Non Member Bride Details    Natalia    N    Silang
    Save Bride Detail Changes
    Select Edit Groom Details
    Select Non-Member Groom Form
    Input Non Member Groom Details    Jonathan Jr.    J    Dela Pena
    Save Groom Detail Changes
    Edit Prenuptial Page Should Be Open
    Input Wedding Date    08    14    2023
    Save Prenuptial Form Data in Edit Prenuptial Page
    Save Prenuptial Form Changes
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Delete Prenuptial Record
    Forms Main Page Should Be Open

Delete Prenuptial Record
    Open Browser to Login Page
    Login Level 3 User
    Main Page Should Be Open
    Navigate to Forms Main Page From Main Page
    Forms Main Page Should Be Open
    Navigate to Prenuptial Page From Forms Main Page
    Prenuptial Main Page Should Be Open
    Navigate to Add Prenuptial Page From Prenuptial Main Page
    Add Prenuptial Page Should Be Open
    Select Non-Member Bride Form
    Select Non-Member Groom Form
    Input Non Member Bride Details    Donna    A    Grant
    Input Non Member Groom Details    Elroy    B    Spalding
    Input Current Date    08    02    2021
    Input Wedding Date    09    09    2021
    Save Prenuptial Form Data
    Submit Prenuptial Form
    View Prenuptial Page Should Be Open
    View Prenuptial Page Should Match Form Inputs
    Navigate to Prenuptial Main Page From View Prenuptial Page
    Prenuptial Main Page Should Be Open
    Navigate to View Prenuptial Page From Prenuptial Main Page
    View Prenuptial Page Should Be Open
    Delete Prenuptial Record
    Forms Main Page Should Be Open
