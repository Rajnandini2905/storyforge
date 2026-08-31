from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(
        max_length=50,
        choices=[
            ('fantasy', 'Fantasy'), ('scifi', 'Sci-Fi'), ('mystery', 'Mystery'),
            ('horror', 'Horror'), ('adventure', 'Adventure'), ('romance', 'Romance'),
            ('thriller', 'Thriller'), ('comedy', 'Comedy'),
            ('cyberpunk', 'Cyberpunk'), ('historical', 'Historical Fiction')
        ],
        default='fantasy'
    )
    cover_emoji = models.CharField(max_length=10, default='📖')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    is_published = models.BooleanField(default=True)
    play_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, blank=True, related_name='start_of_stories')

    class Meta:
        verbose_name_plural = 'Stories'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def node_count(self):
        return self.nodes.count()

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.stars for r in ratings) / len(ratings)
        return 0.0

class Node(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='nodes')
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    is_ending = models.BooleanField(default=False)
    ending_type = models.CharField(
        max_length=20,
        choices=[('good', 'Good Ending 🌟'), ('bad', 'Bad Ending 💀'), ('neutral', 'Neutral Ending 🌙')],
        default='',
        blank=True
    )
    order = models.PositiveIntegerField(default=0)
    step_number = models.IntegerField(default=1) # added for AI step tracking

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.story.title} - {self.title or 'Node ' + str(self.order)}"

class Choice(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    next_node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_choices')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.choice_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar_emoji = models.CharField(max_length=10, default='🧙')
    stories_completed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', help_text='Linked Django auth_user row (manages sessions)')
    username = models.CharField(max_length=150, unique=True, help_text='Chosen at signup — must be unique across all users')
    email = models.EmailField(default='', blank=True, help_text='Optional contact email')
    hashed_password = models.CharField(max_length=255, help_text='PBKDF2-SHA256 hash via Django make_password() — NEVER plain text')
    joined_at = models.DateTimeField(auto_now_add=True, help_text='Auto-set when the row is created')
    last_login_at = models.DateTimeField(null=True, blank=True, help_text='Updated every time the user logs in successfully')
    is_active = models.BooleanField(default=True, help_text='Uncheck to disable this account without deleting it')
    avatar_emoji = models.CharField(max_length=10, default='🧙')
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        db_table = 'stories_useraccount'
        ordering = ['-joined_at']

    def __str__(self):
        return self.username

class Rating(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')

class Bookmark(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')

class UserProgress(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='progress')
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    current_node = models.ForeignKey(Node, on_delete=models.CASCADE)
    visited_nodes = models.TextField(default='')
    choices_made = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'story')

class PlaySession(models.Model):
    # Appears in admin.py
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    ending_type = models.CharField(max_length=20, blank=True)
    steps_taken = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)