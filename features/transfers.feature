Feature: Account transfers

Background:
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"

Scenario: Incoming transfer increases balance
    When I make an "incoming" transfer of "100" to account with pesel "12345678901"
    Then The transfer should be successful
    And Account with pesel "12345678901" has "balance" equal to "100"

Scenario: Outgoing transfer decreases balance
    Given I make an "incoming" transfer of "500" to account with pesel "12345678901"
    When I make an "outgoing" transfer of "200" to account with pesel "12345678901"
    Then The transfer should be successful
    And Account with pesel "12345678901" has "balance" equal to "300"

Scenario: Outgoing transfer fails when insufficient funds
    When I make an "outgoing" transfer of "100" to account with pesel "12345678901"
    Then The transfer should fail with status code "422"
    And Account with pesel "12345678901" has "balance" equal to "0"

Scenario: Express transfer applies fee
    Given I make an "incoming" transfer of "1000" to account with pesel "12345678901"
    When I make an "express" transfer of "100" to account with pesel "12345678901"
    Then The transfer should be successful
    And Account with pesel "12345678901" has "balance" equal to "899"

Scenario: Invalid transfer request returns bad request error
    When I send a transfer request without type with amount "100" to pesel "12345678901"
    Then The transfer should fail with status code "400"