from rapidfuzz import fuzz

class SimilarityRecommender:
    """
    TMDB 기반 콘텐츠 간 유사도를 여러 필드(title, overview, tagline 등)로 계산하고,
    무조건 top_k개의 콘텐츠를 추천해주는 클래스.
    """

    def __init__(self, content_list):
        self.content_list = content_list
        if not self.content_list:
            raise ValueError("추천용 콘텐츠 리스트가 비어 있습니다.")

    def compute_similarity(self, a, b, weights):
        """
        두 콘텐츠 간 유사도를 가중 평균 방식으로 계산.
        존재하지 않는 필드는 무시되고, 있는 필드만으로 유사도 계산함.
        """
        score = 0.0
        total_weight = 0.0

        for key, weight in weights.items():
            a_val = a.get(key, "").strip()
            b_val = b.get(key, "").strip()
            if a_val and b_val:
                sim = fuzz.token_sort_ratio(a_val, b_val)
                score += sim * weight
                total_weight += weight

        return score / total_weight if total_weight > 0 else 0

    def get_similar(self, content_id, top_k=5, weights=None):
        """
        주어진 content_id를 기준으로 가장 유사한 콘텐츠 top_k개를 반환.
        유사도와 관계없이 top_k개를 무조건 반환하도록 fallback 처리 포함.
        """
        if weights is None:
            weights = {
                "title": 0.4,
                "overview": 0.5,
                "tagline": 0.1
            }

        # 기준 콘텐츠 찾기
        try:
            target = next(c for c in self.content_list if c["id"] == content_id)
        except StopIteration:
            # 못 찾았으면 그냥 앞에서 top_k 추천
            return self.content_list[:top_k]

        # 비교 가능한 다른 콘텐츠들과 유사도 점수 계산
        scored = []
        for c in self.content_list:
            if c["id"] == content_id:
                continue
            score = self.compute_similarity(target, c, weights)
            scored.append((c, score))

        # 그래도 결과가 비어 있을 경우 fallback
        if not scored:
            return self.content_list[:top_k]

        # 점수 기준 정렬 후 top_k 반환
        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]
