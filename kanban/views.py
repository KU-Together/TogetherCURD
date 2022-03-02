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
        raw_query = f'''WITH RECURSIVE c3 (id, prev_card_id) AS
                        (
                            SELECT c1.id, c1.prev_card_id
                            FROM Card c1
                            WHERE 1=1
                            AND c1.list_id = {list.id}
                            AND c1.prev_card_id is null
                            UNION ALL
                            SELECT c2.id, c2.prev_card_id
                            FROM Card c2
                            INNER JOIN c3 ON c2.list_id = {list.id} and c2.prev_card_id = c3.id
                        )

                        SELECT * FROM c3;
                    '''
        
        card = Card.objects.raw(raw_query)
        serializer = CardSerializer(card, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i].pop("list")
            serializer.data[i]["user_id"] = user_id
            serializer.data[i]["status"] = status
            # serializer.data[i]["prev_card"] = serializer.data[i]["prev_card"][0]

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
            "prev_card": request.data["prev_card"],
            "list": list.id
        }
        card_serializer = CardSerializer(data = card_data)
        if card_serializer.is_valid(raise_exception=False):
            card_serializer.save()
            
            data = dict(card_serializer.data)
            data["user_id"] = user_id
            data["status"] = status
            data.pop("list")
            
            return Response(data, status=STATUS.HTTP_201_CREATED)
        else:
            return Response({"message": card_serializer.errors}, status=STATUS.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, user_id, board_id, status, card_id):
        print(request.data)
        if "status" in request.data.keys():
            list = List.objects.filter(board_id = board_id, status = request.data["status"]).first()
            request.data["list"] = list.id
        else:
            list = List.objects.filter(board_id = board_id, status = status).first()

        card = Card.objects.get(id=card_id)
        card_serializer = CardSerializer(card, data = request.data, partial=True)
        if card_serializer.is_valid(raise_exception=True):
            card_serializer.save()

            data = dict(card_serializer.data)
            data['user_id'] = user_id
            data['status'] = list.status
            data.pop('list')
            print(data)

            return Response(data, status=STATUS.HTTP_200_OK)
        else:
            return Response({"message": card_serializer.errors}, status=STATUS.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id, board_id, status, card_id):
        card = Card.objects.get(id=card_id)
        card.delete()
        return Response(status=STATUS.HTTP_204_NO_CONTENT)