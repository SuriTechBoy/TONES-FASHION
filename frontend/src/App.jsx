import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "";
const SUGGESTED_QUESTIONS = [
  "Show me black t-shirts",
  "Show me oversized t-shirts under ₹1000",
  "What is your return policy?",
  "How can I track my order?",
  "Can I pay using COD?",
];

const FEATURE_ITEMS = [
  { icon: "✦", title: "AI Shopping Assistant", text: "Ask naturally about products, sizes, prices, shipping, returns and more." },
  { icon: "⌁", title: "Smart Product Search", text: "Find products using colour, fit, category and budget-style requests." },
  { icon: "◈", title: "Verified Knowledge", text: "Answers are grounded in the current TONES Fashion knowledge base." },
  { icon: "↗", title: "Product Discovery", text: "Open matching products directly from the assistant." },
];

const FLOATING_GARMENTS = [
  { type: "tee", label: "TEE", className: "garment-one" },
  { type: "hoodie", label: "HOODIE", className: "garment-two" },
  { type: "shirt", label: "SHIRT", className: "garment-three" },
  { type: "tee", label: "TEE", className: "garment-four" },
];

function GarmentSvg({ type }) {
  if (type === "hoodie") {
    return (
      <svg viewBox="0 0 220 260" className="garment-svg" aria-hidden="true">
        <defs>
          <linearGradient id="hoodieGradient" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor="#ec4899" />
          </linearGradient>
        </defs>
        <path d="M76 42c8-20 60-20 68 0l30 25 30 80-31 13-14-42v91H61v-91l-14 42-31-13 30-80z" fill="url(#hoodieGradient)" />
        <path d="M77 43c8 30 58 30 66 0" fill="none" stroke="rgba(255,255,255,.65)" strokeWidth="6" />
        <path d="M72 174h76v31H72z" fill="rgba(255,255,255,.16)" />
        <path d="M92 62c10 8 26 8 36 0" fill="none" stroke="rgba(255,255,255,.7)" strokeWidth="3" />
      </svg>
    );
  }
  if (type === "shirt") {
    return (
      <svg viewBox="0 0 220 260" className="garment-svg" aria-hidden="true">
        <defs>
          <linearGradient id="shirtGradient" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#06b6d4" />
            <stop offset="100%" stopColor="#2563eb" />
          </linearGradient>
        </defs>
        <path d="M72 48l36-18h4c7 12 19 12 26 0h4l36 18 27 34-30 24-12-18v91H57V88L45 106 15 82z" fill="url(#shirtGradient)" />
        <path d="M103 32c4 15 10 22 17 22s13-7 17-22" fill="none" stroke="rgba(255,255,255,.75)" strokeWidth="5" />
        <path d="M75 125h70" stroke="rgba(255,255,255,.22)" strokeWidth="4" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 220 260" className="garment-svg" aria-hidden="true">
      <defs>
        <linearGradient id="teeGradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f97316" />
          <stop offset="50%" stopColor="#f43f5e" />
          <stop offset="100%" stopColor="#a855f7" />
        </linearGradient>
      </defs>
      <path d="M71 42l37-17h4l37 17 46 36-29 35-17-16v80H71V97L54 113 25 78z" fill="url(#teeGradient)" />
      <path d="M98 27c4 17 20 17 24 0" fill="none" stroke="rgba(255,255,255,.75)" strokeWidth="5" />
      <path d="M78 126h64" stroke="rgba(255,255,255,.22)" strokeWidth="4" />
      <circle cx="110" cy="158" r="14" fill="rgba(255,255,255,.18)" />
    </svg>
  );
}
function Home({ onOpenAssistant }) {
  return (
    <div className="home-page">

      {/* The video belongs ONLY to the opening hero section.
          It must not cover the rest of the homepage. */}
      <div className="home-noise" />

      {/* =====================================================
          HERO SECTION — VIDEO BACKGROUND ONLY HERE
          ===================================================== */}
      <section className="hero-section">

        <video
          className="hero-background-video"
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          aria-hidden="true"
        >
          <source src="/videos/tones-hero.mp4" type="video/mp4" />
        </video>

        <div className="hero-video-overlay" />

        <div className="hero-copy">

          <div className="eyebrow">
            <span className="eyebrow-dot" />
            TONES FASHION · AI SHOPPING
          </div>

          <h1>
            Wear your vibe.
            <br />
            <span>Ask the AI.</span>
          </h1>

          <p className="hero-description">
            Discover TONES Fashion through a smarter shopping experience.
            Ask for a style, colour, fit or budget — and let the assistant
            find it.
          </p>

          <div className="hero-actions">

            <button
              className="primary-cta"
              onClick={onOpenAssistant}
            >
              Open AI Assistant <span>↗</span>
            </button>

            <button
              className="ghost-cta"
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({
                    behavior: "smooth",
                  })
              }
            >
              Explore features ↓
            </button>

          </div>

          <div className="hero-proof">

            <div className="proof-item">
              <strong>AI</strong>
              <span>RAG powered</span>
            </div>

            <div className="proof-line" />

            <div className="proof-item">
              <strong>24/7</strong>
              <span>Always ready</span>
            </div>

            <div className="proof-line" />

            <div className="proof-item">
              <strong>∞</strong>
              <span>Natural queries</span>
            </div>

          </div>

        </div>

        {/* ===================================================
            ANIMATED FASHION STAGE
            =================================================== */}
        <div
          className="fashion-stage"
          aria-label="Animated TONES Fashion garments"
        >

          <div className="stage-glow glow-a" />
          <div className="stage-glow glow-b" />

          <div className="orbit orbit-a" />
          <div className="orbit orbit-b" />

          <div className="stage-core">

            <div className="core-ring" />

            <div className="core-label">
              TONES
              <br />
              <span>AI</span>
            </div>

          </div>

          {FLOATING_GARMENTS.map((garment) => (
            <div
              className={`floating-garment ${garment.className}`}
              key={garment.className}
            >
              <div className="garment-card">

                <GarmentSvg type={garment.type} />

                <span>{garment.label}</span>

              </div>
            </div>
          ))}

          <div className="floating-chip chip-one">
            BLACK · OVERSIZED
          </div>

          <div className="floating-chip chip-two">
            UNDER ₹1000
          </div>

          <div className="floating-chip chip-three">
            SMART SEARCH ✦
          </div>

        </div>

      </section>

      {/* =====================================================
          MARQUEE
          ===================================================== */}
      <div
        className="marquee-wrap"
        aria-hidden="true"
      >
        <div className="marquee-track">

          {Array.from({ length: 2 })
            .flatMap((_, row) =>
              [
                "STREETWEAR",
                "AI SHOPPING",
                "TONES FASHION",
                "FIND YOUR FIT",
                "STYLE · SEARCH · DISCOVER",
              ].map((text, i) => (
                <span key={`${row}-${i}`}>
                  {text} <b>✦</b>
                </span>
              ))
            )}

        </div>
      </div>

      {/* =====================================================
          FEATURES
          ===================================================== */}
      <section
        className="feature-section"
        id="features"
      >

        <div className="section-heading">

          <div className="eyebrow">
            WHY TONES AI
          </div>

          <h2>
            More than a chatbot.
            <br />
            <span>A shopping companion.</span>
          </h2>

          <p>
            The current MVP connects the customer-facing experience
            to your existing FastAPI + RAG + Mock LLM stack.
          </p>

        </div>

        <div className="feature-grid">

          {FEATURE_ITEMS.map((item, index) => (
            <article
              className="feature-card"
              key={item.title}
            >

              <div className="feature-number">
                0{index + 1}
              </div>

              <div className="feature-icon">
                {item.icon}
              </div>

              <h3>
                {item.title}
              </h3>

              <p>
                {item.text}
              </p>

              <div className="feature-arrow">
                ↗
              </div>

            </article>
          ))}

        </div>

      </section>

      {/* =====================================================
          DISCOVER / QUERY CLOUD
          ===================================================== */}
      <section className="discover-section">

        <div className="discover-panel">

          <div>

            <div className="eyebrow">
              TRY IT YOUR WAY
            </div>

            <h2>
              From “black tee”
              <br />
              to <span>“find my fit.”</span>
            </h2>

            <p>
              Natural language is the interface.
              No filters to fight with. Just ask.
            </p>

          </div>

          <div className="query-cloud">

            {[
              "Black oversized tee",
              "Under ₹800",
              "What sizes?",
              "Return policy",
              "COD?",
              "Track my order",
            ].map((q, i) => (
              <button
                key={q}
                style={{ "--i": i }}
                onClick={onOpenAssistant}
              >
                {q}
              </button>
            ))}

          </div>

        </div>

      </section>

      {/* =====================================================
          FOOTER
          ===================================================== */}
      <footer className="home-footer">

        <strong>
          TONES Fashion AI
        </strong>

        <span>
          RAG · Knowledge · Conversation
        </span>

      </footer>

    </div>
  );
}
function ProductCard({ product }) {
  return (
    <div className="product-card">
      <div className="product-image-placeholder">
        <GarmentSvg type="tee" />
        <span className="product-image-badge">TONES</span>
      </div>
      <div className="product-card-content">
        <div className="product-title">{product.name}</div>
        {product.price !== null && product.price !== undefined && <div className="product-price">₹{Number(product.price).toLocaleString("en-IN")}</div>}
        <div className="product-details">
          {product.color && <div><span className="detail-label">Color:</span> {product.color}</div>}
          {product.fit && <div><span className="detail-label">Fit:</span> {product.fit}</div>}
          {product.fabric && <div><span className="detail-label">Fabric:</span> {product.fabric}</div>}
        </div>
        {product.listed_sizes?.length > 0 && <div className="size-section"><div className="size-title">Listed sizes</div><div className="size-list">{product.listed_sizes.map((size) => <span key={size} className="size-pill">{size}</span>)}</div></div>}
        {product.currently_in_stock_sizes?.length > 0 && <div className="stock-section"><div className="stock-title">Recorded in-stock sizes</div><div className="stock-list">{product.currently_in_stock_sizes.map((size) => <span key={size} className="stock-pill">{size}</span>)}</div><div className="stock-note">Based on the current knowledge snapshot. This is not live inventory.</div></div>}
        <a href={product.url} target="_blank" rel="noreferrer" className="view-product-button">View Product ↗</a>
      </div>
    </div>
  );
}

function Assistant({ onHome }) {
  const [messages, setMessages] = useState([{ id: 1, role: "assistant", content: "Hi! 👋 I'm the TONES Fashion AI Assistant. What are you looking for today?", products: [] }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [voiceSupported, setVoiceSupported] = useState(true);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setVoiceSupported(false);
      return undefined;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-IN";

    recognition.onstart = () => setIsListening(true);

    recognition.onresult = (event) => {
      let transcript = "";
      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        transcript += event.results[index][0].transcript;
      }
      setInput(transcript.trim());
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setIsListening(false);
    };

    recognition.onend = () => setIsListening(false);
    recognitionRef.current = recognition;

    return () => {
      try {
        recognition.stop();
      } catch {
        // Recognition may already be stopped when the component unmounts.
      }
      recognitionRef.current = null;
    };
  }, []);

  const toggleVoiceInput = () => {
    if (loading) return;

    if (!voiceSupported || !recognitionRef.current) {
      setInput((current) => current);
      window.alert("Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      return;
    }

    try {
      setInput("");
      recognitionRef.current.start();
    } catch (error) {
      console.error("Could not start speech recognition:", error);
    }
  };

  const sendMessage = async (question = null) => {
    const message = (question ?? input).trim();
    if (!message || loading) return;

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
    }

    setMessages((previous) => [...previous, { id: Date.now(), role: "user", content: message, products: [] }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "The AI assistant could not process the request.");

      setMessages((previous) => [
        ...previous,
        { id: Date.now() + 1, role: "assistant", content: data.answer, products: data.products || [] },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: error.message || "Something went wrong. Please try again.",
          products: [],
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    if (loading) return;
    if (isListening && recognitionRef.current) recognitionRef.current.stop();
    setMessages([{ id: Date.now(), role: "assistant", content: "Hi! 👋 I'm the TONES Fashion AI Assistant. What are you looking for today?", products: [] }]);
    setInput("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="assistant-page">
      <header className="assistant-header">
        <button className="brand-button" onClick={onHome}>
          <span className="brand-mark">T</span>
          <span><strong>TONES</strong><small>FASHION AI</small></span>
        </button>
        <div className="assistant-header-right">
          <div className="live-status"><i /> AI Assistant online</div>
          <button className="new-chat-button" onClick={startNewChat} disabled={loading}>＋ New Chat</button>
        </div>
      </header>

      <main className="chat-container">
        {messages.length === 1 && !loading && (
          <section className="assistant-welcome">
            <div className="welcome-orb"><span>T</span></div>
            <div>
              <div className="welcome-badge">TONES AI · RAG ASSISTANT</div>
              <h1>What can we find<br /><span>for you?</span></h1>
              <p>Ask about products, sizes, prices, shipping, returns, orders and more.</p>
            </div>
          </section>
        )}

        <section className="messages">
          {messages.map((message) => (
            <div key={message.id} className={`message-row ${message.role}`}>
              {message.role === "assistant" && <div className="assistant-avatar">T</div>}
              <div className="message-group">
                <div className={`message ${message.error ? "error-message" : ""}`}>{message.content}</div>
                {message.products?.length > 0 && (
                  <div className="product-grid">
                    {message.products.map((product, index) => (
                      <ProductCard key={`${product.url}-${index}`} product={product} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="assistant-avatar">T</div>
              <div className="message typing-message"><span /><span /><span /></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </section>

        {!loading && (
          <section className="suggestions">
            <div className="suggestions-title">TRY ASKING</div>
            <div className="suggestion-list">
              {SUGGESTED_QUESTIONS.map((question) => (
                <button key={question} className="suggestion-button" onClick={() => sendMessage(question)}>
                  {question}
                </button>
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="input-area">
        <div className="input-wrapper">
          <div className="input-leading-mark" aria-hidden="true">T</div>

          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isListening ? "Listening… speak your TONES question" : "Ask TONES AI anything..."}
            rows="1"
            disabled={loading}
            aria-label="Ask TONES AI"
          />

          <button
            type="button"
            className={`voice-button ${isListening ? "is-listening" : ""}`}
            onClick={toggleVoiceInput}
            disabled={loading}
            aria-label={isListening ? "Stop voice input" : "Start voice input"}
            title={voiceSupported ? (isListening ? "Stop listening" : "Speak your question") : "Voice input is not supported in this browser"}
          >
            <span className="voice-icon" aria-hidden="true">
              {isListening ? (
                <span className="stop-icon" />
              ) : (
                <svg viewBox="0 0 24 24" focusable="false">
                  <path d="M12 15.5a3.5 3.5 0 0 0 3.5-3.5V7a3.5 3.5 0 0 0-7 0v5a3.5 3.5 0 0 0 3.5 3.5Z" />
                  <path d="M5 11.5a7 7 0 0 0 14 0M12 18.5V22M8.5 22h7" />
                </svg>
              )}
            </span>
            {isListening && <span className="voice-pulse" />}
          </button>

          <button
            className="send-button"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            aria-label="Send message"
            title="Send message"
          >
            <span>➤</span>
          </button>
        </div>

        <div className={`voice-status ${isListening ? "active" : ""}`}>
          <span className="voice-status-dot" />
          {isListening ? "Listening — speak your question" : "Type or use the microphone to ask TONES AI"}
        </div>

        <div className="input-note"><span>●</span> TONES Fashion AI Assistant · Answers grounded in current knowledge</div>
      </footer>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("home");
  return page === "home" ? <Home onOpenAssistant={() => setPage("assistant")} /> : <Assistant onHome={() => setPage("home")} />;
}
