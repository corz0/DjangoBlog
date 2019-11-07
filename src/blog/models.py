from django.db import models
from django.db.models import Q
#modelo de user
from django.conf import settings
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        ##
        # para buscar por titulo
        ### return self.filter(title__iexact=query)
        ##
        # para buscar por contenido
        ### return self.filter(content__iconatains=query)
        lookup = (
            # busca por titulo
            Q(title__icontains=query) |
            # busca por contenido
            Q(content__icontains=query) |
            # busca por usuario
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query)
            )

        return self.filter(lookup)

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self.db)

    def published(self):
        return self.get_queryset().published()
    
    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

class BlogPost(models.Model):
    #id = models.IntegerField() # pk
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(null= True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = BlogPostManager()

#funcion utilizada en blog/list.html para utilziar el slug en la url
    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"/blog/{self.slug}/update"

    def get_delete_url(self):
        return f"/blog/{self.slug}/delete"
