from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subdivisions', on_delete=models.CASCADE)  # Division can have no parent

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Division, related_name='districts', on_delete=models.CASCADE)  # District has a parent Division

    def __str__(self):
        return self.name


class Thana(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(District, related_name='thanas', on_delete=models.CASCADE)  # Thana has a parent District

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Thana, related_name='routes', on_delete=models.CASCADE)  # Route has a parent Thana

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Route, related_name='areas', on_delete=models.CASCADE)  # Area has a parent Route

    def __str__(self):
        return self.name

