from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kero.views.home', name='home'),
    # url(r'^kero/', include('kero.foo.urls')),

    url(r'^$', 'network.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    
)

"""
Using the URLconf defined in kero.urls, Django tried these URL patterns, in this order:
^admin/
^accounts/ ^activate/complete/$ [name='registration_activation_complete']
^accounts/ ^activate/(?P<activation_key>\w+)/$ [name='registration_activate']
^accounts/ ^register/$ [name='registration_register']
^accounts/ ^register/complete/$ [name='registration_complete']
^accounts/ ^register/closed/$ [name='registration_disallowed']
^accounts/ ^login/$ [name='auth_login']
^accounts/ ^logout/$ [name='auth_logout']
^accounts/ ^password/change/$ [name='auth_password_change']
^accounts/ ^password/change/done/$ [name='auth_password_change_done']
^accounts/ ^password/reset/$ [name='auth_password_reset']
^accounts/ ^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$ [name='auth_password_reset_confirm']
^accounts/ ^password/reset/complete/$ [name='auth_password_reset_complete']
^accounts/ ^password/reset/done/$ [name='auth_password_reset_done']
"""
