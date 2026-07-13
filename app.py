from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from utils.scraper import scrape_news
from utils.response_builder import build_response

app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/extract",
    methods=["POST"]
)
def extract():

    try:

        data = request.get_json()

        url = data.get(
            "url",
            ""
        ).strip()

        if not url:

            return jsonify({

                "success": False,

                "message": "Please enter a URL."

            })

        news = scrape_news(url)

        response = build_response(

            news["title"],

            news["article"]

        )

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

@app.route(
    "/predict_manual",
    methods=["POST"]
)
def predict_manual():

    try:

        data = request.get_json()

        title = data.get(
            "title",
            ""
        ).strip()

        article = data.get(
            "article",
            ""
        ).strip()

        if not title:

            return jsonify({

                "success": False,

                "message": "Title is required."

            })

        if not article:

            return jsonify({

                "success": False,

                "message": "Article is required."

            })

        response = build_response(

            title,

            article

        )

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

@app.route("/health")
def health():

    return jsonify({

        "status": "running"

    })

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )