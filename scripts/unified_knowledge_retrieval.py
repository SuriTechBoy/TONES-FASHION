import json
import re
from pathlib import Path

from scripts.structured_product_search import search as product_search
from scripts.query_router import route_query

BASE_DIR = Path(__file__).resolve().parent.parent

BUSINESS_FILE = (
    BASE_DIR
    / "05_CANONICAL"
    / "business_knowledge_canonical.json"
)


with BUSINESS_FILE.open(encoding="utf-8") as f:
    business_records = json.load(f)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text):
    return re.sub(
        r"\s+",
        " ",
        str(text or "").lower().strip()
    )


# ============================================================
# BUSINESS INTENT DETECTION
# ============================================================

def detect_business_intent(query):
    """
    Detect the user's primary business-information intent.

    This does NOT replace normal keyword retrieval.
    It provides an additional relevance boost so that
    highly specific business questions prefer the matching
    knowledge topic.
    """

    q = normalize(query)

    intents = []

    # --------------------------------------------------------
    # RETURN / EXCHANGE
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "return policy",
            "return my",
            "return this",
            "return product",
            "return item",
            "return an item",
            "returns",
            "return",
            "exchange policy",
            "exchange",
            "refund policy",
            "refund",
        ]
    ):
        intents.append("return_exchange_policy")

    # --------------------------------------------------------
    # SHIPPING / DELIVERY
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "shipping policy",
            "shipping",
            "delivery",
            "delivery time",
            "how long does shipping",
            "how long will shipping",
            "how long does delivery",
            "when will my order arrive",
            "when will my order be delivered",
            "delivery time",
            "shipping time",
        ]
    ):
        intents.append("shipping_policy")

    # --------------------------------------------------------
    # ORDER TRACKING
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "track my order",
            "track order",
            "order tracking",
            "tracking my order",
            "where is my order",
            "where's my order",
            "order status",
            "check my order",
            "check order",
        ]
    ):
        intents.append("order_tracking")

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "payment",
            "payments",
            "pay using",
            "pay with",
            "payment method",
            "payment methods",
            "cod",
            "cash on delivery",
            "cash on delivery",
        ]
    ):
        intents.append("payment_methods")

    # --------------------------------------------------------
    # CUSTOMER SUPPORT / CONTACT
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "contact",
            "contact you",
            "contact tones",
            "customer support",
            "customer service",
            "support team",
            "support",
            "email",
            "contact details",
        ]
    ):
        intents.append("customer_support")

    # --------------------------------------------------------
    # ABOUT / BRAND
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "about tones",
            "about tones fashion",
            "tell me about tones",
            "what is tones",
            "who are tones",
            "about the brand",
            "about your brand",
            "brand information",
        ]
    ):
        intents.append("brand_identity")

    return intents


# ============================================================
# BUSINESS SEARCH
# ============================================================

def business_search(query, top_k=5):

    q = normalize(query)

    query_words = set(
        re.findall(
            r"\b[a-z0-9]+\b",
            q
        )
    )

    detected_intents = detect_business_intent(q)

    results = []

    for record in business_records:

        facts = record.get(
            "facts",
            []
        )

        facts_text = " ".join(
            str(x)
            for x in facts
        )

        domain = normalize(
            record.get(
                "domain",
                ""
            )
        )

        topic = normalize(
            record.get(
                "topic",
                ""
            )
        )

        title = normalize(
            record.get(
                "title",
                ""
            )
        )

        searchable = " ".join([
            domain,
            topic,
            title,
            normalize(facts_text),
        ])

        score = 0

        # ----------------------------------------------------
        # EXISTING GENERIC MATCHING
        # ----------------------------------------------------

        # Exact topic signal
        if topic and topic in q:
            score += 10

        # Exact domain signal
        if domain and domain in q:
            score += 5

        # Word matching
        for word in query_words:

            if word in title:
                score += 3

            elif word in searchable:
                score += 1

        # ----------------------------------------------------
        # INTENT-BASED BOOSTING
        # ----------------------------------------------------

        for intent in detected_intents:

            # Exact topic match
            if topic == intent:
                score += 15

            # Strong domain/topic relationships
            if intent == "return_exchange_policy":

                if topic == "return_exchange_policy":
                    score += 12

                elif domain == "returns":
                    score += 8

                elif "return" in title:
                    score += 8

                elif "exchange" in title:
                    score += 6

            elif intent == "shipping_policy":

                if topic == "shipping_policy":
                    score += 15

                elif domain == "shipping":
                    score += 8

                elif "shipping" in title:
                    score += 8

                elif "delivery" in title:
                    score += 6

            elif intent == "order_tracking":

                if topic == "order_tracking":
                    score += 15

                elif domain == "orders":
                    score += 8

                elif "track" in title:
                    score += 8

                elif "tracking" in title:
                    score += 8

            elif intent == "payment_methods":

                if topic == "payment_methods":
                    score += 15

                elif domain == "payment":
                    score += 8

                elif "payment" in title:
                    score += 8

            elif intent == "customer_support":

                if topic == "customer_support":
                    score += 15

                elif domain == "business":
                    score += 6

                elif "contact" in title:
                    score += 8

                elif "support" in title:
                    score += 8

            elif intent == "brand_identity":

                if topic == "brand_identity":
                    score += 15

                elif domain == "business":
                    score += 6

                elif "about" in title:
                    score += 8

        # ----------------------------------------------------
        # GENERIC "POLICY" PENALTY
        # ----------------------------------------------------
        #
        # "policy" by itself should not make Privacy Policy,
        # Terms of Service, etc. outrank a specific policy.
        #
        # Example:
        #
        # "what is your return policy"
        #
        # should prefer:
        # Return and Exchange Policy
        #
        # over:
        # Privacy Policy
        # Terms of Service
        #

        if "return_exchange_policy" in detected_intents:

            if topic not in (
                "return_exchange_policy",
            ):
                if domain == "policy":
                    score -= 5

        if "shipping_policy" in detected_intents:

            if topic not in (
                "shipping_policy",
            ):
                if domain == "policy":
                    score -= 5

        if "payment_methods" in detected_intents:

            if topic not in (
                "payment_methods",
            ):
                if domain == "policy":
                    score -= 3

        # ----------------------------------------------------
        # KEEP ONLY RELEVANT RESULTS
        # ----------------------------------------------------

        if score > 0:

            results.append({
                "score": score,
                "record": record,
            })

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# UNIFIED RETRIEVAL
# ============================================================

def unified_retrieve(
    query,
    product_top_k=10,
    business_top_k=5,
):

    routing = route_query(query)

    route = routing["route"]

    product_results = []
    business_results = []

    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    if route in (
        "PRODUCT",
        "MIXED",
    ):

        filters, matches = product_search(
            query,
            top_k=product_top_k
        )

        product_results = [
            {
                "score": score,
                "product": product,
            }
            for score, product in matches
        ]

    # --------------------------------------------------------
    # BUSINESS
    # --------------------------------------------------------

    if route in (
        "BUSINESS",
        "MIXED",
    ):

        business_results = business_search(
            query,
            top_k=business_top_k
        )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {
        "query": query,

        "route": route,

        "routing": routing,

        "product_results": product_results,

        "business_results": business_results,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    queries = [

        "black oversized t shirt",

        "what is your return policy",

        "how long does shipping take",

        "how can I track my order",

        "can I pay using COD",

        "black t shirt and can I return it",

    ]

    print()

    print("=" * 70)

    print(
        "TONES UNIFIED KNOWLEDGE RETRIEVAL"
    )

    print("=" * 70)

    for query in queries:

        result = unified_retrieve(
            query
        )

        print()

        print("=" * 70)

        print(
            "QUERY:",
            query
        )

        print(
            "ROUTE:",
            result["route"]
        )

        print("=" * 70)

        print()

        print(
            "PRODUCT RESULTS"
        )

        if not result["product_results"]:

            print(
                "None"
            )

        else:

            for item in result["product_results"]:

                product = item["product"]

                print(
                    f"{product.get('name')} "
                    f"| Score: {item['score']}"
                )

        print()

        print(
            "BUSINESS RESULTS"
        )

        if not result["business_results"]:

            print(
                "None"
            )

        else:

            for item in result["business_results"]:

                record = item["record"]

                print(
                    f"{record.get('knowledge_id')} "
                    f"| {record.get('topic')} "
                    f"| {record.get('status')} "
                    f"| Score: {item['score']}"
                )