from rapidfuzz import fuzz

class SimilarityRecommender:
    """
    TMDB 콘텐츠 기반 유사 추천기
    - title, overview, tagline, genres 등의 필드를 기준으로
      콘텐츠 간 유사도를 계산하고 가장 비슷한 콘텐츠를 추천함.
    """

    def __init__(self, content_list):
        self.content_list = content_list
        if not self.content_list:
            raise ValueError("추천용 콘텐츠 리스트가 비어 있습니다.")

    def _get_field_as_string(self, val):
        """
        val이 리스트(예: genres)일 경우 문자열로 변환하여 유사도 비교 가능하게 함.
        """
        if isinstance(val, list):
            return " ".join(str(v) for v in val).strip()
        elif isinstance(val, str):
            return val.strip()
        return ""

    def compute_similarity(self, a, b, weights):
        """
        두 콘텐츠(a, b) 간 가중 평균 유사도 점수를 계산함.
        비어 있는 필드는 자동 무시됨.
        """
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

    def get_similar(self, content_id, top_k=5, weights=None):
        """
        기준 콘텐츠 ID를 기준으로 가장 유사한 콘텐츠 top_k개를 추천.
        추천이 불가능한 경우 fallback으로 임의 콘텐츠를 반환.
        """
        if weights is None:
            weights = {
                "title": 0.3,
                "overview": 0.4,
                "tagline": 0.1,
                "genres": 0.2
            }

        try:
            target = next(c for c in self.content_list if c["id"] == content_id)
        except StopIteration:
            print(f"[❌] 콘텐츠 ID {content_id} 가 추천풀에 없음 → fallback 반환")
            return self.content_list[:top_k]

        scored = []
        for c in self.content_list:
            if c["id"] == content_id:
                continue
            score = self.compute_similarity(target, c, weights)
            scored.append((c, score))

        if not scored:
            print(f"[⚠️] 유사도 계산 대상이 없음 → fallback 반환")
            return self.content_list[:top_k]

        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]
