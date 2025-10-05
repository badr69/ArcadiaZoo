import os
from app import create_app

app = create_app()

# Pour test local uniquement
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



# import os
# from app import create_app
# from flask import jsonify
#
#
# app = create_app()
#
# # @app.route('/api/test')
# # def api_test():
# #     return jsonify({"message": "API test route works!"})
#
# if __name__ == '__main__':
#     # app.run(host="0.0.0.0", port=5000, debug=True)
#     # app.run(debug=True)
#
#     # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
#     #
#     # port = int(os.environ.get("PORT", 5000))
#     # # Serve HTTPS using ton certificat et clé
#     # context = ('dev.crt', 'dev.key')  # (certificat, clé)
#     #
#     # app.run(host="0.0.0.0", port=port, debug=True, ssl_context=context)
#
#     app.run(
#         host='0.0.0.0',
#         port=5000,
#         ssl_context=('dev.crt', 'dev.key')  # <-- fichiers à la racine
#     )