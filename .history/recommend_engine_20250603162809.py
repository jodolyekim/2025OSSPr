from rapidfuzz import fuzz

class SimilarityRecommender:
    """
    title, overview, tagline, genres 등을 기반으로 콘텐츠 유사도 계산 + 추천
    """

    def __init__(self, content_list):
        self.content_list = content_list
        if not self.content_list:
            raise ValueError("추천용 콘텐츠 리스트가 비어 있습니다.")

    def compute_similarity(self, a, b, weights):
        score = 0.0
        total_weight = 0.0

        for key, weight in weights.items():
            a_val = self._get_field_as_string(a.get(key))
            b_val = self._get_field_as_string(b.get(key))

            if a_val and b_val:
                sim = fuzz.token_sort_ratio(a_val, b_val)
                score += sim * weight
                total_weight += weight

        return score / total_weight if total_weight > 0 else 0

    def _get_field_as_string(self, val):
        """
        val이 리스트(예: genres)일 경우 문자열로 변환.
        """
        if isinstance(val, list):
            return " ".join(str(v) for v in val).strip()
        elif isinstance(val, str):
            return val.strip()
        else:
            return ""

    def get_similar(self, content_id, top_k=5, weights=None):
        if weights is None:
            weights = {
                "title": 0.3,
                "overview": 0.4,
                "tagline": 0.1,
                "genres": 0.2   # 🔥 장르 추가됨
            }

        try:
            target = next(c for c in self.content_list if c["id"] == content_id)
        except StopIteration:
            return self.content_list[:top_k]

        scored = []
        for c in self.content_list:
            if c["id"] == content_id:
                continue
            score = self.compute_similarity(target, c, weights)
            scored.append((c, score))

        if not scored:
            return self.content_list[:top_k]

        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]
