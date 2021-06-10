import application

if __name__ == '__main__':
    app = application.create_app()
    app.run_server(host='0.0.0.0', port=8080, debug=True)
else:
    # Run gunicorn with 
    # PYTHONPATH=`pwd`/.. gunicorn -b 0.0.0.0:8080 web.appserver:gunicorn_app --timeout 100000
    gunicorn_app = application.create_app().server

