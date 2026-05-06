from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------- FIFO ----------------
def fifo(pages, capacity):
    memory = []
    faults = 0
    hits = 0
    history = []
    status = []

    for page in pages:
        if page in memory:
            hits += 1
            status.append("hit")
        else:
            faults += 1
            status.append("miss")

            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)

        history.append(memory.copy())

    return {
        "faults": faults,
        "hits": hits,
        "history": history,
        "status": status
    }


# ---------------- LRU ----------------
def lru(pages, capacity):
    memory = []
    faults = 0
    hits = 0
    history = []
    status = []

    for i in range(len(pages)):
        page = pages[i]

        if page in memory:
            hits += 1
            status.append("hit")
        else:
            faults += 1
            status.append("miss")

            if len(memory) < capacity:
                memory.append(page)
            else:
                last_used = {}

                for m in memory:
                    for j in range(i - 1, -1, -1):
                        if pages[j] == m:
                            last_used[m] = j
                            break

                lru_page = min(last_used, key=last_used.get)
                memory[memory.index(lru_page)] = page

        history.append(memory.copy())

    return {
        "faults": faults,
        "hits": hits,
        "history": history,
        "status": status
    }


# ---------------- OPTIMAL ----------------
def optimal(pages, capacity):
    memory = []
    faults = 0
    hits = 0
    history = []
    status = []

    for i in range(len(pages)):
        page = pages[i]

        if page in memory:
            hits += 1
            status.append("hit")
        else:
            faults += 1
            status.append("miss")

            if len(memory) < capacity:
                memory.append(page)
            else:
                future = {}

                for m in memory:
                    if m not in pages[i+1:]:
                        future[m] = float('inf')
                    else:
                        future[m] = pages[i+1:].index(m)

                replace_page = max(future, key=future.get)
                memory[memory.index(replace_page)] = page

        history.append(memory.copy())

    return {
        "faults": faults,
        "hits": hits,
        "history": history,
        "status": status
    }


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.json

    input_str = data["pages"]
    capacity = int(data["capacity"])
    algorithm = data["algorithm"]

    # Handle both formats: "1 2 3" OR "123"
    if " " in input_str:
        pages = list(map(int, input_str.split()))
    else:
        pages = [int(ch) for ch in input_str]

    # Select algorithm
    if algorithm == "fifo":
        result = fifo(pages, capacity)
    elif algorithm == "lru":
        result = lru(pages, capacity)
    elif algorithm == "optimal":
        result = optimal(pages, capacity)
    else:
        result = {
            "faults": 0,
            "hits": 0,
            "history": [],
            "status": []
        }

    return jsonify(result)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)