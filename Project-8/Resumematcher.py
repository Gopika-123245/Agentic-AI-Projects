from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = Flask(__name__)

# Fast Model
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

def calculate_scores(jd, resume):

    # Semantic Search Score
    docs = [jd, resume]

    embeddings = model.encode(
        docs,
        convert_to_numpy=True
    )

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    query = model.encode(
        [jd],
        convert_to_numpy=True
    )

    D, I = index.search(query, k=2)

    semantic_score = max(0, 100 - D[0][1])

    # Keyword Match Score
    jd_words = set(jd.lower().split())

    resume_words = set(resume.lower().split())

    matched = jd_words.intersection(
        resume_words
    )

    keyword_score = (
        len(matched) / len(jd_words)
    ) * 100

    # Final ATS Score
    ats_score = (
        semantic_score * 0.7 +
        keyword_score * 0.3
    )

    return (
        round(semantic_score, 2),
        round(keyword_score, 2),
        round(ats_score, 2),
        matched
    )


@app.route('/', methods=['GET', 'POST'])
def home():

    semantic_score = None
    keyword_score = None
    ats_score = None
    matched_keywords = []

    if request.method == 'POST':

        jd = request.form['job_desc']

        resume = request.form['resume_text']

        (
            semantic_score,
            keyword_score,
            ats_score,
            matched_keywords

        ) = calculate_scores(jd, resume)

    return render_template(
        'index.html',
        semantic_score=semantic_score,
        keyword_score=keyword_score,
        ats_score=ats_score,
        matched_keywords=matched_keywords
    )


if __name__ == '__main__':
    app.run(debug=True)
