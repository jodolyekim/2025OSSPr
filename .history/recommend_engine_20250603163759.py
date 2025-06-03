from rapidfuzz import fuzz

class SimilarityRecommender:
    def __init__(self, content_list):
        self.content_list = [c for c in content_list if c.get("overview") and len(c["overview"].strip()) >= 10]
        if not self.content_list:
            raise ValueError("유효한 overview를 가진 콘텐츠가 없습니다.")

    def get_similar(self, content_id, top_k=5):
        try:
            target = next(c for c in self.content_list if c["id"] == content_id)
        except StopIteration:
            return []

        target_text = target["overview"]
        scored = [
            (c, fuzz.token_sort_ratio(target_text, c["overview"]))
            for c in self.content_list if c["id"] != content_id
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]