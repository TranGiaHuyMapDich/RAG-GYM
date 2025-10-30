"""
RAG System for Gym Assistant (Simplified Version - No ChromaDB)
Hệ thống RAG cho trợ lý gym thông minh (Phiên bản đơn giản)
"""

import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import pickle
import os


class GymRAGSystem:
    def __init__(self, csv_path: str):
        """Khởi tạo hệ thống RAG"""
        self.csv_path = csv_path
        self.df = None
        self.embeddings_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.embeddings = None
        self.documents = None
        self.embeddings_cache = "embeddings_cache.pkl"
        
    def load_data(self):
        """Đọc dữ liệu từ CSV"""
        print("Đang đọc dữ liệu từ CSV...")
        self.df = pd.read_csv(self.csv_path)
        self.df = self.df.fillna('')  # Thay thế NaN bằng string rỗng
        # Tạo các cột normalized để lọc ổn định hơn (lowercase, trim)
        for col in ['BodyPart', 'Equipment', 'Level', 'Type', 'Title', 'Desc']:
            norm_col = f"{col}_norm"
            self.df[norm_col] = self.df[col].astype(str).str.strip().str.lower()
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
                # Normalized metadata (lowercase) giúp filter nhất quán nếu cần
                'bodypart_norm': str(row.get('BodyPart', '')).strip().lower(),
                'equipment_norm': str(row.get('Equipment', '')).strip().lower(),
                'level_norm': str(row.get('Level', '')).strip().lower(),
            }
            
            documents.append({
                'text': doc_text,
                'metadata': metadata,
                'id': str(row['id'])
            })
        
        return documents
    
    def initialize_vector_store(self, force_recreate: bool = False):
        """Khởi tạo vector store"""
        
        # Load dữ liệu nếu chưa có
        if self.df is None:
            self.load_data()
        
        # Kiểm tra cache
        if os.path.exists(self.embeddings_cache) and not force_recreate:
            print("Đang load embeddings từ cache...")
            with open(self.embeddings_cache, 'rb') as f:
                cache_data = pickle.load(f)
                self.embeddings = cache_data['embeddings']
                self.documents = cache_data['documents']
            # recreate normalized embeddings for fast dot-product cosine
            try:
                arr = np.array(self.embeddings)
                norms = np.linalg.norm(arr, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                self.embeddings_norm = (arr / norms).astype(float)
            except Exception:
                # fallback
                self.embeddings_norm = np.array(self.embeddings)

            # build bodypart index (normalized tokens)
            self.bodypart_index = {}
            for idx, doc in enumerate(self.documents):
                bp = doc['metadata'].get('bodypart_norm') or doc['metadata'].get('bodypart', '').strip().lower()
                if not bp:
                    continue
                for token in re.split(r"[,;/\\|]\\s*|\\s*;\\s*", bp):
                    token = token.strip()
                    if not token:
                        continue
                    self.bodypart_index.setdefault(token, []).append(idx)

            # build equipment index as well
            self.equipment_index = {}
            for idx, doc in enumerate(self.documents):
                eq = doc['metadata'].get('equipment_norm') or doc['metadata'].get('equipment', '').strip().lower()
                if not eq:
                    continue
                for token in re.split(r"[,;/\\|]\\s*|\\s+", eq):
                    token = token.strip()
                    if not token:
                        continue
                    self.equipment_index.setdefault(token, []).append(idx)

            print("✅ Đã load embeddings từ cache!")
            return
        
        # Tạo documents
        self.documents = self.create_documents()
        print(f"Đang tạo embeddings cho {len(self.documents)} documents...")
        print("(Lần đầu chạy sẽ tải model ~500MB, mất 2-5 phút)")
        
        # Tạo embeddings
        texts = [doc['text'] for doc in self.documents]
        self.embeddings = self.embeddings_model.encode(texts, show_progress_bar=True)

        # Chuẩn hóa embeddings thành unit vectors để tính cosine nhanh hơn
        try:
            arr = np.array(self.embeddings)
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.embeddings_norm = (arr / norms).astype(float)
        except Exception:
            self.embeddings_norm = np.array(self.embeddings)

        # Tạo index nhanh theo nhóm cơ (normalized)
        self.bodypart_index = {}
        for idx, doc in enumerate(self.documents):
            bp = doc['metadata'].get('bodypart_norm') or doc['metadata'].get('bodypart', '').strip().lower()
            if not bp:
                continue
            for token in re.split(r"[,;/\\|]\\s*|\\s*;\\s*", bp):
                token = token.strip()
                if not token:
                    continue
                self.bodypart_index.setdefault(token, []).append(idx)

        # Tạo index cho equipment để có thể lọc nhanh theo thiết bị
        self.equipment_index = {}
        for idx, doc in enumerate(self.documents):
            eq = doc['metadata'].get('equipment_norm') or doc['metadata'].get('equipment', '').strip().lower()
            if not eq:
                continue
            for token in re.split(r"[,;/\\|]\\s*|\\s+", eq):
                token = token.strip()
                if not token:
                    continue
                self.equipment_index.setdefault(token, []).append(idx)

        # Lưu cache (embeddings thô + documents). emb_norm và index sẽ được tái tạo khi load.
        print("Đang lưu embeddings vào cache...")
        with open(self.embeddings_cache, 'wb') as f:
            pickle.dump({
                'embeddings': self.embeddings,
                'documents': self.documents
            }, f)

        print("✅ Hoàn thành khởi tạo vector store!")
    
    def search(self, query: str, n_results: int = 5, filters: Dict = None) -> List[Dict]:
        """Tìm kiếm các bài tập liên quan"""
        
        # Tạo embedding cho query và chuẩn hóa
        query_embedding = self.embeddings_model.encode([query])[0]
        q_arr = np.array(query_embedding, dtype=float)
        q_norm = q_arr / (np.linalg.norm(q_arr) + 1e-12)

        # Candidate indices (start with all)
        total_n = len(self.documents)
        candidate_indices = set(range(total_n))

        # Strict bodypart and equipment detection with common word boundaries
        query_norm_text = " " + str(query).strip().lower() + " "  # add spaces for word boundary checking
        
        # Common English words to ignore
        ignore_words = {'with', 'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of'}
        query_words = set(w for w in query_norm_text.split() if w not in ignore_words)
        
        # Map common variations to standard terms
        # Initialize bodypart tokens list
        bp_tokens_found = []
        
        if hasattr(self, 'bodypart_index'):
            # Special case patterns for back to avoid false matches
            back_patterns = [
                r'\b(back)\b(?!\s+to|\s+and|\s+of|\s+in|\s+on|\s+at)',  # 'back' not followed by prepositions
                r'\b(lats|latissimus)\b',
                r'\b(upper|lower|mid)\s+back\b'
            ]
            
            # Handle back exercises first (special case)
            back_categories = {'lats', 'lower back', 'middle back'}
            back_variations = {
                'lats': ['lats', 'latissimus', 'lat pulldown', 'pull-up', 'pullup'],
                'lower back': ['lower back', 'deadlift', 'good morning'],
                'middle back': ['middle back', 'rows', 'row exercise']
            }
            
            # Check for specific back part first
            found_specific = False
            for category, terms in back_variations.items():
                if any(f" {term} " in query_norm_text for term in terms):
                    if category in self.bodypart_index:
                        bp_tokens_found.append(category)
                        found_specific = True
            
            # If no specific back part found but "back" is mentioned generically
            if not found_specific and any(re.search(pattern, query_norm_text) for pattern in back_patterns):
                # Add all back categories to search across all back exercises
                for category in back_categories:
                    if category in self.bodypart_index:
                        bp_tokens_found.append(category)
            
            if bp_tokens_found:
                self.strict_back_search = True  # Force strict matching for back
            
            # Standard bodypart variations
            bodypart_variations = {
                'chest': ['chest', 'pecs', 'pectorals'],
                'shoulders': ['shoulder', 'shoulders', 'deltoids'],
                'biceps': ['bicep', 'biceps', 'arm'],
                'triceps': ['tricep', 'triceps'],
                'quadriceps': ['leg', 'legs', 'quadriceps'],
                'hamstrings': ['hamstring', 'hamstrings'],
                'abdominals': ['ab', 'abs', 'abdominals', 'core']
            }
            
            # Check each variation against the index
            for index_term, variations in bodypart_variations.items():
                if index_term in self.bodypart_index:
                    if any(f" {var} " in query_norm_text for var in variations):
                        bp_tokens_found.append(index_term)
        
        bp_tokens_found = []
        if hasattr(self, 'bodypart_index'):
            # First check exact matches in index
            for token in self.bodypart_index.keys():
                if token and f" {token} " in query_norm_text:
                    bp_tokens_found.append(token)
            
            # If no exact matches, try variations
            if not bp_tokens_found:
                for std_term, variations in bodypart_variations.items():
                    if any(f" {var} " in query_norm_text for var in variations):
                        if std_term in self.bodypart_index:
                            bp_tokens_found.append(std_term)

        # Strict equipment detection with word boundaries and variations
        equipment_variations = {
            'dumbbell': ['dumbbell', 'dumbbells', 'db'],
            'barbell': ['barbell', 'barbells', 'bb'],
            'kettlebell': ['kettlebell', 'kettlebells', 'kb'],
            'bodyweight': ['bodyweight', 'body weight', 'no equipment'],
            'resistance band': ['resistance band', 'bands', 'resistance bands'],
            'machine': ['machine', 'machines', 'gym machine']
        }
        
        equip_tokens_found = []
        if hasattr(self, 'equipment_index'):
            # First check exact matches in index
            for token in self.equipment_index.keys():
                if token and f" {token} " in query_norm_text:
                    equip_tokens_found.append(token)
            
            # If no exact matches, try variations
            if not equip_tokens_found:
                for std_term, variations in equipment_variations.items():
                    if any(f" {var} " in query_norm_text for var in variations):
                        if std_term in self.equipment_index:
                            equip_tokens_found.append(std_term)

        if bp_tokens_found:
            # union indices for found tokens
            bp_indices = set()
            for t in bp_tokens_found:
                bp_indices.update(self.bodypart_index.get(t, []))
            # If equipment is also requested in the query, REQUIRE the intersection
            if equip_tokens_found:
                equip_indices = set()
                for t in equip_tokens_found:
                    equip_indices.update(self.equipment_index.get(t, []))
                # Strict intersection - MUST match both bodypart AND equipment
                inter = bp_indices & equip_indices
                if inter:
                    candidate_indices = inter
                    # Extremely strict matching - must be primary bodypart
                    final_indices = set()
                    for idx in inter:
                        doc = self.documents[idx]
                        bodypart_norm = doc['metadata'].get('bodypart_norm', '').lower()
                        equipment_norm = doc['metadata'].get('equipment_norm', '').lower()
                        
                        # Special handling for back exercises to be extremely strict
                        if hasattr(self, 'strict_back_search') and self.strict_back_search:
                            # For back exercises, check the first two muscle groups to catch exercises
                            # that might list "lats" second after "back" for example
                            primary_muscles = [m.strip() for m in bodypart_norm.split(',')[:2]]
                            bp_match = any(any(bp == muscle for bp in bp_tokens_found) for muscle in primary_muscles)
                            self.strict_back_search = False  # Reset for next search
                        else:
                            # For other bodyparts, only match if it's the primary muscle group
                            primary_bodypart = bodypart_norm.split(',')[0].strip()
                            bp_match = any(bp == primary_bodypart for bp in bp_tokens_found)
                        
                        # For equipment, any match in the list is fine
                        eq_match = any(eq in equipment_norm for eq in equip_tokens_found)
                        
                        if bp_match and eq_match:
                            final_indices.add(idx)
                    if final_indices:
                        candidate_indices = final_indices
                    else:
                        # If somehow no perfect matches, keep the original intersection
                        candidate_indices = inter
            else:
                # Prefer bodypart-based results (user requested bodypart-centric answers)
                candidate_indices = bp_indices
        elif equip_tokens_found:
            # No bodypart found but equipment mentioned -> restrict to equipment indices
            equip_indices = set()
            for t in equip_tokens_found:
                equip_indices.update(self.equipment_index.get(t, []))
            candidate_indices = equip_indices
        
        if filters:
            # Normalize filter values similar to get_exercise_by_filters behaviour
            f_body = filters.get('bodypart') or filters.get('body') or filters.get('body_part')
            f_equip = filters.get('equipment')
            f_level = filters.get('level')

            # helper to treat empty/all values
            def _normalize_input(v: str):
                if not v:
                    return None
                vv = str(v).strip().lower()
                if vv in ['tất cả', 'tat ca', 'tấtca', 'all', 'tất_cả']:
                    return None
                return vv

            f_body = _normalize_input(f_body)
            f_equip = _normalize_input(f_equip)
            f_level = _normalize_input(f_level)

            # Build valid indices by checking normalized metadata
            # Build valid indices by checking normalized metadata, but only within current candidate_indices
            valid_indices = []
            for idx in list(candidate_indices):
                doc = self.documents[idx]
                metadata = doc['metadata']

                # compare using normalized text where possible
                body_norm = metadata.get('bodypart', '').strip().lower()
                equip_norm = metadata.get('equipment', '').strip().lower()
                level_norm = metadata.get('level', '').strip().lower()

                if f_level and f_level not in level_norm:
                    continue

                if f_body and f_body not in body_norm:
                    continue

                if f_equip and f_equip not in equip_norm:
                    continue

                valid_indices.append(idx)

            # If filters were applied and reduced candidates, use them
            candidate_indices = set(valid_indices)
        
        # Compute similarities only for candidate indices (faster if subset)
        if not hasattr(self, 'embeddings_norm'):
            # fallback to original embeddings and sklearn if normalized not available
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            cand_list = list(candidate_indices)
            sims = [(idx, float(similarities[idx])) for idx in cand_list]
        else:
            # vectorized dot product (embeddings_norm @ q_norm) -> cosine similarities
            sims_all = np.dot(self.embeddings_norm, q_norm)
            cand_list = list(candidate_indices)
            sims = [(idx, float(sims_all[idx])) for idx in cand_list]

        # sort by similarity and take top
        sims.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in sims[:n_results]]
        
        # Format kết quả
        formatted_results = []
        # format results using computed similarity values
        sims_dict = {idx: score for idx, score in sims}
        for idx in top_indices:
            sim = sims_dict.get(idx, 0.0)
            formatted_results.append({
                'text': self.documents[idx]['text'],
                'metadata': self.documents[idx]['metadata'],
                'distance': float(1.0 - sim)
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
            day_splits = [
                ['Chest', 'Back', 'Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves'],
                ['Full Body', 'Abdominals']
            ]
        elif days_per_week == 4:
            day_splits = [
                ['Chest', 'Shoulders', 'Triceps'],
                ['Quadriceps', 'Hamstrings', 'Calves'],
                ['Back', 'Biceps', 'Abdominals'],
                ['Glutes', 'Full Body']
            ]
        elif days_per_week == 5:
            day_splits = [
                ['Chest', 'Triceps'],
                ['Back', 'Biceps'],
                ['Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings'],
                ['Glutes', 'Calves', 'Abdominals']
            ]
        elif days_per_week == 6:
            day_splits = [
                ['Chest', 'Shoulders', 'Triceps'],
                ['Back', 'Biceps'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves'],
                ['Chest', 'Shoulders', 'Triceps', 'Abdominals'],
                ['Back', 'Biceps', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes', 'Calves']
            ]
        else:
            day_splits = [
                ['Chest', 'Back', 'Shoulders', 'Abdominals'],
                ['Quadriceps', 'Hamstrings', 'Glutes'],
                ['Full Body', 'Abdominals']
            ]
        
        # Tìm bài tập cho từng ngày
        for day_num, muscle_groups in enumerate(day_splits, 1):
            day_exercises = []
            
            for muscle_group in muscle_groups:
                filters = {
                    'level': fitness_level,
                }
                
                if muscle_group != 'Full Body':
                    filters['bodypart'] = muscle_group
                
                if available_equipment:
                    for equipment in available_equipment:
                        search_query = f"Bài tập {muscle_group} với {equipment}"
                        results = self.search(search_query, n_results=2, filters=filters)
                        day_exercises.extend(results[:1])
                else:
                    search_query = f"Bài tập {muscle_group}"
                    results = self.search(search_query, n_results=3, filters=filters)
                    day_exercises.extend(results[:2])
            
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
                'exercises': unique_exercises[:6]
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

        # Normalize and interpret common "all" values
        def _normalize_input(v: str):
            if not v:
                return None
            vv = str(v).strip().lower()
            if vv in ['tất cả', 'tat ca', 'tấtca', 'all', 'tất_cả']:
                return None
            return vv

        body_in = _normalize_input(body_part)
        equip_in = _normalize_input(equipment)
        level_in = _normalize_input(level)

        # simple Vietnamese->dataset mappings (extendable)
        body_map = {
            'ngực': 'chest',
            'lưng': 'back',
            'vai': 'shoulders',
            'bụng': 'abdominals',
            'mông': 'glutes',
            'đùi trước': 'quadriceps',
            'đùi sau': 'hamstrings',
            'bắp chân': 'calves',
            'tay trước': 'biceps',
            'tay sau': 'triceps',
            'toàn thân': 'full body',
        }

        level_map = {
            'người mới': 'beginner',
            'mới': 'beginner',
            'trung bình': 'intermediate',
            'nâng cao': 'expert'
        }

        if body_in and body_in in body_map:
            body_in = body_map[body_in]

        if level_in and level_in in level_map:
            level_in = level_map[level_in]

        # Use normalized dataframe columns for stable matching
        if body_in:
            filtered_df = filtered_df[filtered_df['BodyPart_norm'].str.contains(re.escape(body_in), na=False)]

        if equip_in:
            # allow multiple tokens (e.g., 'dumbbell, bodyweight')
            tokens = re.split(r"[,;/\\|]\\s*|\\s+", equip_in)
            mask = pd.Series(False, index=filtered_df.index)
            for t in tokens:
                if not t:
                    continue
                mask = mask | filtered_df['Equipment_norm'].str.contains(re.escape(t), na=False)
            filtered_df = filtered_df[mask]

        if level_in:
            filtered_df = filtered_df[filtered_df['Level_norm'].str.contains(re.escape(level_in), na=False)]

        # Sắp xếp theo rating (convert to numeric if mixed types)
        filtered_df['Rating_numeric'] = pd.to_numeric(filtered_df['Rating'], errors='coerce')
        filtered_df = filtered_df.sort_values(by='Rating_numeric', ascending=False, na_position='last')
        
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
    print("Khởi tạo Gym RAG System (Simplified)...")
    rag = GymRAGSystem("data/megaGymDataset.csv")
    
    # Khởi tạo vector store
    rag.initialize_vector_store(force_recreate=False)
    
    # Test search
    print("\n=== Test Search ===")
    results = rag.search("bài tập ngực cho người mới bắt đầu", n_results=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['metadata']['title']}")
        print(f"   Level: {result['metadata']['level']}")
        print(f"   Equipment: {result['metadata']['equipment']}")
    
    print("\n✅ System ready!")


