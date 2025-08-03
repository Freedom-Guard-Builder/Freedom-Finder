import base64

def export_txt(configs: list[str], filename="out/all.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for c in configs:
            f.write(c + "\n")

def export_base64(configs: list[str], filename="out/all_base64.txt"):
    full = "\n".join(configs)
    b64 = base64.b64encode(full.encode()).decode()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(b64)

def export_html_index(configs: list[str], filename="out/index.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("<html><body><h2>Proxy List</h2><pre>\n")
        for c in configs:
            f.write(c + "\n")
        f.write("</pre></body></html>")
