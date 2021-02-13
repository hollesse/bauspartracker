from django.contrib.auth.models import User
from django.db import models


class Bausparvertrag(models.Model):
    class Meta:
        verbose_name_plural = "Bausparverträge"

    ZEITRAUM_CHOICES = (
        ('JAEHRLICH', 'jährlich'),
        ('HALBJAEHRLICH', 'halbjährlich'),
        ('VIERTELJAEHRLICH', 'vierteljährlich'),
        ('MONATLICH', 'monatlich'),
        ('EINMALIG', 'einmalig'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bausparvertraege')
    bausparsumme = models.IntegerField()
    abschlussgebuehren_prozent = models.IntegerField(null=True)
    abschlussgebuehren_in_euro = models.IntegerField(null=True)
    laufende_gebuehren_prozent = models.IntegerField(null=True)
    laufende_gebuehren_in_euro = models.IntegerField(null=True)
    laufende_gebuehren_zeitraum = models.CharField(max_length=16, choices=ZEITRAUM_CHOICES)
    zinsen_ansparphase = models.IntegerField()


class Sparbeitrag(models.Model):
    class Meta:
        verbose_name_plural = "Sparbeiträge"

    ZEITRAUM_CHOICES = (
        ('JAEHRLICH', 'jährlich'),
        ('HALBJAEHRLICH', 'halbjährlich'),
        ('VIERTELJAEHRLICH', 'vierteljährlich'),
        ('MONATLICH', 'monatlich'),
        ('EINMALIG', 'einmalig'),
    )
    betrag = models.IntegerField()
    erste_buchung = models.DateField()
    letzte_buchung = models.DateField(null=True)
    bausparvertrag = models.ForeignKey(Bausparvertrag, on_delete=models.CASCADE, related_name='sparbeitraege')


class Buchung(models.Model):
    class Meta:
        verbose_name_plural = "Buchungen"

    BUCHUNGSART_CHOICES = (
        ('ABSCHLUSSGEBUEHR', 'Abschlussgebühr'),
        ('LAUFENDE_GEBUEHR', 'Laufende Gebühr'),
        ('SPARBEITRAG', 'Sparbeitrag'),
    )
    datum = models.DateField()
    betrag = models.IntegerField()
    art = models.CharField(max_length=16, choices=BUCHUNGSART_CHOICES)
    bausparvertrag = models.ForeignKey(Bausparvertrag, on_delete=models.CASCADE, related_name='buchungen')
    sparbetrag = models.ForeignKey(Sparbeitrag, on_delete=models.CASCADE, related_name='buchungen')



