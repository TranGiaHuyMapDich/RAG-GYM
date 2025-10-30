from rag_system_simple import GymRAGSystem


def print_sample(results, label):
    print('\n---', label, '->', len(results), 'results')
    for i, r in enumerate(results[:5], 1):
        print(f"{i}. {r['title']} | body: {r['bodypart']} | equip: {r['equipment']} | level: {r['level']}")


def main():
    rag = GymRAGSystem("data/megaGymDataset.csv")
    rag.load_data()

    # 1. 'Tất cả' should return many (treated as no filter)
    res_all = rag.get_exercise_by_filters(body_part='Tất cả', equipment=None, level=None, limit=5)
    print_sample(res_all, "Tất cả (no filter)")

    # 2. Vietnamese body part 'ngực' should map to 'chest'
    res_chest_vi = rag.get_exercise_by_filters(body_part='ngực', equipment=None, level=None, limit=5)
    print_sample(res_chest_vi, "ngực -> chest")

    # 3. English body part 'Chest'
    res_chest_en = rag.get_exercise_by_filters(body_part='Chest', equipment=None, level=None, limit=5)
    print_sample(res_chest_en, "Chest (english)")

    # 4. Equipment filter
    res_dumbbell = rag.get_exercise_by_filters(body_part=None, equipment='Dumbbell', level=None, limit=5)
    print_sample(res_dumbbell, "Equipment: Dumbbell")


if __name__ == '__main__':
    main()
