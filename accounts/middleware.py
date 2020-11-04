from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from employee.emp_models.model_comp import LoggedInUser
#Session model stores the session data
from django.contrib.sessions.models import Session

class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()


class OneSessionPerUserMiddleware:
    # Now called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            try:
                logged_in_user = request.user.logged_in_user
                stored_session_key = logged_in_user.session_key
                # stored_session_key exists so delete it if it's different
                if stored_session_key != session_key:
                    Session.objects.filter(session_key=stored_session_key).delete()
                logged_in_user.session_key = session_key
                logged_in_user.save()
            except LoggedInUser.DoesNotExist:
                LoggedInUser.objects.create(user=request.user, session_key=session_key)

        response = self.get_response(request)

        return response