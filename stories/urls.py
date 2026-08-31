from django.urls import path
from . import views

urlpatterns = [
    # Library
    path('',                              views.homepage,       name='homepage'),
    path('search/',                       views.search_view,    name='search'),
    path('leaderboard/',                  views.leaderboard,    name='leaderboard'),

    # Story
    path('story/<int:story_id>/',                      views.story_detail,   name='story_detail'),
    path('story/<int:story_id>/play/',                 views.story_play,     name='story_play'),
    path('story/<int:story_id>/play/<int:node_id>/',   views.story_play,     name='story_play_node'),
    path('story/<int:story_id>/choose/',               views.story_choose,   name='story_choose'),
    path('story/<int:story_id>/restart/',              views.story_restart,  name='story_restart'),

    # Social
    path('story/<int:story_id>/bookmark/', views.bookmark_toggle, name='bookmark_toggle'),
    path('story/<int:story_id>/rate/',     views.rate_story,      name='rate_story'),
    path('story/<int:story_id>/comment/',  views.add_comment,     name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Auth — Sign Up / Sign In / Sign Out
    path('signup/',  views.signup_view,  name='signup'),
    path('signin/',  views.signin_view,  name='signin'),
    path('signout/', views.signout_view, name='signout'),

    # Profile
    path('profile/',      views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
