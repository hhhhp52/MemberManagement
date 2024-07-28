from database.db import init_db
from flask import Flask, request, jsonify, make_response
from flasgger import Swagger
from implement import implement

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"success": True}), 201


@app.route('/create_account', methods=['POST'])
def create_account():
    """
    Create a new account
    ---
    tags:
      - Account
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The desired username for the account
              example: testuser
            password:
              type: string
              description: The desired password for the account
              example: TestPassword1
    responses:
      201:
        description: Account created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            reason:
              type: string
              example: "Username already exists"
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    flag, result = implement.create_account_impl(username, password)
    if flag:
        return make_response(
            jsonify(
                success=flag
            ),
            result.get("status_code")
        )
    else:
        return make_response(
            jsonify(
                success=flag,
                reason=result.get("reason")
            ),
            result.get("status_code")
        )


@app.route('/verify_account', methods=['POST'])
def verify_account():
    """
    Verify account and password
    ---
    tags:
      - Account
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The username of the account being accessed
              example: testuser
            password:
              type: string
              description: The password being used to access the account
              example: TestPassword1
    responses:
      200:
        description: Password verified successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            reason:
              type: string
              example: "Username and password are required"
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            reason:
              type: string
              example: "Invalid username or password"
      429:
        description: Too Many Requests
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            reason:
              type: string
              example: "Too many failed attempts. Please wait before trying again."
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    flag, result = implement.verify_account_impl(username, password)
    if flag:
        return make_response(
            jsonify(
                success=flag
            ),
            result.get("status_code")
        )
    else:
        return make_response(
            jsonify(
                success=flag,
                reason=result.get("reason")
            ),
            result.get("status_code")
        )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
