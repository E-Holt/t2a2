from main import db

class Bean(db.Model):
    #define the tablename in the database as beans
    __tablename__="beans"
    # setting the columns 
    bean_id = db.Column(db.Integer, primary_key = True)
    country = db.Column(db.String())
    variety = db.Column(db.String())
    flavour_notes = db.Column(db.String())
    roast = db.Column(db.String())
    recommended_preparation = db.Column(db.String())
    processing_method = db.Column(db.String())
    roaster_id = db.Column(db.Integer, db.ForeignKey("roasters.roaster_id"), nullable=False)
