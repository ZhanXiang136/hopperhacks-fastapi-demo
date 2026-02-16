# client_requests.py
import sys
import requests


def get_root(base_url: str) -> None:
    url = f"{base_url}/"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    print("GET / ->", r.json())


def get_items(base_url: str) -> None:
    url = f"{base_url}/items/"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    print("GET /items/ ->", r.json())


def post_item(base_url: str, name: str, price: float, is_offer: bool | None) -> None:
    url = f"{base_url}/items/"
    payload = {"name": name, "price": price, "is_offer": is_offer}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    print("POST /items/ ->", r.json())

def get_item_by_id(base_url: str, item_id: int) -> None:
    url = f"{base_url}/items/{item_id}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    print(f"GET /items/{item_id} ->", r.json())


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

    try:
        get_items(base_url)
        post_item(base_url, name="Apple", price=1.99, is_offer=True)
        post_item(base_url, name="Notebook", price=4.50, is_offer=None)
        get_item_by_id(base_url, item_id=5)
    except requests.HTTPError as e:
        # Print the server response body if available
        resp = e.response
        print(f"HTTP error: {e}")
        if resp is not None:
            print("Status:", resp.status_code)
            print("Body:", resp.text)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()