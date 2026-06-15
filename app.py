from llama_cpp import Llama
from flask import Flask, request, jsonify

app = Flask(__name__)

print("Loading model from local file...")
model_path = "/app/qwen2.5-3b-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=4,
    chat_format="chatml"
)
print("Model loaded. Starting server...")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a careful medical information assistant. The user will describe symptoms. Give a brief, clear explanation of possible common causes and simple self-care advice, in a few short sentences. Always remind them to see a doctor if symptoms are severe or last more than a few days. Do NOT ask questions and do NOT list multiple-choice options."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.3
    )
    return jsonify({
        "response": output["choices"][0]["message"]["content"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)