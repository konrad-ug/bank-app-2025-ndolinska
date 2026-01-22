from behave import *
import requests

URL = "http://localhost:5000"

@when('I make an "{transfer_type}" transfer of "{amount}" to account with pesel "{pesel}"')
@given('I make an "{transfer_type}" transfer of "{amount}" to account with pesel "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    json_body = {
        "amount": float(amount),  
        "type": transfer_type
    }
    context.response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)

@when('I send a transfer request without type with amount "{amount}" to pesel "{pesel}"')
def make_invalid_transfer(context, amount, pesel):
    json_body = {
        "amount": float(amount)
    }
    context.response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)

@then('The transfer should be successful')
def transfer_success(context):
    assert context.response.status_code == 200
    
@then('The transfer should fail with status code "{status_code}"')
def transfer_fail(context, status_code):
    assert context.response.status_code == int(status_code)