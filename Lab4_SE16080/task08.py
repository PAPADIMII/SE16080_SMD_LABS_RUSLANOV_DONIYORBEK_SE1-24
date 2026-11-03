# Task 8 — One search method, no mutable default
# 8.3 A keyword-only filters dictionary keeps filter conditions grouped and explicit.
class ProductSearch:
    def __init__(self, products):
        self.products = products

    def search(self, query, *, filters=None):
        q = query.lower()
        result = [p for p in self.products if q in p["title"].lower()]
        if filters is not None:
            for key, value in filters.items():
                result = [p for p in result if p.get(key) == value]
        return result

def test_search_with_and_without_filters():
    ps = ProductSearch([
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 14", "brand": "Apple"},
        {"title": "Galaxy S24", "brand": "Samsung"},
    ])
    assert len(ps.search("iphone")) == 2
    assert ps.search("iphone", filters={"brand": "Apple"}) == [
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 14", "brand": "Apple"},
    ]
