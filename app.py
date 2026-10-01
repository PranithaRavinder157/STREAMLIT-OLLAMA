import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import ollama
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MARVEL // RAG COMMAND",
    page_icon="🦸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# MARVEL ADVENTURE UI
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Oswald', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(255, 30, 30, 0.22),
            transparent 35%
        ),
        radial-gradient(
            circle at 0% 50%,
            rgba(255, 190, 0, 0.08),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #030303 0%,
            #090909 45%,
            #050505 100%
        );

    color: #ffffff;
}


/* =========================================================
   BACKGROUND COMIC LINES
   ========================================================= */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    opacity: 0.10;

    background-image:
        repeating-linear-gradient(
            45deg,
            transparent,
            transparent 28px,
            #ffffff 29px,
            transparent 30px
        );

    z-index: 0;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {

    max-width: 1250px;

    padding-top: 25px !important;
    padding-bottom: 60px !important;

    position: relative;

    z-index: 1;
}


/* =========================================================
   TOP MARVEL STRIP
   ========================================================= */

.top-strip {

    height: 7px;

    background:
        linear-gradient(
            90deg,
            #7a0000,
            #ed1d24,
            #ffcc00,
            #ed1d24,
            #7a0000
        );

    box-shadow:
        0 0 18px rgba(237, 29, 36, 0.8);

    margin-bottom: 25px;
}


/* =========================================================
   LOGO
   ========================================================= */

.marvel-logo {

    display: inline-block;

    background: #ed1d24;

    color: white;

    font-family: 'Bebas Neue', sans-serif;

    font-size: 42px;

    letter-spacing: 4px;

    padding: 3px 22px 1px 22px;

    border: 4px solid white;

    box-shadow:
        7px 7px 0px #000,
        0 0 18px rgba(237,29,36,0.6);

    transform: skew(-3deg);

    margin-bottom: 15px;
}


/* =========================================================
   HERO TITLE
   ========================================================= */

.hero-title {

    font-family: 'Bebas Neue', sans-serif;

    font-size: 76px;

    line-height: 0.95;

    letter-spacing: 3px;

    color: #ffffff;

    text-transform: uppercase;

    text-shadow:
        5px 5px 0px #ed1d24,
        9px 9px 0px #000;

    margin: 5px 0 12px 0;
}


.hero-subtitle {

    font-size: 20px;

    color: #cfcfcf;

    letter-spacing: 1.5px;

    margin-bottom: 25px;
}


/* =========================================================
   COMIC DIVIDER
   ========================================================= */

.comic-divider {

    height: 5px;

    background:
        linear-gradient(
            90deg,
            #ed1d24 0%,
            #ed1d24 35%,
            #ffcc00 35%,
            #ffcc00 65%,
            #ed1d24 65%,
            #ed1d24 100%
        );

    margin: 20px 0 30px 0;

    box-shadow:
        0 0 12px rgba(237,29,36,0.5);
}


/* =========================================================
   MISSION PANEL
   ========================================================= */

.mission-panel {

    position: relative;

    background:
        linear-gradient(
            145deg,
            #171717,
            #0b0b0b
        );

    border: 2px solid #333;

    border-left: 8px solid #ed1d24;

    padding: 28px;

    margin: 20px 0 30px 0;

    box-shadow:
        10px 10px 0 #000,
        0 0 25px rgba(237,29,36,0.15);
}


.mission-panel::after {

    content: "MISSION";

    position: absolute;

    top: 12px;

    right: 18px;

    color: #555;

    font-size: 12px;

    font-weight: bold;

    letter-spacing: 3px;
}


.mission-title {

    font-family: 'Bebas Neue', sans-serif;

    font-size: 30px;

    color: #ffcc00;

    letter-spacing: 2px;

    margin-bottom: 8px;
}


.mission-text {

    color: #cccccc;

    font-size: 16px;

    line-height: 1.6;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-heading {

    display: flex;

    align-items: center;

    gap: 12px;

    margin: 30px 0 15px 0;

    font-family: 'Bebas Neue', sans-serif;

    font-size: 30px;

    letter-spacing: 2px;

    color: white;
}


.section-heading span {

    color: #ed1d24;

    font-size: 35px;
}


/* =========================================================
   UPLOAD AREA
   ========================================================= */

[data-testid="stFileUploader"] {

    background:
        linear-gradient(
            135deg,
            rgba(237,29,36,0.08),
            rgba(255,204,0,0.03)
        );

    border: 2px dashed #ed1d24;

    border-radius: 4px;

    padding: 25px;

    box-shadow:
        inset 0 0 25px rgba(237,29,36,0.04),
        0 0 15px rgba(237,29,36,0.08);
}


[data-testid="stFileUploader"] section {

    background: transparent !important;
}


/* =========================================================
   FILE UPLOADER TEXT
   ========================================================= */

[data-testid="stFileUploader"] label {

    color: white !important;

    font-size: 17px !important;

    font-weight: 600 !important;
}


/* =========================================================
   STATS
   ========================================================= */

.stats-row {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;

    margin: 20px 0;
}


.stat-box {

    background: #101010;

    border: 1px solid #333;

    border-top: 4px solid #ed1d24;

    padding: 20px;

    text-align: center;

    box-shadow:
        5px 5px 0 #000;
}


.stat-number {

    font-family: 'Bebas Neue', sans-serif;

    font-size: 36px;

    color: #ffcc00;

    letter-spacing: 2px;
}


.stat-label {

    font-size: 12px;

    color: #888;

    letter-spacing: 2px;

    text-transform: uppercase;
}


/* =========================================================
   INPUT AREA
   ========================================================= */

.question-panel {

    background:
        linear-gradient(
            145deg,
            #151515,
            #090909
        );

    border: 2px solid #333;

    border-radius: 3px;

    padding: 25px;

    margin-top: 20px;

    box-shadow:
        8px 8px 0 #000;
}


/* =========================================================
   TEXT INPUT
   ========================================================= */

.stTextInput > div > div > input {

    background: #050505 !important;

    color: #ffffff !important;

    border: 2px solid #444 !important;

    border-radius: 3px !important;

    padding: 16px !important;

    font-size: 17px !important;

    transition: all 0.2s ease;
}


.stTextInput > div > div > input:focus {

    border: 2px solid #ed1d24 !important;

    box-shadow:
        0 0 15px rgba(237,29,36,0.35) !important;
}


/* =========================================================
   INPUT LABEL
   ========================================================= */

.stTextInput label {

    color: #ffcc00 !important;

    font-weight: 700 !important;

    letter-spacing: 1px;
}


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {

    background: #0c0c0c;

    border: 1px solid #333;

    border-radius: 3px;

    margin-top: 20px;
}


[data-testid="stExpander"] summary {

    color: #ffcc00 !important;

    font-weight: 700 !important;

    letter-spacing: 1px;
}


/* =========================================================
   ANSWER PANEL
   ========================================================= */

.answer-panel {

    position: relative;

    background:
        linear-gradient(
            145deg,
            #191919,
            #080808
        );

    border: 2px solid #444;

    border-left: 9px solid #ed1d24;

    padding: 30px;

    margin-top: 20px;

    box-shadow:
        10px 10px 0 #000,
        0 0 25px rgba(237,29,36,0.12);
}


.answer-panel::before {

    content: "AI";

    position: absolute;

    top: -18px;

    left: 20px;

    background: #ed1d24;

    color: white;

    font-family: 'Bebas Neue', sans-serif;

    font-size: 20px;

    padding: 4px 15px;

    border: 2px solid white;

    box-shadow: 4px 4px 0 #000;
}


.answer-title {

    font-family: 'Bebas Neue', sans-serif;

    color: #ffcc00;

    font-size: 32px;

    letter-spacing: 2px;

    margin-bottom: 15px;
}


.answer-text {

    color: #eeeeee;

    font-size: 17px;

    line-height: 1.8;

    white-space: pre-wrap;
}


/* =========================================================
   COMIC SPEECH BUBBLE
   ========================================================= */

.question-bubble {

    position: relative;

    background: white;

    color: #080808;

    padding: 14px 20px;

    display: inline-block;

    font-family: 'Bebas Neue', sans-serif;

    font-size: 22px;

    letter-spacing: 1px;

    border: 3px solid #000;

    box-shadow: 6px 6px 0 #ed1d24;

    margin-bottom: 20px;
}


/* =========================================================
   SUCCESS / INFO / ERROR
   ========================================================= */

[data-testid="stAlert"] {

    border-radius: 3px !important;

    border-left-width: 5px !important;
}


/* =========================================================
   SPINNER
   ========================================================= */

.stSpinner > div {

    border-top-color: #ed1d24 !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    margin-top: 60px;

    padding-top: 25px;

    border-top: 2px solid #222;

    text-align: center;

    color: #666;

    font-size: 13px;

    letter-spacing: 1px;
}


.footer strong {

    color: #ed1d24;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 700px) {

    .hero-title {

        font-size: 50px;

    }

    .marvel-logo {

        font-size: 30px;

    }

    .stats-row {

        grid-template-columns: 1fr;

    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="top-strip"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="marvel-logo">MARVEL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">DOCUMENT<br>ADVENTURE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'YOUR PDF IS THE MISSION. &nbsp; YOUR QUESTION IS THE CHALLENGE.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="comic-divider"></div>',
    unsafe_allow_html=True
)


# ============================================================
# MISSION INTRO
# ============================================================

st.markdown("""
<div class="mission-panel">

<div class="mission-title">
⚡ WELCOME, HERO
</div>

<div class="mission-text">

Your mission is simple: upload a PDF, explore its knowledge,
and ask questions about it.

The RAG engine searches your document using semantic
embeddings and ChromaDB, then Ollama generates an answer
using the retrieved information.

<strong style="color:#ed1d24;">
NO GUESSING. NO RANDOM ANSWERS. JUST YOUR DOCUMENT.
</strong>

</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# UPLOAD
# ============================================================

st.markdown("""
<div class="section-heading">
<span>01</span>
CHOOSE YOUR MISSION FILE
</div>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    "📁 Upload your PDF",
    type=["pdf"]
)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    st.success(
        "⚡ MISSION FILE RECEIVED — Preparing document intelligence..."
    )

    # ========================================================
    # READ PDF
    # ========================================================

    reader = PdfReader(uploaded_file)

    page_count = len(reader.pages)

    # ========================================================
    # EXTRACT TEXT
    # ========================================================

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"


    # ========================================================
    # CHECK TEXT
    # ========================================================

    if not text.strip():

        st.error(
            "❌ Mission failed: No readable text could be extracted."
        )

        st.stop()


    # ========================================================
    # CHUNKS
    # ========================================================

    chunk_size = 500

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunk = text[
            i:i + chunk_size
        ]

        if chunk.strip():

            chunks.append(chunk)


    # ========================================================
    # STATS
    # ========================================================

    st.markdown(
        f"""
        <div class="stats-row">

            <div class="stat-box">
                <div class="stat-number">
                    {page_count}
                </div>

                <div class="stat-label">
                    Pages
                </div>
            </div>


            <div class="stat-box">
                <div class="stat-number">
                    {len(text):,}
                </div>

                <div class="stat-label">
                    Characters
                </div>
            </div>


            <div class="stat-box">
                <div class="stat-number">
                    {len(chunks)}
                </div>

                <div class="stat-label">
                    Knowledge Chunks
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # EMBEDDING MODEL
    # ========================================================

    with st.spinner(
        "🧠 ACTIVATING DOCUMENT INTELLIGENCE..."
    ):

        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


    st.success(
        "🧠 INTELLIGENCE SYSTEM ONLINE"
    )


    # ========================================================
    # CREATE EMBEDDINGS
    # ========================================================

    with st.spinner(
        "⚡ CONVERTING DOCUMENT INTO KNOWLEDGE VECTORS..."
    ):

        embeddings = embedding_model.encode(
            chunks
        )


    st.success(
        "⚡ KNOWLEDGE VECTORS CREATED"
    )


    # ========================================================
    # CHROMADB
    # ========================================================

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="documents"
    )


    # ========================================================
    # IDS
    # ========================================================

    ids = []

    for i in range(len(chunks)):

        ids.append(
            "chunk_" + str(i)
        )


    # ========================================================
    # REMOVE OLD DATA
    # ========================================================

    try:

        old_data = collection.get()

        if old_data["ids"]:

            collection.delete(
                ids=old_data["ids"]
            )

    except Exception:

        pass


    # ========================================================
    # STORE DATA
    # ========================================================

    collection.add(

        ids=ids,

        documents=chunks,

        embeddings=embeddings.tolist()

    )


    st.success(
        "💾 KNOWLEDGE STORED IN CHROMADB"
    )


    # ========================================================
    # QUESTION SECTION
    # ========================================================

    st.markdown("""
    <div class="comic-divider"></div>

    <div class="section-heading">
    <span>02</span>
    ENTER THE BATTLE
    </div>

    <div class="question-bubble">
    WHAT DO YOU WANT TO KNOW?
    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="question-panel">',
        unsafe_allow_html=True
    )


    question = st.text_input(
        "Ask your document anything",
        placeholder="Example: What is the main topic of this document?"
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH + ANSWER
    # ========================================================

    if question:

        # ====================================================
        # SEARCH
        # ====================================================

        with st.spinner(
            "🔎 SEARCHING THE KNOWLEDGE UNIVERSE..."
        ):

            question_embedding = (
                embedding_model.encode(
                    [question]
                )
            )


            results = collection.query(

                query_embeddings=
                question_embedding.tolist(),

                n_results=len(chunks)

            )


            relevant_chunks = (
                results["documents"][0]
            )


            context = "\n\n".join(
                relevant_chunks
            )


        # ====================================================
        # RETRIEVED CONTEXT
        # ====================================================

        with st.expander(
            "🔍 OPEN DOCUMENT INTELLIGENCE"
        ):

            st.write(context)


        # ====================================================
        # PROMPT
        # ====================================================

        prompt = f"""

You are a helpful document assistant.

Answer the user's question using only the
information available in the document context.

If the user asks for a summary, overview, or
brief description, summarize the important
information from the document context.

If the answer cannot be found in the document,
say:

"I could not find the answer in the document."

Do not make up information.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:

"""


        # ====================================================
        # OLLAMA
        # ====================================================

        with st.spinner(
            "🤖 YOUR AI HERO IS PREPARING THE ANSWER..."
        ):

            response = ollama.chat(

                model="llama3.2",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )


        # ====================================================
        # ANSWER
        # ====================================================

        answer = response[
            "message"
        ][
            "content"
        ]


        safe_answer = html.escape(
            answer
        )


        # ====================================================
        # ANSWER PANEL
        # ====================================================

        st.markdown("""
        <div class="comic-divider"></div>

        <div class="section-heading">
        <span>03</span>
        HERO RESPONSE
        </div>
        """, unsafe_allow_html=True)


        st.markdown(
            f"""
            <div class="answer-panel">

                <div class="answer-title">
                    ⚡ MISSION ANSWER
                </div>

                <div class="answer-text">
                    {safe_answer}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <strong>MARVEL DOCUMENT ADVENTURE</strong>

    <br><br>

    RAG • CHROMADB • SENTENCE TRANSFORMERS • OLLAMA

    <br>

    YOUR DOCUMENT. YOUR QUESTIONS. YOUR AI.

</div>
""", unsafe_allow_html=True)