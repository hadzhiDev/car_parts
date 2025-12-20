from django.db import models


class AnalyticsReport(models.Model):
    """Fake model to show analytics in admin"""
    
    class Meta:
        verbose_name = "Аналитический отчет"
        verbose_name_plural = "Аналитические отчеты"
        managed = False  # Don't create database table
        
    def __str__(self):
        return "Аналитический отчет"