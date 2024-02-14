class EmbedSchema:
    def __init__(self, title: str, description: str, fields: list, color: int, thumbnail_url: str = None, image_url: str = None, footer_text: str = None, author_url: str = None) -> None:
        self.title = title
        self.description = description
        self.fields = fields
        self.color = color
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.footer_text = footer_text
        self.author_url = author_url

    def __repr__(self) -> str:
        return f"<EmbedSchema title={self.title} description={self.description} fields={self.fields} color={self.color}> thumbnail_url={self.thumbnail_url} image_url={self.image_url} footer_text={self.footer_text}"

    def get_schema(self) -> dict:
        schema = {
            "title": self.title,
            "description": self.description,
            "fields": self.fields,
            "color": self.color,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "footer_text": self.footer_text,
            "author_url": self.author_url,
        }
        return schema
