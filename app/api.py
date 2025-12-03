from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import Personal_Account

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    account = Personal_Account(data["first_name"], data["last_name"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all()
    accounts_data = [{"first_name": acc.first_name, "last_name": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.return_length()
    return jsonify({"count": count}), 200
@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print("Find account by pesel request received")
    account = registry.search_account(pesel)
    if account:
            return jsonify({
                "first_name": account.first_name,
                "last_name": account.last_name,
                "pesel": account.pesel,
                "balance": account.balance
            }), 200
    else:
        return jsonify({"message": "Account not found"}), 404
@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    print(f"Update account by pesel: {pesel}")
    account = registry.search_account(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    data = request.get_json()
    if "first_name" in data:
        account.first_name = data["first_name"]
    if "last_name" in data:
        account.last_name = data["last_name"]
    return jsonify({"message": "Account updated"}), 200
@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print(f"Delete account by pesel: {pesel}")
    account = registry.search_account(pesel)
    
    if not account:
        return jsonify({"message": "Account not found"}), 404
    registry.accounts.remove(account)
    
    return jsonify({"message": "Account deleted"}), 200