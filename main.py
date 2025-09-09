import os
from app import create_app


app = create_app()



if __name__ == '__main__':

    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run(host="0.0.0.0", port=5000, ssl_context=("dev.crt", "dev.key"))


