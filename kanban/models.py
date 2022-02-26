from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length = 150, blank = False, null = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id", "email"],
                name="unique email",
            )
        ]

    def getValues(self):
        data = {}
        data['id'] = self.id
        data['email'] = self.email
        return data
    
    def setValues(self, data):
        self.email = data['email']
        self.password = data['password']


class Board(models.Model):
    board_title = models.CharField(max_length = 150, blank = False, null = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def getValues(self):
        data = {}
        data['id'] = self.id
        data['board_title'] = self.board_title
        # data['user'] = self.user.getValues()
        return data

    def setValues(self, data):
        self.board_title = data['board_title']
        # self.user = data['user']

class List(models.Model):
    TYPE_OF_STATUS = (
        ('T', 'To Do'),
        ('I', 'In Progress'),
        ('C', 'Completed'),
        ('D', 'Deleted')
    )

    list_title = models.CharField(max_length = 1, choices = TYPE_OF_STATUS, blank = False, null = True)
    board = models.ForeignKey(Board, on_delete = models.CASCADE)

class Card(models.Model):
    TYPE_OF_EMOJI = (
        ('H', 'Happy'),
        ('S', 'Sad'),
        ('A', 'Angry')
    )

    task_title = models.CharField(max_length = 150, blank = False, null = False)
    deadline = models.DateField(blank = False, null = False)
    task_detail = models.TextField()
    is_memorable = models.BooleanField(default = True)
    emoji = models.CharField(max_length = 1, choices = TYPE_OF_EMOJI)
    next_card_id = models.ForeignKey("Card", on_delete = models.SET_NULL, blank=True, null=True)
    list = models.ForeignKey(List, on_delete = models.CASCADE)