
def title_must_not_be_empty(title: str) -> str:
    if title and title.strip():
        return title
    raise ValueError("Title must not be empty!")

def description_must_not_be_empty(desc: str) -> str:
    if desc and desc.strip():
        return desc
    raise ValueError("Description must not be empty!")
