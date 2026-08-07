from langchain_tavily import TavilySearch

# Inisialisasi tool dengan parameter yang dioptimalkan
search_general = TavilySearch(
    max_results=5,             # Batasi jumlah hasil untuk menghemat token LLM
    topic="general",           # Bisa juga "news" atau "finance"
    search_depth="basic",      # Gunakan "advanced" hanya jika butuh riset mendalam
    include_answer=True,       # Mengambil ringkasan jawaban cepat dari Tavily
    include_raw_content=False  # PENTING: Set False di production (lihat penjelasan di bawah)
)

search_tech = TavilySearch(
    max_results=5,
    topic="technology",
    search_depth="basic",
    include_answer=True,
    include_raw_content=False
)

search_economy = TavilySearch(
    max_results=5,
    topic="economy",
    search_depth="basic",
    include_answer=True,
    include_raw_content=False
)