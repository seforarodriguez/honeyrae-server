"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Customer, Employee


class TicketView(ViewSet):
    """Honey Rae API Tickets view"""

    def list(self, request):
        """Handle GET requests to get all Tickets

        Returns:
            Response -- JSON serialized list of Tickets
        """
        service_tickets = []

        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    service_tickets = service_tickets.filter(date_completed__isnull=False)
                if request.query_params['status'] == "all":
                    pass    
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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for service tickets
        
        returns:
            Response none with 204 status code
        """

        service_ticket = ServiceTicket.objects.get(pk=pk)
        service_ticket.delete()

        return Response(None, status= status.HTTP_204_NO_CONTENT)
    
    
    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data['description']
        new_ticket.emergency = request.data['emergency']
        new_ticket.save()

        serialized = TicketSerializer(new_ticket, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """This Handles the PUT operation of the ticket to change the employee
        
        Returns:
            Response: No response body, just the 204 status code saying is was updated
        """
        # Select the targeted ticket using pk that was passed through
        ticket = ServiceTicket.objects.get(pk=pk)

        # get the employee id from the client request
        employee_id = request.data['employee']

        # Select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)

        # Assign the employee instance that was just grabbed from line 75 to the employee property of the ticket
        ticket.employee = assigned_employee

        # save the updated ticket because you rocked the update function
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TicketEmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for Employee"""
    class Meta:
        model = Employee
        fields = ( 'id', 'full_name', 'specialty',)

class TicketCustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for Employee"""
    class Meta:
        model = Customer
        fields = ('full_name',)

class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for Tickets"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )
        depth = 1