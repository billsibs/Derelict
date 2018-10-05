from django.db import models

# Create your models here.

class gambitStats(models.Model):
    matchDate = models.DateField()
    matchId = models.IntegerField()
    guardianId = models.IntegerField()
    bankOverage = models.IntegerField()
    blockerKills = models.IntegerField()
    highValueKills = models.IntegerField()
    invaderDeaths = models.IntegerField()
    invaderKills = models.IntegerField()
    invasionKills = models.IntegerField()
    invasions = models.IntegerField()
    largeBlockersSent = models.IntegerField()
    mediumBlockersSent = models.IntegerField()
    mobKills = models.IntegerField()
    motesDegraded = models.IntegerField()
    motesDenied = models.IntegerField()
    motesDeposited = models.IntegerField()
    motesGenerated = models.IntegerField(default=0)
    motesLost = models.IntegerField()
    motesPickedUp = models.IntegerField()
    motesStolen = models.IntegerField(default=0)
    precisionKills = models.IntegerField()
    primevalDamage = models.IntegerField()
    primevalHealing = models.IntegerField()
    primevalKills = models.IntegerField()
    smallBlockersSent = models.IntegerField()
    weaponKillsAbility = models.IntegerField()
    weaponKillsGrenade = models.IntegerField()
    weaponKillsMelee = models.IntegerField()
    weaponKillsSuper = models.IntegerField()

class GuardianId(models.Model):
    guardianName = models.CharField(max_length=50)
    guardianId = models.IntegerField()
    active = models.BooleanField(default=False)

class GuardianClass(models.Model):
    guardianId = models.IntegerField()
    guardianClass = models.IntegerField()
    guardianClassId = models.IntegerField()