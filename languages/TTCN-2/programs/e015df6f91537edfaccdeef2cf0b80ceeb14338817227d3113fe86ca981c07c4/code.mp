Test Case Dynamic Behaviour: SimpleTest

Test Case Name: SimpleTest
Group: BasicTests
Purpose: Simple connection test
Default: INCONC
Configuration: Simple_Config

Nr  Label  Behaviour Description           Constraints Ref  Verdict  Comments
1          + CREATE (PCO1)
2          + SEND (PCO1, ConnectRequest)   CR1
3          + RECEIVE (PCO1, ConnectConfirm) CC1              PASS
4   L1     + OTHERWISE                                       FAIL
5          + TERMINATE
