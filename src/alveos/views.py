from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import ConnectForm

class ChatView(FormView):
    form_class = ConnectForm
    success_url = reverse_lazy('chatview')

    def form_valid(self, form):
        # Save nickname in session
        self.request.session['nickname'] = form.cleaned_data['nickname']
        return super(ChatView, self).form_valid(form)

    def get_template_names(self):
        if self.request.session.get('nickname', None):
            print("We have a nickname in the session %s (%s), so show the chat template" % (self.request.session.session_key, self.request.session.get('nickname', None)))
            return ['chat.html']
        else:
            # We need a nickname before the fun starts
            return ['connect.html']

