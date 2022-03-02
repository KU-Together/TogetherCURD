from rest_framework import serializers
from .models import User, Board, List, Card

class PrevCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id',)

class CardSerializer(serializers.ModelSerializer):
    prev_card = PrevCardSerializer().data
    class Meta:
        model = Card
        fields = (
            "id", 
            "task_title",
            "deadline",
            "task_detail",
            "is_memorable",
            "emoji",
            "prev_card",
            "list",
        )

class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ("status", "board_id", "cards")


class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ("id", "board_title", "lists")


class UserSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("id", "email", "password", "boards")