#to test on vs use uncoment this code
#from app.main import app as application


#if __name__ == "__main__":
#    application.run()

# to deploy on render we should to use the follow structure in wsgi
from app.main import app as application
app = application
