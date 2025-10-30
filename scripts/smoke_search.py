import time
from rag_system_simple import GymRAGSystem

r = GymRAGSystem('data/megaGymDataset.csv')
r.load_data()
start = time.time()
r.initialize_vector_store(force_recreate=False)
print('init took', time.time()-start)

queries = [
    'bài tập ngực cho người mới bắt đầu',
    'back exercises',
    'shoulder press with dumbbell',
    'bài tập mông',
    'how to train biceps at home'
]

for q in queries:
    t0 = time.time()
    res = r.search(q, n_results=5)
    t1 = time.time()
    print(f"Query: {q} -> {len(res)} results in {t1-t0:.4f}s")
    for i, e in enumerate(res, 1):
        print(f"  {i}. {e['metadata'].get('title','')[:60]} | {e['metadata'].get('bodypart','')}")
    print('---')
