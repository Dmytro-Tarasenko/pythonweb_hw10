from django.db.models import (Model,
                              CharField,
                              DateField,
                              TextField,
                              ManyToManyField,
                              ForeignKey,
                              ManyToOneRel,
                              CASCADE)
# Create your models here.


class Tag(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Quote(Model):
    text = TextField()
    author = ForeignKey('Author', on_delete=CASCADE)
    tags = ManyToManyField(Tag)

    def __str__(self):
        return f"{self.author}: {self.text[:50]}"


class Author(Model):
    fulname = CharField(max_length=100)
    birth_date = DateField()
    birth_location = CharField(max_length=100)
    description = TextField()
    # quotes = ManyToOneRel(to=Quote, field='author')

    def __str__(self):
        return f"{self.name} {self.birth_date}"
