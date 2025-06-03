def get_similar(self, content_id, top_k=5, weights=None, min_score=1):
    """
    기준 콘텐츠 ID와 유사한 콘텐츠를 유사도 기준으로 top_k개 반환.
    min_score 미만은 무시. 추천할 게 없으면 빈 리스트 반환.
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
        if score >= min_score:  # ✅ 최소 유사도 기준 도입
            scored.append((c, score))

    if not scored:
        print(f"[⚠️] 유사한 콘텐츠 없음 (유사도 ≥ {min_score})")
        return []

    scored.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in scored[:top_k]]
