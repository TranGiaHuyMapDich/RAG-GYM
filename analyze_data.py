from rag_system_simple import GymRAGSystem

# Initialize RAG system
rag = GymRAGSystem("data/megaGymDataset.csv")
rag.initialize_vector_store()

# Get all exercises to analyze the data structure
print("\nAnalyzing dataset structure:")
df = rag.df

# Show unique bodypart values
print("\nUnique bodyparts in dataset:")
print(sorted(df['BodyPart_norm'].unique()))

# Show a few back exercises
print("\nSample back exercises:")
back_exercises = df[df['BodyPart_norm'].str.contains('back|lats', na=False)]
print(back_exercises[['Title', 'BodyPart', 'Equipment']].head())