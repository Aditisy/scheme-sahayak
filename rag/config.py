from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INDEX_DIR = ROOT / "index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SIM_THRESHOLD = 0.30
BM25_MIN_SCORE = 1.0
TOP_DENSE = 10
TOP_BM25 = 10
TOP_K = 5
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
SCHEME_NAMES = {
    "2022050996.pdf": "PM-JAY",
    "2022051036.pdf": "PM-JAY",
    "AMH.pdf": "PM-JAY",
    "ayush.pdf": "PM-JAY",
    "gr6_dscw_sje_02092022.pdf": "Post-Matric Scholarship (SC)",
    "Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf": "Post-Matric Scholarship (SC)",
    "physicalverificationofbeneficiariesunderPM-KISAN.pdf": "PM-KISAN",
    "PMKisanSamanNidhi.pdf": "PM-KISAN",
    "RevisedPM-KISANOperationalGuidelines(English).pdf": "PM-KISAN",
}
