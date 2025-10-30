from rag_system_simple import GymRAGSystem

def test_search(query):
    print(f"\nTesting query: {query}")
    print("-" * 50)
    results = rag.search(query, n_results=3)
    for r in results:
        print(f"Title: {r['metadata']['title']}")
        print(f"Bodypart: {r['metadata']['bodypart']}")
        print(f"Equipment: {r['metadata']['equipment']}")
        print()

# Initialize RAG system
rag = GymRAGSystem("data/megaGymDataset.csv")
rag.initialize_vector_store()

# Test specific queries with more back exercise variations
test_search("how to do back exercises with dumbbells")
test_search("chest workout with dumbbell")
test_search("lats exercises with dumbbells")
test_search("lower back workout dumbbell")