"""Read the public original member directory for the website migration."""
from html.parser import HTMLParser
import json
from urllib.parse import urljoin
from urllib.request import Request, urlopen

URL = "https://aireqlab.uta.edu/cp_school_directory/members/"
class DirectoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.items = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if self.skip:
            return
        if tag == "img":
            item = {"kind": "image", "alt": attrs.get("alt", "")}
            for key in ("src", "data-src", "srcset", "data-srcset"):
                if attrs.get(key):
                    value = attrs[key]
                    item[key] = urljoin(URL, value) if key.endswith("src") else value
            self.items.append(item)
        if tag == "a" and attrs.get("href", "").startswith("mailto:"):
            self.items.append({"kind": "email", "value": attrs["href"]})
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
    def handle_data(self, value):
        if not self.skip:
            value = " ".join(value.split())
            if value:
                self.items.append({"kind": "text", "value": value[:3000]})

try:
    request = Request(URL, headers={"User-Agent": "AIRE-Q website migration (public directory read)"})
    with urlopen(request, timeout=25) as response:
        content = response.read(3000000).decode("utf-8", errors="replace")
        status = response.status
    parser = DirectoryParser()
    parser.feed(content)
    print("MEMBER_DIRECTORY_JSON_START")
    print(json.dumps({"url": URL, "status": status, "items": parser.items}, ensure_ascii=True))
    print("MEMBER_DIRECTORY_JSON_END")
except Exception as error:
    print("MEMBER_DIRECTORY_ERROR", type(error).__name__, str(error))
    raise
