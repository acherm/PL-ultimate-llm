Feature: data tables

  Scenario: passing a data table to a step
    Given a step with a data table:
      | a | b |
      | c | d |
      | e | f |
    When I run the feature
    Then the step passes
    And the step definition has a data table with the following rows:
      | a | b |
      | c | d |
      | e | f |
    And the step definition has a data table with the following hashes:
      | a | b |
      | c | d |
      | e | f |
    And the step definition has a data table with the following raw rows:
      | a | b |
      | c | d |
      | e | f |

  Scenario: passing a data table to a step with a doc string
    Given a step with a doc string and a data table:
      """
      doc string
      """
      | a | b |
      | c | d |
    When I run the feature
    Then the step passes
    And the step definition has a doc string "doc string"
    And the step definition has a data table with the following rows:
      | a | b |
      | c | d |

  Scenario: data table with special characters
    Given a step with a data table:
      | \ | |
      | | \ |
    When I run the feature
    Then the step passes
    And the step definition has a data table with the following rows:
      | \ | |
      | | \ |

  Scenario: data table with escaped pipe
    Given a step with a data table:
      | a \| b |
    When I run the feature
    Then the step passes
    And the step definition has a data table with the following rows:
      | a \| b |

  Scenario: data table with escaped backslash
    Given a step with a data table:
      | a \\ b |
    When I run the feature
    Then the step passes
    And the step definition has a data table with the following rows:
      | a \\ b |