from django.db import models

from accounts.models import User


# Create your models here.


class ElectionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Election(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ElectionType, on_delete=models.CASCADE, related_name='elections')
    year = models.CharField(max_length=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    nomination_deadline = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['year', 'name']


class SubElection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='sub_elections')
    winner = models.ForeignKey('Candidate', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='won_sub_elections')
    complete_votes = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.election.name}"

    class Meta:
        ordering = ['election', 'name']


class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidacies')
    sub_election = models.ForeignKey(SubElection, on_delete=models.CASCADE, related_name='candidates')
    nomination_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.sub_election.name}"

    @property
    def votes(self):
        return self.votes_set.count()

    class Meta:
        unique_together = ('user', 'sub_election')


class Vote(models.Model):
    sub_election = models.ForeignKey(SubElection, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    vote_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sub_election', 'voter')
        ordering = ['-vote_date']

    def __str__(self):
        return f"Vote by {self.voter.username} for {self.candidate.user.username} in {self.sub_election.name}"


class VoteStatus(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='vote_statuses')
    sub_election = models.ForeignKey(SubElection, on_delete=models.CASCADE, related_name='vote_statuses')
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Status for {self.candidate.user.username} in {self.sub_election.name} - {self.status}"

    class Meta:
        unique_together = ('candidate', 'sub_election')


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.election.name} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"


class EligibilityCriteria(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='eligibility_criteria')
    description = models.TextField()

    def __str__(self):
        return f"Eligibility Criteria for {self.election.name}"
