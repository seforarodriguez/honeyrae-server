"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Employee


class EmployeeView(ViewSet):
    """Honey Rae API Employees view"""

    def list(self, request):
        """Handle GET requests to get all Employees

        Returns:
            Response -- JSON serialized list of Employees
        """

        Employees = Employee.objects.all()
        serialized = EmployeeSerializer(Employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Employee

        Returns:
            Response -- JSON serialized Employee record
        """

        Employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(Employee, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for Employees"""
    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'specialty')