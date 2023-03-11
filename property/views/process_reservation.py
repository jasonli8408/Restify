from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from ..models import Reservation, Property, PropertyAvailability
from django import forms
from backend.constants import *
import datetime
from django.db.models import Q


class ReserveForm(forms.Form):
    start_date = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
    end_date = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
    property_id = forms.IntegerField(required=True)

    # def clean(self):
    #     start_date = self.cleaned_data['start_date']
    #     end_date = self.cleaned_data['end_date']
    #
    #     return self.cleaned_data


class RequestForm(forms.Form):
    reservation_id = forms.IntegerField()


class ProcessForm(forms.Form):
    reservation_id = forms.IntegerField()
    decision = forms.BooleanField(required=False)


class ReserveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        form = ReserveForm(request.data)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            property_id = form.cleaned_data['property_id']

            if end_date < start_date:
                return Response({'errors': 'invalid reserve request'}, status=status.HTTP_400_BAD_REQUEST)

            current_date = start_date
            total_price = 0
            is_valid = True
            while current_date <= end_date:
                reserve_property = get_object_or_404(Property, id=property_id)
                if Reservation.objects.filter(start_date__lte=current_date,
                                              end_date__gte=current_date,
                                              property=reserve_property,
                                              status=PENDING):
                    is_valid = False
                if Reservation.objects.filter(start_date__lte=current_date,
                                              end_date__gte=current_date,
                                              property=reserve_property,
                                              status=APPROVED):
                    is_valid = False
                if Reservation.objects.filter(start_date__lte=current_date,
                                end_date__gte=current_date,
                                property=reserve_property,
                                status=CANCELING):
                    is_valid = False
                r_set = PropertyAvailability.objects.filter(start_date__lte=current_date,
                                                            end_date__gte=current_date,
                                                            property=reserve_property)
                if not r_set:
                    is_valid = False
                else:
                    total_price += r_set.get().price_per_night
                current_date += datetime.timedelta(days=1)

            if is_valid:
                new_reservation = Reservation(
                    client=user,
                    property=reserve_property,
                    total_price=total_price,
                    status=PENDING,
                    start_date=start_date,
                    end_date=end_date
                )
                new_reservation.save()
                return Response({'message': 'Reservation created successfully.',
                                 'id': new_reservation.id,
                                 'status': new_reservation.status,
                                 'guest': new_reservation.client.username,
                                 'host': new_reservation.property.user.username,
                                 'property': new_reservation.property.id,
                                 'start_date': new_reservation.start_date,
                                 'end_date': new_reservation.end_date,
                                 'total_price': new_reservation.total_price})
            else:
                return Response({'errors': 'time slot unavailable'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = self.request.user
        form = RequestForm(request.data)
        if form.is_valid():
            r_id = form.cleaned_data['reservation_id']
            reservation = get_object_or_404(Reservation, id=r_id)
            if reservation.client == user:
                if reservation.status in [PENDING, APPROVED]:
                    if reservation.status == PENDING:
                        reservation.status = CANCELED
                    else:
                        reservation.status = CANCELING
                    reservation.save()
                    return Response({'message': 'Reservation requested.',
                                     'id': reservation.id,
                                     'status': reservation.status,
                                     'guest': reservation.client.username,
                                     'host': reservation.property.user.username,
                                     'property': reservation.property.id,
                                     'start_date': reservation.start_date,
                                     'end_date': reservation.end_date,
                                     'total_price': reservation.total_price})
                else:
                    return Response({'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors': 'invalid request'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProcessPendingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = self.request.user
        form = ProcessForm(request.data)
        if form.is_valid():
            r_id = form.cleaned_data['reservation_id']
            decision = form.cleaned_data['decision']
            reservation = get_object_or_404(Reservation, id=r_id)
            if reservation.property.user == user:
                if reservation.status == PENDING:
                    if decision:
                        reservation.status = APPROVED
                    else:
                        reservation.status = DENIED
                    reservation.save()
                    return Response({'message': 'Your decision has been made.',
                                     'id': reservation.id,
                                     'status': reservation.status,
                                     'guest': reservation.client.username,
                                     'host': reservation.property.user.username,
                                     'property': reservation.property.id,
                                     'start_date': reservation.start_date,
                                     'end_date': reservation.end_date,
                                     'total_price': reservation.total_price})
                else:
                    return Response({'errors': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors': 'invalid request'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProcessCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = self.request.user
        form = ProcessForm(request.data)
        if form.is_valid():
            r_id = form.cleaned_data['reservation_id']
            decision = form.cleaned_data['decision']
            reservation = get_object_or_404(Reservation, id=r_id)
            if reservation.property.user == user:
                if reservation.status == CANCELING:
                    if decision:
                        reservation.status = CANCELED
                    else:
                        reservation.status = APPROVED
                    reservation.save()
                    return Response({'message': 'Your decision has been made.',
                                     'id': reservation.id,
                                     'status': reservation.status,
                                     'guest': reservation.client.username,
                                     'host': reservation.property.user.username,
                                     'property': reservation.property.id,
                                     'start_date': reservation.start_date,
                                     'end_date': reservation.end_date,
                                     'total_price': reservation.total_price})
                else:
                    return Response({'errors': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors': 'invalid request'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class TerminateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = self.request.user
        form = RequestForm(request.data)
        if form.is_valid():
            r_id = form.cleaned_data['reservation_id']
            reservation = get_object_or_404(Reservation, id=r_id)
            if reservation.property.user == user:
                if reservation.status == APPROVED:
                    reservation.status = TERMINATED
                    reservation.save()
                    return Response({'message': 'Your decision has been made.',
                                     'id': reservation.id,
                                     'status': reservation.status,
                                     'guest': reservation.client.username,
                                     'host': reservation.property.user.username,
                                     'property': reservation.property.id,
                                     'start_date': reservation.start_date,
                                     'end_date': reservation.end_date,
                                     'total_price': reservation.total_price})
                else:
                    return Response({'errors': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors': 'invalid request'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)