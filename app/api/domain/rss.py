from datetime import datetime
from pydantic import BaseModel


class RssItem(BaseModel):
    title: str
    description: str
    link: str
    publish_date: datetime
