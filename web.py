from flask import Flask

from routesold.dashboard_route import dashboard_bp
from routesold.customer_route import customer
from routesold.machine_route import machine_bp
from routesold.manual_route import manual_bp

app = Flask(__name__)

app.register_blueprint(dashboard_bp)
app.register_blueprint(customer)
app.register_blueprint(machine_bp)
app.register_blueprint(manual_bp)

if __name__ == "__main__":

    app.run(
        debug=True
    )