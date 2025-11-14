from flask import Flask, request, Response
from flask_cors import CORS
import requests
from base64 import b64encode

app = Flask(__name__)
CORS(app)  # adds Access-Control-Allow-Origin: * to ALL responses


def xml_response(text, status=200):
    """Always return XML with CORS-safe Flask Response object"""
    return Response(text, status=status, mimetype="application/xml")


@app.route("/api/fetch", methods=["GET"])
def fetch_data():
    school_code = request.args.get("school_code")
    username = request.args.get("username")
    password = request.args.get("password")
    date = request.args.get("date")

    if not (school_code and username and password and date):
        return xml_response("<VpMobil><error>Missing parameters</error></VpMobil>", 400)

    url = f"https://www.stundenplan24.de/{school_code}/mobil/mobdaten/PlanKl{date}.xml"
    auth_header = "Basic " + b64encode(f"{username}:{password}".encode()).decode()

    try:
        r = requests.get(url, headers={"Authorization": auth_header}, timeout=10)

        if r.status_code != 200:
            return xml_response(
                f"<VpMobil><error>HTTP {r.status_code} error</error></VpMobil>",
                r.status_code
            )

        # SUCCESS → return XML
        return xml_response(r.text, 200)

    except requests.exceptions.RequestException as e:
        return xml_response(f"<VpMobil><error>Failed to fetch: {str(e)}</error></VpMobil>", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
