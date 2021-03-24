from allauth.account.models import EmailAddress
from allauth.account.signals import user_signed_up
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings
from invitations.models import Invitation
from invitations.signals import invite_accepted
from invitations.utils import get_invitation_model
from invitations.views import AcceptInvite
from recipes.models import Recipe, Bookmarks
from user.models import Profile
from .forms import ProfileUpdateForm, UserCreationForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(
                request, f'تهانينا {new_user} لقد تمت عملية التسجيل بنجاح.')
            return redirect('user:login')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {
        'title': 'التسجيل',
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:profile')
        else:
            messages.warning(
                request, 'هناك خطأ في اسم المستخدم أو كلمة المرور.')

    return render(request, 'user/login.html', {
        'title': 'تسجيل الدخول',
    })


def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html', {
        'title': 'تسجيل الخروج'
    })


class ProfileDetail(LoginRequiredMixin, SingleObjectMixin, ListView):
    # ORIGINAL ATTRIBUTES
    login_url = 'user:login'
    model = User
    template_name = 'user/profile.html'
    paginate_by = 10
    paginate_orphans = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, username=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


@login_required(login_url='user:login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'تم تحديث الملف الشخصي.')
            return redirect('user:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'تعديل الملف الشخصي',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'user/profile_update.html', context)


# ---------------- INVITATIONS --------------------------
def invite_friend(request):
    # inviter argument is optional
    Invitation = get_invitation_model()
    invite = Invitation.create('email1@example1.com', inviter=request.user)
    invite.send_invitation(request)
    return redirect(app_settings.SIGNUP_REDIRECT)


# django-invitations https://gist.github.com/nsomaru/53d0caf0981b56d57d77649b29c8cd1d
class AcceptInviteView(AcceptInvite):
    def post(self, *args, **kwargs):
        self.object = invitation = self.get_object()

        # Compatibility with older versions: return an HTTP 410 GONE if there
        # is an error. # Error conditions are: no key, expired key or
        # previously accepted key.
        if app_settings.GONE_ON_ACCEPT_ERROR and \
                (not invitation or
                 (invitation and (invitation.accepted or
                                  invitation.key_expired()))):
            return HttpResponse(status=410)

        # No invitation was found.
        if not invitation:
            # Newer behavior: show an error message and redirect.
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_invalid.txt')
            return redirect(app_settings.LOGIN_REDIRECT)

        # The invitation was previously accepted, redirect to the login
        # view.
        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_already_accepted.txt',
                {'email': invitation.email})
            # Redirect to login since there's hopefully an account already.
            return redirect(app_settings.LOGIN_REDIRECT)

        # The key was expired.
        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_expired.txt',
                {'email': invitation.email})
            # Redirect to sign-up since they might be able to register anyway.
            return redirect(app_settings.SIGNUP_REDIRECT)

        get_invitations_adapter().stash_verified_email(
            self.request, invitation.email)

        get_invitations_adapter().add_message(
            self.request,
            messages.SUCCESS,
            'invitations/messages/invite_accepted.txt',
            {'email': invitation.email})

        return redirect(app_settings.SIGNUP_REDIRECT)


@receiver(user_signed_up)
def accept_invite(sender, request, user, **kwargs):
    # Traverse from the user to verified email addresses. It is possible for a
    # user to already have multiple email addresses if they typed in a different
    # email after accepted the invite. In this case, the user will have two
    # emails, but only one will be verified.
    addresses = EmailAddress.objects.filter(user=user, verified=True) \
        .values_list('email', flat=True)
    # Check if any invites exist for this address and were accepted.
    invites = Invitation.objects.filter(email__in=addresses)
    if invites:
        # Mark all these invites as accepted.
        invites.update(accepted=True)
        for invite in invites:
            # Note that this doesn't send it with a request.
            invite_accepted.send(sender=Invitation, email=invite.email)

        # Figure out if you care if there are multiple invites here


@login_required
def MyProfileView(request):
    profile = Profile.objects.get(user=request.user)
    recipes = Recipe.objects.filter(author=profile)
    bookmarks = Bookmarks.objects.get(profile=profile).recipes.all()

    # posts
    context = {
    }
    context['profile'] = profile
    context['recipes'] = recipes
    context['bookmarks'] = bookmarks
    return render(request, "user/my-account.html", context)
