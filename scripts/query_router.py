import re


# ============================================================
# QUERY ROUTER
# ============================================================

PRODUCT_TERMS = [
    "product",
    "products",
    "buy",
    "purchase",
    "price",
    "cost",
    "size",
    "sizes",
    "fit",
    "color",
    "colour",
    "fabric",
    "material",
    "t shirt",
    "t-shirt",
    "tshirt",
    "tee",
    "tees",
    "shirt",
    "shirts",
    "sweatshirt",
    "sweatshirts",
    "kurta",
    "kurtas",
    "cargo",
    "cargos",
    "chino",
    "chinos",
    "jacket",
    "jackets",
    "in stock",
    "available",
    "availability",
    "under ₹",
    "under rs",
    "under ",
    "below ",
]


BUSINESS_TERMS = [
    "return",
    "returns",
    "exchange",
    "refund",
    "refunds",
    "policy",
    "shipping",
    "delivery",
    "deliver",
    "dispatch",
    "track order",
    "tracking",
    "order tracking",
    "order status",
    "cancel order",
    "cancellation",
    "payment",
    "pay",
    "cod",
    "cash on delivery",
    "upi",
    "card",
    "privacy",
    "terms",
    "support",
    "contact",
    "customer service",
    "complaint",
    "damaged",
    "defective",
    "wrong product",
    "about tones",
    "about the brand",
    "brand",
    "company",
]


def normalize(text):
    return re.sub(
        r"\s+",
        " ",
        str(text or "").lower().strip()
    )


def contains_term(query, term):
    """
    Avoid some accidental substring matches.

    Multi-word phrases use direct matching.
    Single words use word boundaries.
    """

    if " " in term or "-" in term:

        return term in query

    return bool(
        re.search(
            rf"\b{re.escape(term)}\b",
            query
        )
    )


def route_query(query):

    q = normalize(query)

    product_hits = [
        term
        for term in PRODUCT_TERMS
        if contains_term(q, term)
    ]

    business_hits = [
        term
        for term in BUSINESS_TERMS
        if contains_term(q, term)
    ]

    # --------------------------------------------------------
    # Strong business intent
    # --------------------------------------------------------

    strong_business_phrases = [
        "return policy",
        "return my",
        "exchange policy",
        "refund",
        "shipping",
        "delivery",
        "track my order",
        "track order",
        "order tracking",
        "cancel my order",
        "cancellation",
        "cash on delivery",
        "cod",
        "payment",
        "privacy policy",
        "terms of service",
    ]

    if any(
        phrase in q
        for phrase in strong_business_phrases
    ):
        return {
            "route": "BUSINESS",
            "product_hits": product_hits,
            "business_hits": business_hits,
        }

    # --------------------------------------------------------
    # Product + business mixed query
    # --------------------------------------------------------

    if product_hits and business_hits:

        return {
            "route": "MIXED",
            "product_hits": product_hits,
            "business_hits": business_hits,
        }

    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    if product_hits:

        return {
            "route": "PRODUCT",
            "product_hits": product_hits,
            "business_hits": business_hits,
        }

    # --------------------------------------------------------
    # Business
    # --------------------------------------------------------

    if business_hits:

        return {
            "route": "BUSINESS",
            "product_hits": product_hits,
            "business_hits": business_hits,
        }

    # --------------------------------------------------------
    # Unknown / general
    # --------------------------------------------------------

    return {
        "route": "GENERAL",
        "product_hits": [],
        "business_hits": [],
    }


if __name__ == "__main__":

    queries = [
        "black oversized t shirt",
        "black t shirts under 1000",
        "XL t shirts in stock",
        "sweatshirts under 1500",

        "what is your return policy",
        "how long does shipping take",
        "how can I track my order",
        "can I pay using COD",

        "black t shirt and can I return it",
        "tell me about TONES Fashion",
        "hello",
    ]

    print()
    print("TONES QUERY ROUTER")
    print("=" * 60)

    for query in queries:

        result = route_query(query)

        print()
        print("QUERY:", query)
        print("ROUTE:", result["route"])
        print(
            "PRODUCT HITS:",
            result["product_hits"]
        )
        print(
            "BUSINESS HITS:",
            result["business_hits"]
        )