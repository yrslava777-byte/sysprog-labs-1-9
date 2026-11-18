import argparse
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "1.2"))
from brain import get_info, load_core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("webhook", help="URL вебхука n8n")
    parser.add_argument("--library", type=Path, required=True)
    args = parser.parse_args()
    event = get_info(load_core(args.library))
    data = json.dumps(event, ensure_ascii=False).encode("utf-8")
    request = Request(args.webhook, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=10) as response:
        print(f"{event['event']}: HTTP {response.status}")


if __name__ == "__main__":
    main()
