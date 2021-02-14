from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


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
    bausparkasse = models.CharField(max_length=255)
    tarifname = models.CharField(max_length=255)
    vertragsbeginn = models.DateField()
    bausparsumme = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    abschlussgebuehren_prozent = models.FloatField(null=True, blank=True)
    abschlussgebuehren_in_euro = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', null=True, blank=True)
    laufende_gebuehren_in_euro = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    laufende_gebuehren_zeitraum = models.CharField(max_length=16, choices=ZEITRAUM_CHOICES)
    zinsen_ansparphase = models.FloatField()

    def is_abschlussgebuehren_in_prozent(self):
        if self.abschlussgebuehren_prozent:
            return True
        return False

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username + ' - ' + self.bausparkasse + ' ' + self.tarifname + ' (' + str(self.bausparsumme) + ')'


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
    betrag = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    erste_buchung = models.DateField()
    letzte_buchung = models.DateField(null=True, blank=True)
    bausparvertrag = models.ForeignKey(Bausparvertrag, on_delete=models.CASCADE, related_name='sparbeitraege')

    def __str__(self):
        return str(self.bausparvertrag) + ' - ' + str(self.betrag) + ' (' + str(self.erste_buchung) + ' - ' + str(self.letzte_buchung) + ')'


class SparbeitragJob(models.Model):
    STATUS_CHOICES = (
        ('GEPLANT', 'geplant'),
        ('WIRD_AUSGEFUEHRT', 'wird ausgeführt'),
        ('ERFOLGREICH_ABGESCHLOSSEN', 'erfolgreich abgeschlossen'),
        ('ABGEBROCHEN', 'abgebrochen'),
    )
    von_datum_inklusive = models.DateField()
    bis_datum_inklusive = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    sparbeitrag = models.ForeignKey(Sparbeitrag, on_delete=models.CASCADE, related_name='jobs')


class Buchung(models.Model):
    class Meta:
        verbose_name_plural = "Buchungen"

    BUCHUNGSART_CHOICES = (
        ('ABSCHLUSSGEBUEHR', 'Abschlussgebühr'),
        ('LAUFENDE_GEBUEHR', 'Laufende Gebühr'),
        ('SPARBEITRAG', 'Sparbeitrag'),
    )
    datum = models.DateField()
    betrag = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    art = models.CharField(max_length=16, choices=BUCHUNGSART_CHOICES)
    bausparvertrag = models.ForeignKey(Bausparvertrag, on_delete=models.CASCADE, related_name='buchungen')
    sparbetrag = models.ForeignKey(Sparbeitrag,
                                   on_delete=models.CASCADE,
                                   related_name='buchungen',
                                   null=True,
                                   blank=True)

    def __str__(self):
        return str(self.bausparvertrag) + ' - ' + str(self.datum) + ' ' + str(self.art) + ' ' + str(self.betrag)


def create_abschlussgebuehr_buchung(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return

    if instance.is_abschlussgebuehren_in_prozent:
        betrag = - round(instance.bausparsumme / 100 * float(instance.abschlussgebuehren_prozent), 2)
    else:
        betrag = - float(instance.abschlussgebuehren_in_euro)
    buchung = Buchung(datum=instance.vertragsbeginn, betrag=betrag, art='ABSCHLUSSGEBUEHR', bausparvertrag=instance)
    buchung.save()


models.signals.post_save.connect(
    create_abschlussgebuehr_buchung,
    sender=Bausparvertrag,
    dispatch_uid='create_abschlussgebuehr_buchung')


def create_sparbeitrag_buchung(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return

    instance.status = "WIRD_AUSGEFUEHRT"
    instance.save()

    if instance.von_datum_inklusive > instance.bis_datum_inklusive:
        instance.status = 'ABGEBROCHEN'
        instance.save()
        return

    index = 0
    datum = instance.sparbeitrag.erste_buchung + relativedelta(months=index)
    while datum <= instance.bis_datum_inklusive:

        if instance.von_datum_inklusive <= datum <= instance.bis_datum_inklusive:
            buchung = Buchung(datum=datum,
                              betrag=instance.sparbeitrag.betrag,
                              art='SPARBEITRAG',
                              bausparvertrag=instance.sparbeitrag.bausparvertrag,
                              sparbetrag=instance.sparbeitrag)
            buchung.save()
        index += 1
        datum = instance.sparbeitrag.erste_buchung + relativedelta(months=index)
    instance.status = 'ERFOLGREICH'
    instance.save()


models.signals.post_save.connect(
    create_sparbeitrag_buchung,
    sender=SparbeitragJob,
    dispatch_uid='create_sparbeitrag_buchung')


