from app import create_app
from flask import Flask, jsonify
import os

app = create_app()

@app.route('/api/test')
def api_test():
    return jsonify({"message": "API test route works!"})


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



