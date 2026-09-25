from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
from scripts.build_rag_context import build_rag_context

from scripts.test_llm_answers import (
    SYSTEM_INSTRUCTIONS,
    build_user_prompt,
)

from scripts.llm_adapter import get_llm_service


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("tones-api")


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="TONES Fashion AI Assistant API",
    description="RAG-powered AI customer assistant for TONES Fashion",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LLM SERVICE
# ============================================================

try:

    llm_provider = os.getenv(
        "TONES_LLM_PROVIDER",
        "openrouter",
    ).lower().strip()

    llm_service = get_llm_service(
        provider=llm_provider
    )

    llm_init_error = None

    logger.info(
        "LLM service initialized successfully. "
        "provider=%s",
        llm_provider,
    )

except Exception as exc:

    llm_service = None

    llm_init_error = str(exc)

    logger.error(
        "LLM service initialization failed: %s",
        exc,
    )


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer message",
    )

    session_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional conversation session ID",
    )


# ============================================================
# PRODUCT RESPONSE MODEL
# ============================================================

class ProductResponse(BaseModel):

    name: str

    url: str

    price: Optional[float] = None

    currency: Optional[str] = None

    color: Optional[str] = None

    fit: Optional[str] = None

    fabric: Optional[str] = None

    listed_sizes: list[str] = []

    currently_in_stock_sizes: list[str] = []


# ============================================================
# CHAT RESPONSE MODEL
# ============================================================

class ChatResponse(BaseModel):

    answer: str

    route: str

    session_id: Optional[str] = None

    products: list[ProductResponse] = []


# ============================================================
# PRODUCT RESPONSE BUILDER
# ============================================================
def build_product_responses(
    context: dict,
) -> list[ProductResponse]:
    """
    Convert the internal RAG product structure into
    safe customer-facing product objects.

    Internal fields such as product_id and score
    are deliberately not exposed.
    """

    products = context.get(
        "products",
        [],
    )

    result = []

    for product in products:

        if not isinstance(product, dict):
            continue

        # ----------------------------------------------------
        # RAG uses "title", not "name"
        # ----------------------------------------------------

        name = str(
            product.get("title") or ""
        ).strip()

        url = str(
            product.get("url") or ""
        ).strip()

        # A product without a title or URL should
        # not become a customer-facing card.
        if not name or not url:
            continue

        # ----------------------------------------------------
        # RAG uses "sizes"
        # ----------------------------------------------------

        listed_sizes = product.get(
            "sizes",
            [],
        )

        # ----------------------------------------------------
        # RAG uses "in_stock_sizes"
        # ----------------------------------------------------

        currently_in_stock_sizes = product.get(
            "in_stock_sizes",
            [],
        )

        if not isinstance(
            listed_sizes,
            list,
        ):
            listed_sizes = []

        if not isinstance(
            currently_in_stock_sizes,
            list,
        ):
            currently_in_stock_sizes = []

        # ----------------------------------------------------
        # Build safe product response
        # ----------------------------------------------------

        result.append(
            ProductResponse(
                name=name,
                url=url,
                price=product.get("price"),
                currency=product.get("currency"),

                color=(
                    str(product.get("color"))
                    if product.get("color")
                    else None
                ),

                fit=(
                    str(product.get("fit"))
                    if product.get("fit")
                    else None
                ),

                fabric=(
                    str(product.get("fabric"))
                    if product.get("fabric")
                    else None
                ),

                listed_sizes=[
                    str(size)
                    for size in listed_sizes
                    if size
                ],

                currently_in_stock_sizes=[
                    str(size)
                    for size in currently_in_stock_sizes
                    if size
                ],
            )
        )

    return result
    



# ============================================================
# ERROR HELPERS
# ============================================================

def is_rate_limit_error(exc: Exception) -> bool:

    error_text = str(exc).lower()

    rate_limit_indicators = [
        "http status: 429",
        "status code: 429",
        "rate limit exceeded",
        "rate_limit",
        "free-models-per-day",
        "too many requests",
    ]

    return any(
        indicator in error_text
        for indicator in rate_limit_indicators
    )


def is_provider_error(exc: Exception) -> bool:

    error_text = str(exc).lower()

    provider_indicators = [
        "openrouter request failed",
        "openrouter api request failed",
        "openrouter returned an invalid json response",
        "openrouter response did not contain",
        "openrouter returned an empty response",
        "llm returned an empty response",
    ]

    return any(
        indicator in error_text
        for indicator in provider_indicators
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "TONES Fashion AI Assistant",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    if llm_service is None:

        return {
            "status": "degraded",
            "llm_configured": False,
        }

    return {
        "status": "healthy",
        "llm_configured": True,
    }


# ============================================================
# CHAT
# ============================================================

@app.post(
    "/api/v1/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    # --------------------------------------------------------
    # CHECK LLM
    # --------------------------------------------------------

    if llm_service is None:

        logger.error(
            "Chat request rejected because LLM service "
            "is unavailable."
        )

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable.",
        )

    try:

        logger.info(
            "Processing chat request | session=%s",
            request.session_id,
        )

        # ----------------------------------------------------
        # STEP 1
        # Build RAG context
        # ----------------------------------------------------

        context = build_rag_context(
            message
        )

        # ----------------------------------------------------
        # STEP 2
        # Build LLM prompt
        # ----------------------------------------------------

        user_prompt = build_user_prompt(
            query=message,
            context=context,
        )

        # ----------------------------------------------------
        # STEP 3
        # Call LLM
        # ----------------------------------------------------

        answer = llm_service.answer(
            system_prompt=SYSTEM_INSTRUCTIONS,
            user_prompt=user_prompt,
        )

        # ----------------------------------------------------
        # STEP 4
        # Validate answer
        # ----------------------------------------------------

        if not answer or not answer.strip():

            logger.error(
                "LLM returned an empty answer."
            )

            raise HTTPException(
                status_code=502,
                detail="AI service returned an empty response.",
            )

        # ----------------------------------------------------
        # STEP 5
        # Route
        # ----------------------------------------------------

        route = context.get(
            "route",
            "UNKNOWN",
        )

        # ----------------------------------------------------
        # STEP 6
        # Build safe product data
        # ----------------------------------------------------

        products = []

        if route in {
            "PRODUCT",
            "MIXED",
        }:

            products = build_product_responses(
                context
            )

        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        logger.info(
            "Chat request completed | route=%s | products=%s | session=%s",
            route,
            len(products),
            request.session_id,
        )

        # ----------------------------------------------------
        # STEP 7
        # RETURN
        # ----------------------------------------------------

        return ChatResponse(
            answer=answer.strip(),
            route=route,
            session_id=request.session_id,
            products=products,
        )

    # ========================================================
    # HTTP EXCEPTIONS
    # ========================================================

    except HTTPException:
        raise

    # ========================================================
    # OPENROUTER RATE LIMIT
    # ========================================================

    except Exception as exc:

        if is_rate_limit_error(exc):

            logger.warning(
                "LLM provider rate limit reached | "
                "session=%s | error=%s",
                request.session_id,
                exc,
            )

            raise HTTPException(
                status_code=429,
                detail=(
                    "AI service rate limit reached. "
                    "Please try again later."
                ),
            ) from exc

        # ----------------------------------------------------
        # PROVIDER ERROR
        # ----------------------------------------------------

        if is_provider_error(exc):

            logger.error(
                "LLM provider error | session=%s | error=%s",
                request.session_id,
                exc,
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "AI service is temporarily unavailable. "
                    "Please try again later."
                ),
            ) from exc

        # ----------------------------------------------------
        # UNKNOWN ERROR
        # ----------------------------------------------------

        logger.exception(
            "Chat request failed | session=%s",
            request.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The AI assistant could not process "
                "the request."
            ),
        ) from exc


# ============================================================
# DIRECT RUN
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )