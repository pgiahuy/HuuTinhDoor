class Config:
    SECRET_KEY = "supersecret"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/huutinhdoor"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLOUDINARY = {
        "cloud_name": "dbxtbus46",
        "api_key": "994774263527943",
        "api_secret": "HLpoMPuSSuFMTLFeEP805AriVsk",
        "secure": True
    }
