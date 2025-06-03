from rapidfuzz import fuzz

class SimilarityRecommender:
    """
    콘텐츠 간 유사도를 다중 필드(title, overview, tagline 등) 기반으로 계산하고,
    가장 유사한 콘텐츠를 추천하는 클래스.
    """

    def __init__(self, content_list):
        self.content_list = content_list
        if not content_list:
            raise ValueError("콘텐츠 리스트가 비어 있습니다.")

    def compute_similarity(self, a, b, weights):
        """
        두 콘텐츠 간 가중 평균 유사도 점수를 계산.
        존재하지 않는 필드는 무시되며, 정상 필드만 기준으로 가중합 계산.
        """
        score = 0.0
        total_weight = 0.0

        for key in weights:
            a_val = a.get(key, "").strip()
            b_val = b.get(key, "").strip()

            if a_val and b_val:
                sim = fuzz.token_sort_ratio(a_val, b_val)
                score += sim * weights[key]
                total_weight += weights[key]

        return score / total_weight if total_weight > 0 else 0

    def get_similar(self, content_id, top_k=5, weights=None):
        """
        특정 콘텐츠 ID에 대해 유사 콘텐츠를 top_k개 반환.
        유사도가 낮아도 무조건 top_k개를 반환함.
        """
        if weights is None:
            weights = {
                "title": 0.4,
                "overview": 0.5,
                "tagline": 0.1
            }

        try:
            target = next(c for c in self.content_list if c["id"] == content_id)
        except StopIteration:
            return []

        scored = [
            (c, self.compute_similarity(target, c, weights))
            for c in self.content_list if c["id"] != content_id
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        return [c for c, _ in scored[:top_k]]
