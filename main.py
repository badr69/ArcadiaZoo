from app import create_app


app = create_app()


if __name__ == '__main__':
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    app.run(debug=True)

