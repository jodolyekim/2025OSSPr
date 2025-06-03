from rapidfuzz import fuzz

class SimilarityRecommender:
    """
    TMDB 기반 콘텐츠 간 유사도를 title, overview, tagline, genres 필드를 기준으로 계산하고,
    min_score 이상인 top_k 콘텐츠를 추천해주는 클래스.
    """

    def __init__(self, content_list):
        """
        content_list: 추천 풀로 사용할 TMDB 콘텐츠 리스트 (dict 목록)
        """
        self.content_list = content_list
        if not self.content_list:
            raise ValueError("추천용 콘텐츠 리스트가 비어 있습니다.")

    def _get_field_as_string(self, val):
        """
        val이 문자열 또는 리스트(예: 장르 목록)일 경우 문자열로 변환
        """
        if isinstance(val, list):
            return " ".join(str(v) for v in val).strip()
        elif isinstance(val, str):
            return val.strip()
        return ""

    def compute_similarity(self, a, b, weights):
        """
        두 콘텐츠 a, b 간 유사도를 가중 평균 방식으로 계산
        weights는 {"overview": 0.4, "title": 0.3, ...} 형태
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

    def get_similar(self, content_id, top_k=5, weights=None, min_score=30):
        """
        기준 content_id에 대해 유사도가 min_score 이상인 콘텐츠 중
        유사도 상위 top_k개를 반환. 조건 충족 콘텐츠가 없으면 빈 리스트 반환.
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
            print(f"[❌] 콘텐츠 ID {content_id} 가 추천풀에 없음")
            return []

        scored = []
        for c in self.content_list:
            if c["id"] == content_id:
                continue
            score = self.compute_similarity(target, c, weights)
            if score >= min_score:
                scored.append((c, score))

        if not scored:
            print(f"[⚠️] 유사한 콘텐츠 없음 (유사도 ≥ {min_score})")
            return []

        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]
