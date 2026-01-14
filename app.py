from flask import Flask, render_template, request
import time

app = Flask(__name__)

# Simple cache
cache = {}

def fraud_prediction(amount, merchant, device_score, new_device):
    start = time.time()

    key = (amount, merchant, device_score, new_device)

    if key in cache:
        result = cache[key]
        cache_hit = True
    else:
        if amount > 30000 and new_device == 1:
            result = ("Fraud", 0.88, "HIGH_AMOUNT_NEW_DEVICE")
        else:
            result = ("Not Fraud", 0.10, "LOW_RISK")

        cache[key] = result
        cache_hit = False

    latency = round((time.time() - start) * 1000, 2)

    return result[0], result[1], result[2], latency, cache_hit


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        merchant = request.form.get("merchant")
        device_score = float(request.form.get("device_score"))
        new_device = int(request.form.get("new_device"))

        prediction, probability, rule, latency, cache_hit = fraud_prediction(
            amount, merchant, device_score, new_device
        )

        return render_template(
            "index.html",
            prediction=prediction,
            probability=probability,
            rule=rule,
            latency=latency,
            cache_hit=cache_hit
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

