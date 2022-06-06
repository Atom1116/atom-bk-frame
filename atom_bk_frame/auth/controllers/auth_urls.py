import typing as t
from todo_scratch.bk_base.auth.controllers.sign_in_contrller import SignInController
from todo_scratch.bk_base.auth.controllers.sign_out_controller import SignOutController
from todo_scratch.bk_base.auth.controllers.sign_up_controller import SignUpController
from todo_scratch.bk_base.core.url_pattern import UrlPattern

auth_urlpatterns: t.List[UrlPattern] = [
    UrlPattern(path='/signup', controller=SignUpController()),
    UrlPattern(path='/signin', controller=SignInController()),
    UrlPattern(path='/signout', controller=SignOutController())
]
