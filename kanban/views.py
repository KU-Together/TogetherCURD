from django.shortcuts import render
from django.core.exceptions import *

from rest_framework import status as STATUS
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Board, List, Card
from .serializers import UserSerializer, BoardSerializer, ListSerializer, CardSerializer

class UserViewset(viewsets.ModelViewSet):
    def retrieve(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=STATUS.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=STATUS.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=STATUS.HTTP_400_BAD_REQUEST)


class CardViewset(viewsets.ModelViewSet):
    def list(self, request, user_id, board_id, status):
        list = List.objects.filter(status=status, board=board_id, board__user = user_id).first()
        card = Card.objects.filter(list = list)
        serializer = CardSerializer(card, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i].pop("list")
            # serializer.data[i]["user_id"] = user_id
            # serializer.data[i]["status"] = status

        return Response(serializer.data, status=STATUS.HTTP_200_OK)

    def create(self, request, user_id, board_id, status):
        #user
        list = List.objects.filter(board=board_id, status=status, board__user = user_id).first()

        # card
        card_data = { 
            "task_title": request.data["task_title"],
            "deadline": request.data["deadline"],
            "task_detail": request.data["task_detail"],
            "is_memorable": request.data["is_memorable"],
            "emoji": request.data["emoji"],
            "next_card_id": request.data["next_card_id"],
            "list": list.id
        }
        card_serializer = CardSerializer(data = card_data)
        if card_serializer.is_valid(raise_exception=False):
            card_serializer.save()
            
            for i in range(len(card_serializer.data)):
                card_serializer.data[i].pop("list")
                # card_serializer.data[i]["user_id"] = user_id
                # card_serializer.data[i]["board_id"] = board_id
                # card_serializer.data[i]["status"] = status
            return Response(card_serializer.data, status=STATUS.HTTP_201_CREATED)
        else:
            return Response({"message": card_serializer.errors}, status=STATUS.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, user_id, board_id, card_id):
        card = Card.objects.get(id=card_id)
        card_serializer = CardSerializer(card, data = request.data, partial=True)
        if card_serializer.is_valid(raise_exception=False):
            card_serializer.save()

            for i in range(len(card_serializer.data)):
                card_serializer.data[i].pop("list")
                # card_serializer.data[i]["user_id"] = user_id
                # card_serializer.data[i]["board_id"] = board_id
                # card_serializer.data[i]["status"] = request.data["status"]
            return Response(card_serializer.data, status=STATUS.HTTP_200_OK)
        else:
            return Response({"message": card_serializer.errors}, status=STATUS.HTTP_400_BAD_REQUEST)