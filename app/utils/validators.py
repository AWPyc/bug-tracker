
def title_must_not_be_empty(title: str) -> str:
    if title and title.strip():
        return title
    raise ValueError("Title must not be empty!")

def description_must_not_be_empty(desc: str) -> str:
    if desc and desc.strip():
        return desc
    raise ValueError("Description must not be empty!")

def tag_name_must_not_be_empty(tag: str) -> str:
    if tag and tag.strip():
        return tag
    raise ValueError("Tag must not be empty!")
