# from flask import Flask
# app = Flask(__name__)


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

#1
@app.route('/')
def hello_world():
    return 'Hello, World!'

#2

@app.route('/get_leetcode_profile', methods=['POST'])
def get_leetcode_profile():
    # Extract username from the request's JSON body
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # GraphQL query and variables
    graphql_query = {
        "query": """
        query getUserProfile($username: String!) {
            allQuestionsCount { difficulty count }
            matchedUser(username: $username) {
                contributions { points }
                profile { reputation ranking }
                submissionCalendar
                submitStats {
                    acSubmissionNum { difficulty count submissions }
                    totalSubmissionNum { difficulty count submissions }
                }
            }
        }
        """,
        "variables": {"username": username}
    }

    # Headers for the POST request to LeetCode
    headers = {
        "referer": f"https://leetcode.com/{username}/",
        "Content-Type": "application/json"
    }

    # URL for LeetCode GraphQL API
    url = "https://leetcode.com/graphql/"

    # Making the POST request to LeetCode
    response = requests.post(url, json=graphql_query, headers=headers)

    # Return the response from LeetCode
    return jsonify(response.json())
