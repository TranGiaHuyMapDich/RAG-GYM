"""
RAG System for Gym Assistant
Hệ thống RAG cho trợ lý gym thông minh
"""

import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import os
import json


class GymRAGSystem:
    def __init__(self, csv_path: str):
        """Khởi tạo hệ thống RAG"""
        self.csv_path = csv_path
        self.df = None
        self.embeddings_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        # Khởi tạo ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory="./chroma_db"
        ))
        
        self.collection_name = "gym_exercises"
        self.collection = None
        
    def load_data(self):
        """Đọc dữ liệu từ CSV"""
        print("Đang đọc dữ liệu từ CSV...")
        self.df = pd.read_csv(self.csv_path)
        self.df = self.df.fillna('')  # Thay thế NaN bằng string rỗng
        print(f"Đã tải {len(self.df)} bài tập")
        return self.df
    
    def create_documents(self) -> List[Dict]:
        """Tạo documents từ DataFrame"""
        documents = []
        
        for idx, row in self.df.iterrows():
            # Tạo text content đầy đủ cho mỗi bài tập
            doc_text = f"""
Tên bài tập: {row['Title']}
Mô tả: {row['Desc']}
Loại: {row['Type']}
Nhóm cơ: {row['BodyPart']}
Thiết bị: {row['Equipment']}
Cấp độ: {row['Level']}
Đánh giá: {row['Rating']} - {row['RatingDesc']}
"""
            
            # Metadata
            metadata = {
                'id': str(row['id']),
                'title': str(row['Title']),
                'type': str(row['Type']),
                'bodypart': str(row['BodyPart']),
                'equipment': str(row['Equipment']),
                'level': str(row['Level']),
                'rating': str(row['Rating']),
            }
            
            documents.append({
                'text': doc_text,
                'metadata': metadata,
                'id': str(row['id'])
            })
        
        return documents
    
    def initialize_vector_store(self, force_recreate: bool = False):
        """Khởi tạo vector store với ChromaDB"""
        
        # Xóa collection cũ nếu cần
        if force_recreate:
            try:
                self.chroma_client.delete_collection(name=self.collection_name)
                print("Đã xóa collection cũ")
            except:
                pass
        
        # Tạo hoặc lấy collection
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            print("Đã tìm thấy collection có sẵn")
            return
        except:
            print("Tạo collection mới...")
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Gym exercises database"}
            )
        
        # Load dữ liệu nếu chưa có
        if self.df is None:
            self.load_data()
        
        # Tạo documents
        documents = self.create_documents()
        print(f"Đang tạo embeddings cho {len(documents)} documents...")
        
        # Thêm documents vào ChromaDB theo batch
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            
            texts = [doc['text'] for doc in batch]
            metadatas = [doc['metadata'] for doc in batch]
            ids = [doc['id'] for doc in batch]
            
            # Tạo embeddings
            embeddings = self.embeddings_model.encode(texts).tolist()
            
            # Thêm vào collection
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Đã xử lý {min(i+batch_size, len(documents))}/{len(documents)} documents")
        
        print("Hoàn thành khởi tạo vector store!")
    
    def search(self, query: str, n_results: int = 5, filters: Dict = None) -> List[Dict]:
        """Tìm kiếm các bài tập liên quan"""
        
        # Tạo embedding cho query
        query_embedding = self.embeddings_model.encode([query])[0].tolist()
        
        # Chuẩn bị where clause nếu có filters
        where_clause = None
        if filters:
            where_clause = {}
            if 'level' in filters and filters['level']:
                where_clause['level'] = filters['level']
            if 'bodypart' in filters and filters['bodypart']:
                where_clause['bodypart'] = filters['bodypart']
            if 'equipment' in filters and filters['equipment']:
                where_clause['equipment'] = filters['equipment']
        
        # Tìm kiếm
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_clause if where_clause else None
        )
        
        # Format kết quả
        formatted_results = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def generate_workout_plan(self, 
                             body_type: str, 
                             fitness_level: str,
                             goals: str,
                             available_equipment: List[str] = None,
                             days_per_week: int = 3) -> Dict:
        """
        Tạo kế hoạch tập luyện cá nhân hóa
        
        Args:
            body_type: Loại cơ thể (ectomorph/mesomorph/endomorph)
            fitness_level: Trình độ (Beginner/Intermediate/Advanced)
            goals: Mục tiêu (muscle gain/weight loss/endurance/strength)
            available_equipment: Thiết bị có sẵn
            days_per_week: Số ngày tập/tuần
        """
        
        # Mapping body type và goals
        body_type_mapping = {
            'ectomorph': 'Người gầy, khó tăng cân - nên tập trọng lượng, ít cardio',
            'mesomorph': 'Người cơ bắp, dễ tăng cơ - cân bằng giữa sức mạnh và cardio',
            'endomorph': 'Người dễ tăng cân - nên kết hợp cardio và tập sức mạnh'
        }
        
        goals_mapping = {
            'muscle_gain': 'tăng cơ',
            'weight_loss': 'giảm cân',
            'endurance': 'tăng sức bền',
            'strength': 'tăng sức mạnh',
            'general_fitness': 'tăng cường thể lực tổng quát'
        }
        
        # Tạo query dựa trên thông tin người dùng
        base_query = f"Bài tập cho người {body_type_mapping.get(body_type, body_type)}, mục tiêu {goals_mapping.get(goals, goals)}, cấp độ {fitness_level}"
        
        # Lấy danh sách các nhóm cơ chính
        major_muscle_groups = [
            'Chest', 'Back', 'Shoulders', 'Quadriceps', 'Hamstrings',
            'Abdominals', 'Biceps', 'Triceps', 'Glutes', 'Calves'
        ]
        
        workout_plan = {
            'body_type': body_type,
            'fitness_level': fitness_level,
            'goals': goals,
            'days_per_week': days_per_week,
            'recommendations': body_type_mapping.get(body_type, ''),
            'weekly_plan': []
        }
        
        # Tạo lịch tập cho từng ngày
        if days_per_week == 3:
            # Full body 3 ngày/tuần
            day_splits = [
                ['Chest', 'Back', 'Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves'],
                ['Full Body', 'Abdominals']
            ]
        elif days_per_week == 4:
            # Upper/Lower split
            day_splits = [
                ['Chest', 'Shoulders', 'Triceps'],
                ['Quadriceps', 'Hamstrings', 'Calves'],
                ['Back', 'Biceps', 'Abdominals'],
                ['Glutes', 'Full Body']
            ]
        elif days_per_week == 5:
            # Bro split
            day_splits = [
                ['Chest', 'Triceps'],
                ['Back', 'Biceps'],
                ['Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings'],
                ['Glutes', 'Calves', 'Abdominals']
            ]
        elif days_per_week == 6:
            # Push/Pull/Legs split x2
            day_splits = [
                ['Chest', 'Shoulders', 'Triceps'],
                ['Back', 'Biceps'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves'],
                ['Chest', 'Shoulders', 'Triceps', 'Abdominals'],
                ['Back', 'Biceps', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves']
            ]
        else:  # Mặc định 3 ngày
            day_splits = [
                ['Chest', 'Back', 'Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes'],
                ['Full Body', 'Abdominals']
            ]
        
        # Tìm bài tập cho từng ngày
        for day_num, muscle_groups in enumerate(day_splits, 1):
            day_exercises = []
            
            for muscle_group in muscle_groups:
                # Tìm kiếm bài tập cho nhóm cơ này
                filters = {
                    'level': fitness_level,
                }
                
                if muscle_group != 'Full Body':
                    filters['bodypart'] = muscle_group
                
                if available_equipment:
                    # Tìm bài tập với từng thiết bị
                    for equipment in available_equipment:
                        search_query = f"Bài tập {muscle_group} với {equipment}"
                        results = self.search(search_query, n_results=2, filters=filters)
                        day_exercises.extend(results[:1])  # Lấy 1 bài tập tốt nhất
                else:
                    search_query = f"Bài tập {muscle_group}"
                    results = self.search(search_query, n_results=3, filters=filters)
                    day_exercises.extend(results[:2])  # Lấy 2 bài tập tốt nhất
            
            # Loại bỏ trùng lặp
            seen_ids = set()
            unique_exercises = []
            for ex in day_exercises:
                ex_id = ex['metadata']['id']
                if ex_id not in seen_ids:
                    seen_ids.add(ex_id)
                    unique_exercises.append(ex)
            
            workout_plan['weekly_plan'].append({
                'day': day_num,
                'focus': ', '.join(muscle_groups),
                'exercises': unique_exercises[:6]  # Giới hạn 6 bài tập/ngày
            })
        
        return workout_plan
    
    def get_exercise_by_filters(self, 
                                body_part: str = None,
                                equipment: str = None,
                                level: str = None,
                                limit: int = 10) -> List[Dict]:
        """Lọc bài tập theo tiêu chí"""
        
        if self.df is None:
            self.load_data()
        
        filtered_df = self.df.copy()
        
        if body_part:
            filtered_df = filtered_df[filtered_df['BodyPart'].str.contains(body_part, case=False, na=False)]
        
        if equipment:
            filtered_df = filtered_df[filtered_df['Equipment'].str.contains(equipment, case=False, na=False)]
        
        if level:
            filtered_df = filtered_df[filtered_df['Level'].str.contains(level, case=False, na=False)]
        
        # Sắp xếp theo rating
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False, na_position='last')
        
        # Chuyển đổi sang list of dicts
        results = []
        for _, row in filtered_df.head(limit).iterrows():
            results.append({
                'id': str(row['id']),
                'title': str(row['Title']),
                'description': str(row['Desc']),
                'type': str(row['Type']),
                'bodypart': str(row['BodyPart']),
                'equipment': str(row['Equipment']),
                'level': str(row['Level']),
                'rating': str(row['Rating'])
            })
        
        return results
    
    def get_statistics(self) -> Dict:
        """Lấy thống kê về dataset"""
        if self.df is None:
            self.load_data()
        
        stats = {
            'total_exercises': len(self.df),
            'body_parts': self.df['BodyPart'].value_counts().to_dict(),
            'equipment_types': self.df['Equipment'].value_counts().to_dict(),
            'levels': self.df['Level'].value_counts().to_dict(),
            'types': self.df['Type'].value_counts().to_dict(),
        }
        
        return stats


if __name__ == "__main__":
    # Test RAG system
    print("Khởi tạo Gym RAG System...")
    rag = GymRAGSystem("megaGymDataset.csv")
    
    # Khởi tạo vector store
    rag.initialize_vector_store(force_recreate=False)
    
    # Test search
    print("\n=== Test Search ===")
    results = rag.search("bài tập ngực cho người mới bắt đầu", n_results=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['metadata']['title']}")
        print(f"   Level: {result['metadata']['level']}")
        print(f"   Equipment: {result['metadata']['equipment']}")
    
    # Test workout plan
    print("\n=== Test Workout Plan ===")
    plan = rag.generate_workout_plan(
        body_type='mesomorph',
        fitness_level='Intermediate',
        goals='muscle_gain',
        available_equipment=['Barbell', 'Dumbbell'],
        days_per_week=4
    )
    
    print(f"\nKế hoạch tập {plan['days_per_week']} ngày/tuần:")
    for day in plan['weekly_plan']:
        print(f"\nNgày {day['day']} - {day['focus']}:")
        for ex in day['exercises'][:3]:
            print(f"  - {ex['metadata']['title']} ({ex['metadata']['equipment']})")
    
    # Stats
    print("\n=== Statistics ===")
    stats = rag.get_statistics()
    print(f"Tổng số bài tập: {stats['total_exercises']}")
    print(f"Số nhóm cơ: {len(stats['body_parts'])}")
    print(f"Số loại thiết bị: {len(stats['equipment_types'])}")

