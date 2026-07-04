import os

from flask import Flask, jsonify

from remediation_engine import ALLOWED_PORTS, remediate_inverted, seed_rules

app = Flask(__name__)

FLAG_REMEDIATE = os.environ.get("FLAG_REMEDIATE", "FLAG{inverted_allowlist_leaves_ssh_open}")

DANGEROUS_PORTS = {22, 3389}

security_group = {"rules": seed_rules()}


@app.route("/security-group", methods=["GET"])
def get_security_group():
    rules = security_group["rules"]
    dangerous = [r for r in rules if r["port"] in DANGEROUS_PORTS and r["cidr"] == "0.0.0.0/0"]
    resp = {"rules": rules, "dangerous_rules_present": bool(dangerous)}
    if dangerous:
        resp["flag"] = FLAG_REMEDIATE
    return jsonify(resp)


@app.route("/reset", methods=["POST"])
def reset():
    security_group["rules"] = seed_rules()
    return jsonify({"status": "reset", "rules": security_group["rules"]})


@app.route("/remediate", methods=["POST"])
def remediate():
    before = security_group["rules"]
    # BUG: this is meant to implement the AWS Config auto-remediation action
    # "revoke any inbound rule whose port is not on the allowlist" but the
    # condition is inverted (see remediation_engine.remediate_inverted) — it
    # revokes the allowed rules and keeps everything else instead.
    after = remediate_inverted(before, ALLOWED_PORTS)
    security_group["rules"] = after
    return jsonify({"status": "remediated", "before": before, "after": after, "mode": "vulnerable"})


@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "mode": "vulnerable"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
