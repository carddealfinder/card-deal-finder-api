from flask import Flask, request, jsonify
from pricing.aggregator import aggregate_search

app = Flask(__name__)

@app.get("/search")
def search_cards():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Missing ?query="}), 400

    results = aggregate_search(query)

    return jsonify({
        "query": query,
        "metrics": results["metrics"],
        "results": results["results"],   # <-- THIS replaces ranked_results
    })

if __name__ == "__main__":
    app.run(debug=True)
