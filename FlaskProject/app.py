from create_app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Rule: {rule}")

    app.run(debug=True)
