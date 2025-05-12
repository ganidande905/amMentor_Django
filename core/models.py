from django.db import models

class Mentor(models.Model):
    mentor_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    github = models.CharField(max_length=100)
    gitlab = models.CharField(max_length=100)
    pfp = models.URLField()
    def __str__(self):
        return self.mentor_name

class Mentee(models.Model):
    mentee_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    github = models.CharField(max_length=100)
    gitlab = models.CharField(max_length=100)
    pfp = models.URLField()
    @property
    def total_points(self):
        from django.db.models import Sum
        return self.submission_set.filter(accepted=True).aggregate(
        total=Sum('task__points')
    )['total'] or 0
    current_tracks = models.ForeignKey(
        'Track',
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'current_tracks'
    )
    badges = models.ManyToManyField('Badges', related_name='mentees', blank=True)
    mentors = models.ManyToManyField(Mentor, related_name ='mentees')
    def __str__(self):
        return self.mentee_name
    
class Badges(models.Model):
    badge_id = models.BigAutoField(primary_key=True)
    badge_name = models.CharField(max_length= 100)
    badge_description = models.CharField(max_length= 100)
    badge_image = models.URLField()
    def __str__(self):
        return self.badge_name
class Track(models.Model):
    track_id = models.BigAutoField(primary_key=True)
    track_name  = models.CharField(max_length=100)
    track_description = models.CharField(max_length=100)   
    def __str__(self):
        return f"{self.mentee_name} - {self.track_name}"    
    
class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_description = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    points = models.IntegerField()
    task_resources = models.CharField(max_length=100)
    task_status = models.CharField(max_length=100)
    track = models.ForeignKey( 
        'Track',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    def __str__(self):
        return f"{self.track.name} - {self.task_name}"

class Submission(models.Model):
    submission_id = models.BigAutoField(primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    submission_url = models.URLField()
    task_started = models.DateTimeField()
    task_ended = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    mentor_feedback = models.TextField(blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mentee.name} - {self.task.name}"

    
