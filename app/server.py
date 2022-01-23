from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from app.dash2 import create_dash2_app

from app.dashapp import create_dash_app
from app.simple_dashboard import create_simple_dashboard_app


app = FastAPI()


@app.get("/")
def read_main():
    return {
        "routes": [
            {"method": "GET", "path": "/", "summary": "Landing"},
            {"method": "GET", "path": "/status", "summary": "App status"},
            {"method": "GET", "path": "/dash", "summary": "Sub-mounted Dash application"},
        ]
    }


@app.get("/status")
def get_status():
    return {"status": "ok"}


# A bit odd, but the only way I've been able to get prefixing of the Dash app
# to work is by allowing the Dash/Flask app to prefix itself, then mounting
# it to root
dash_app = create_dash_app(requests_pathname_prefix="/dash/")
app.mount("/dash", WSGIMiddleware(dash_app.server))

simple_dash_app = create_simple_dashboard_app(requests_pathname_prefix="/simple_dash/")
app.mount("/simple_dash", WSGIMiddleware(simple_dash_app.server))


dash2_app = create_dash2_app(requests_pathname_prefix="/dash2/")
app.mount("/dash2", WSGIMiddleware(dash2_app.server))

# todo ファンダメンタル分析とテクニカル分析のURLを別に用意
# tech_app = create_tech_app(requests_pathname_prefix="/tech/")
# app.mount("/tech", WSGIMiddleware(tech_app.server))

# fund_app = create_fund_app(requests_pathname_prefix="/fund/")
# app.mount("/fund", WSGIMiddleware(fund_app.server))

