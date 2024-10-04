def validate_create(create_data):
    title = create_data.get("title")
    content = create_data.get("content")
    category = create_data.get("category")

    if not all([title, content, category]):
        return False, "필수 입력값이 누락되었습니다."
    
    if len(title) > 50:
        return False, {"title": "제목의 길이는 50자 이하여야 합니다."}
    
    return True, None