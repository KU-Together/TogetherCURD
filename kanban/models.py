from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length = 150, blank = False, null = False)

    class Meta:
        db_table = "User"
        constraints = [
            models.UniqueConstraint(
                fields=["id", "email"],
                name="unique email",
            )
        ]


class Board(models.Model):
    board_title = models.CharField(max_length = 150, blank = False, null = False)
    user = models.ForeignKey(User, related_name='boards', on_delete = models.CASCADE)

    class Meta:
        db_table = "Board"


class List(models.Model):
    TYPE_OF_STATUS = (
        ('T', 'To Do'),
        ('I', 'In Progress'),
        ('C', 'Completed'),
        ('D', 'Deleted')
    )

    status = models.CharField(max_length = 1, choices = TYPE_OF_STATUS, blank = False, null = False)
    board = models.ForeignKey(Board, related_name="lists", on_delete = models.CASCADE)

    class Meta:
        db_table = "List"
        constraints = [
            models.UniqueConstraint(
                fields=["status", "board"],
                name="unique board status",
            )
        ]


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
    list = models.ForeignKey(List, related_name="cards", on_delete = models.CASCADE)

    class Meta:
        db_table = "Card"