*** Settings ***
Library    String
Library    Collections

*** Variables ***
@{NAMES}      Alice    Bob    Charlie    Diana    Eve
${GREETING}   Hello

*** Test Cases ***
Greet All Users
    [Documentation]    Greet each user and verify the greeting format
    FOR    ${name}    IN    @{NAMES}
        ${message}=    Create Greeting    ${name}
        Should Start With    ${message}    ${GREETING}
        Should End With    ${message}    !
        Log    ${message}
    END

Count Names By Length
    [Documentation]    Count names that are shorter or longer than 4 characters
    ${short}=    Create List
    ${long}=    Create List
    FOR    ${name}    IN    @{NAMES}
        ${length}=    Get Length    ${name}
        IF    ${length} <= 4
            Append To List    ${short}    ${name}
        ELSE
            Append To List    ${long}    ${name}
        END
    END
    Length Should Be    ${short}    3
    Length Should Be    ${long}    2
    Log    Short names: @{short}
    Log    Long names: @{long}

Reverse And Uppercase Names
    [Documentation]    Transform each name and collect results
    @{results}=    Create List
    FOR    ${name}    IN    @{NAMES}
        ${upper}=    Convert To Upper Case    ${name}
        ${reversed}=    Evaluate    '${name}'[::-1]
        Append To List    ${results}    ${upper}-${reversed}
    END
    Length Should Be    ${results}    5
    Log Many    @{results}

*** Keywords ***
Create Greeting
    [Arguments]    ${name}
    ${message}=    Catenate    ${GREETING}    ,    ${name}    !
    RETURN    ${message}
