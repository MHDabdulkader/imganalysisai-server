from sqlalchemy.orm import Session
from app.model.image_collection import ImageCollection
from app.model.image_version import ImageVersion
from app.schema.image_schema import ImageCollectionCreate

class ImageService:
    @staticmethod
    def create_image_collection(db:Session, data: ImageCollectionCreate):
        newImageCollection = ImageCollection(
            prompt = data.prompt,
            model = data.model,
            style = data.style,
            user_id = data.user_id
        )
        db.add(newImageCollection)
        db.flush()
        
        for version in data.image_version:
            new_version = ImageVersion(
                image_url=version.image_url,
                parent_id = newImageCollection.id,
                isFinal = True,
                collection_id = newImageCollection.id
            )
            db.add(new_version)
        
        db.commit()
        db.refresh(newImageCollection)
        return newImageCollection
    
    @staticmethod
    def add_version(db: Session, collection_id: int, image_url: str, isFinal: bool = False):
        collection = db.query(ImageCollection).filter(
            ImageCollection.id == collection_id
        ).first()
        
        if not collection:
            return None
        
        new_version = ImageVersion(
            image_url=image_url
        )
    
    @staticmethod
    def get_by_id(db: Session, id: int):
        response_query = db.query(ImageCollection).filter(ImageCollection.id == id).first()
        return response_query
    
    @staticmethod
    def get_by_userid(db: Session, user_id: int):
        response_query = db.query(ImageCollection).filter(ImageCollection.user_id== user_id).all()
        return response_query
    
    @staticmethod
    def get_all(db: Session):
        response_query = db.query(ImageCollection).all()
        return response_query
