import typing as t
from atom_bk_frame.auth.controllers.sign_in_contrller import SignInController
from atom_bk_frame.auth.controllers.sign_out_controller import SignOutController
from atom_bk_frame.auth.controllers.sign_up_controller import SignUpController
from atom_bk_frame.core.url_pattern import UrlPattern

auth_urlpatterns: t.List[UrlPattern] = [
    UrlPattern(path='/signup', controller=SignUpController()),
    UrlPattern(path='/signin', controller=SignInController()),
    UrlPattern(path='/signout', controller=SignOutController())
]