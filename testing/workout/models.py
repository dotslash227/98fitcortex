#Contains Exercise Tables

from django.db import models
from epilogue.models import *
from workoutplan import levels

import isoweek

# Create your models here.

class BaseExercise():

    @property
    def module_name(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        return "%s : %s"%(str(self.workout_name) , getattr(self  , "exercise_level" , "None"))

    def __str__(self):
        return self.workout_name

class CardioFloorExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length=250, blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    _duration = models.IntegerField( default = 0, db_column = "duration")
    swing1 = models.BooleanField(default = True)
    home = models.BooleanField(default = True)
    gym = models.BooleanField(default = True)
    machine_required = models.BooleanField(default = True)
    machine_name = models.CharField(max_length=250, blank=True, null=True)
    exercise_level = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    image_name = models.CharField(max_length=250, blank=True, null=True)

    @property
    def duration(self):
        if self.swing1:
            return self._duration * 2
        return self._duration

class CardioTimeBasedExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length=250, blank=True, null=True)
    duration = models.IntegerField( blank=True, null=True)
    home = models.BooleanField(default = True)
    gym = models.BooleanField(default = True)
    machine_required = models.BooleanField(default = True)
    machine_required_home = models.CharField(max_length=250, blank=True, null=True)
    machine_required_gym = models.CharField(max_length=250, blank=True, null=True)
    exercise_level = models.CharField(max_length=50, blank=True, null=True)
    functional_warmup = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=True,default = 1)
    image_name = models.CharField(max_length=100, blank=True, null=True)

    @property
    def machine_name(self):
        if self.home:
            return self.machine_required_home
        elif self.gym:
            return self.machine_required_gym

class NoviceCoreStrengthiningExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length=250)
    reps = models.CharField(max_length=50)
    _duration = models.IntegerField(default=0, db_column = "duration")
    hold = models.BooleanField(default = False)
    swing1 = models.BooleanField(default = False)
    rotation = models.BooleanField()
    swing2 = models.BooleanField(default = False)
    sets = models.IntegerField()
    home = models.BooleanField(default = True)
    gym = models.BooleanField(default = True)
    machine_required = models.BooleanField(default = True)
    machine_name = models.CharField(max_length=100, blank=True, null=True)
    exercise_level = models.CharField(max_length=100, blank=True, null=True)
    muscle_group_cat = models.CharField(max_length=100, blank=True, null=True)
    muscle_group_name = models.CharField(max_length=100, blank=True, null=True)
    body_part = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    image_name = models.CharField(max_length=200, blank=True, null=True)

    @property
    def duration(self):
        multiplier = 0
        if self.swing1 == 1:
            multiplier += 1
        if self.swing2 == 1:
            multiplier += 1
        if self.rotation == 1:
            multiplier += 2

        if multiplier == 0:
            return self._duration
        return self._duration * multiplier



class ResistanceTrainingExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length = 100,blank=True, null=True)
    exercise_group = models.CharField(max_length = 30,blank=True, null=True)
    left_right = models.BooleanField(default = True)
    home = models.BooleanField(default = True)
    gym = models.BooleanField(default = True)
    eqip_name_home = models.CharField(max_length = 100,blank=True, null=True)
    machine_required = models.BooleanField(default = True)
    machine_name = models.CharField(max_length = 100,blank=True, null=True)
    exercise_level = models.CharField(max_length  =10,blank=True, null=True)
    muscle_group_cat = models.CharField(max_length = 100,blank=True, null=True)
    muscle_group_name = models.CharField(max_length = 100,blank=True, null=True)
    sub_muscle_group = models.CharField(max_length = 30,blank=True, null=True)
    body_part = models.CharField(max_length = 30,blank=True, null=True)
    exercise_type = models.CharField(max_length = 100,blank=True, null=True)
    status = models.IntegerField(default = 1)
    image_name = models.CharField(max_length = 50,blank=True, null=True)


class StretchingExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length=250, blank=True, null=True)
    swing1 = models.BooleanField(default = True)
    home = models.BooleanField(default = True)
    gym = models.BooleanField(default = True)
    machine_required = models.BooleanField(default = True)
    machine_name = models.CharField(max_length=250, blank=True, null=True)
    muscle_group_cat = models.CharField(max_length=250, blank=True, null=True)
    sub_muscle_group_name = models.CharField(max_length=250, blank=True, null=True)
    muscle_group_name = models.CharField(max_length=250, blank=True, null=True)
    body_part = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    image_name = models.CharField(max_length=250, blank=True, null=True)


class WarmupCoolDownMobilityDrillExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length = 100)
    _duration = models.IntegerField(default = 0 , db_column = "duration")
    reps = models.IntegerField(default = 0)
    swing1 = models.BooleanField(default = False)
    rotation = models.BooleanField(default = False)
    swing2 = models.BooleanField(default = False)
    home  = models.BooleanField(default = True)
    gym  = models.BooleanField(default = True)
    machine_required  = models.BooleanField(default = True)
    machine_name = models.CharField(max_length = 100, blank=True, null=True)
    exercise_level = models.CharField(max_length = 30, blank=True, null=True)
    joint_name = models.CharField(max_length = 50, blank=True, null=True)
    body_part = models.CharField(max_length = 50, blank=True, null=True)
    muscle_group_name = models.CharField(max_length = 100, blank=True, null=True)
    description = models.CharField(max_length = 255, blank=True, null=True)
    status = models.IntegerField(default = 0)
    image_name = models.CharField(max_length = 50, blank=True, null=True)

    @property
    def duration(self):
        multiplier = 0
        if self.swing1 == 1:
            multiplier += 2
        if self.swing2 == 1:
            multiplier += 2
        if self.rotation == 1:
            multiplier += 2

        if multiplier == 0:
            return self._duration
        return self._duration * multiplier


class WarmupCoolDownTimeBasedExercise(BaseExercise,models.Model):
    workout_name = models.CharField(max_length = 100)
    duration = models.IntegerField()
    total_time = models.IntegerField()
    time_unit = models.CharField(max_length = 10 , default = "secs")
    machine_required  = models.BooleanField()
    machine_name = models.CharField(max_length = 100)
    exercise_level = models.CharField(max_length = 30)
    muscle_group = models.CharField(max_length = 50)
    body_part = models.CharField(max_length = 50)
    status = models.IntegerField()
    home  = models.BooleanField()
    gym  = models.BooleanField()


class GeneratedExercisePlan(models.Model):
    class Meta:
        db_table = "erp_exercise_plan"

    created_on = models.DateTimeField(auto_now_add = True)
    year = models.IntegerField()
    customer = models.ForeignKey(Customer , related_name = "workouts", db_column = "erp_customer_id" , on_delete = models.CASCADE)
    user_week_id = models.IntegerField()
    week_id = models.IntegerField()
    level = models.IntegerField(default = 1, db_column = "glo_level_id")
    lifestyle = models.FloatField(default = 1.2, db_column = "life_style")

    @property
    def level_obj(self):
        level = self.glo_level_id

        if level == 1:
            return levels.Novice
        elif level == 2:
            return levels.Beginner
        elif level == 3:
            return levels.Intermediate

        return levels.Novice
    
    @property
    def activity(self):
       return self.lifestyle 
    
    @property
    def monday(self):
        return isoweek.Week(self.year, self.week_id)

class GeneratedExercisePlanDetails(models.Model):
    class Meta:
        db_table = "erp_exercise_plan_detail"
    description = models.CharField(default = '' , max_length = 225)
    workoutplan = models.ForeignKey(GeneratedExercisePlan , related_name = "exercises", db_column = "erp_exercise_plan_id" , on_delete = models.CASCADE)
    day = models.IntegerField()
    exercise_type = models.IntegerField()
    workout_name = models.CharField(max_length = 100)
    time = models.CharField(max_length = 50)
    reps = models.CharField(max_length=50)
    sets = models.CharField(max_length=50)
    machine_name = models.CharField(max_length=50)
    equipment_name = models.CharField(max_length=50)
    mod_name = models.CharField(max_length = 30)
    mod_id = models.IntegerField()
    muscle_group = models.CharField(default = '', max_length = 20)
    exercise_level = models.CharField(default = "" , max_length = 20)
    image = models.URLField(default = "http://www.98fit.com/webroot/workout_images/workout_blank.jpg")

class CustomerInjury(models.Model):
    class Meta:
        db_table = "erp_customer_injury"
    injury_name = models.CharField(max_length = 20)
    customer = models.ForeignKey(Customer , db_column = "erp_customer_id" , related_name = "injuries" , on_delete = models.CASCADE)

    def __str__(self):
        return self.injury_name

