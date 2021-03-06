# Generated by Django 3.1.6 on 2021-02-14 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bausparvertrag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bausparkasse', models.CharField(max_length=255)),
                ('tarifname', models.CharField(max_length=255)),
                ('vertragsbeginn', models.DateField()),
                ('bausparsumme_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3)),
                ('bausparsumme', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=14)),
                ('abschlussgebuehren_prozent', models.FloatField(blank=True, null=True)),
                ('abschlussgebuehren_in_euro_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3)),
                ('abschlussgebuehren_in_euro', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='EUR', max_digits=14, null=True)),
                ('laufende_gebuehren_in_euro_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3)),
                ('laufende_gebuehren_in_euro', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=14)),
                ('laufende_gebuehren_zeitraum', models.CharField(choices=[('JAEHRLICH', 'jährlich'), ('HALBJAEHRLICH', 'halbjährlich'), ('VIERTELJAEHRLICH', 'vierteljährlich'), ('MONATLICH', 'monatlich'), ('EINMALIG', 'einmalig')], max_length=16)),
                ('zinsen_ansparphase', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bausparvertraege', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bausparverträge',
            },
        ),
        migrations.CreateModel(
            name='Sparbeitrag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('betrag_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3)),
                ('betrag', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=14)),
                ('erste_buchung', models.DateField()),
                ('letzte_buchung', models.DateField(blank=True, null=True)),
                ('bausparvertrag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sparbeitraege', to='bauspartrackerapp.bausparvertrag')),
            ],
            options={
                'verbose_name_plural': 'Sparbeiträge',
            },
        ),
        migrations.CreateModel(
            name='SparbeitragJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('von_datum_inklusive', models.DateField()),
                ('bis_datum_inklusive', models.DateField()),
                ('status', models.CharField(choices=[('GEPLANT', 'geplant'), ('WIRD_AUSGEFUEHRT', 'wird ausgeführt'), ('ERFOLGREICH_ABGESCHLOSSEN', 'erfolgreich abgeschlossen'), ('ABGEBROCHEN', 'abgebrochen')], max_length=25)),
                ('sparbeitrag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='bauspartrackerapp.sparbeitrag')),
            ],
        ),
        migrations.CreateModel(
            name='Buchung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('betrag_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3)),
                ('betrag', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=14)),
                ('art', models.CharField(choices=[('ABSCHLUSSGEBUEHR', 'Abschlussgebühr'), ('LAUFENDE_GEBUEHR', 'Laufende Gebühr'), ('SPARBEITRAG', 'Sparbeitrag')], max_length=16)),
                ('bausparvertrag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buchungen', to='bauspartrackerapp.bausparvertrag')),
                ('sparbetrag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buchungen', to='bauspartrackerapp.sparbeitrag')),
            ],
            options={
                'verbose_name_plural': 'Buchungen',
            },
        ),
    ]
