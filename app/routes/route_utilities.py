from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} is invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} is not found"}
        abort(make_response(response, 404))

    return model

# review this function and use for post route
def create_model_from_dict(cls, data):
    model = cls.from_dict(data)
    db.session.add(model)
    db.session.commit()
    return model 

# what about get model by filter? 