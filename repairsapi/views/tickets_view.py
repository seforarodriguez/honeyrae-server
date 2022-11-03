"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket


class TicketView(ViewSet):
    """Honey Rae API Tickets view"""

    def list(self, request):
        """Handle GET requests to get all Tickets

        Returns:
            Response -- JSON serialized list of Tickets
        """
        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()
            serialized = TicketSerializer(service_tickets, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            service_tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)
            serialized = TicketSerializer(service_tickets, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single Ticket

        Returns:
            Response -- JSON serialized Ticket record
        """

        Ticket = ServiceTicket.objects.get(pk=pk)
        serialized = TicketSerializer(Ticket, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for Tickets"""
    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )
        depth = 1