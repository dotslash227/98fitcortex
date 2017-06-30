from .bmi import BMI
from .lean import LeanFactor
from .bodyTypes import BodyTypes
from .bmr import BasalMetabolicRate
from .tdee import TDEE
from .goals import Goals
from . import meals
from .calorieNumber import CalorieNumber
from .ibw import IBW
from .medical_conditions import Osteoporosis , Anemia
from knapsack.knapsack_dp import knapsack
import itertools , threading , lego

class Calculations:
	@lego.assemble
	def __init__(self , weight , height , activity , goal , gender,  exclude , disease = None , exclusion_conditions = None , exclude2 = None):
		#calculations
		self.bmi = BMI(weight , height)
		self.ibw = IBW(self.height, self.gender)
		self.calorieNumber = CalorieNumber(self.bmi , self.activity)
		self.countCalories()
		# self.exclude += [e.name for e in Food.objects.filter(self.exclusion_conditions)]


	def countCalories(self):
		# import ipdb
		# ipdb.set_trace()
		self.calories = max( 1200 , self.ibw.ibw * self.calorieNumber.number)
		return self

	def makeMeals(self):
		self.m5 = meals.M5(self.calories ,
			 self.goal ,
			 exclude = self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions,
			 exclude2 = self.exclude2
		)
		self.m5.build()
		
		self.m3 = meals.M3(
			self.calories , 
			self.goal , 
			exclude = self.exclude + [e.name for e in self.m5.selected] , 
			extra = self.m5.calories_remaining , 
			disease = self.disease , 
			exclusion_conditions = self.exclusion_conditions,
			make_combination = hasattr(self.m5, "combination"),
			exclude2 = self.exclude2
		)
		self.m3.build()
		
		self.m1 = meals.M1(
			self.calories , 
			self.goal , 
			exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected], 
			extra = self.m3.calories_remaining, 
			disease = self.disease, 
			exclusion_conditions = self.exclusion_conditions
		)
		self.m1.build()
		self.m4 = meals.M4(
			self.calories ,
			self.goal ,
			exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected+self.m1.selected],
			extra = self.m1.calories_remaining ,
			disease = self.disease ,
			exclusion_conditions = self.exclusion_conditions)
		self.m4.build()
		self.m2 = meals.M2(self.calories ,
			self.goal ,
			exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected+self.m1.selected+self.m4.selected],
			extra = self.m4.calories_remaining ,
			disease = self.disease ,
			exclusion_conditions = self.exclusion_conditions)
		self.m2.build()
		
		self.meals = [
			self.m1 , self.m2 , self.m3 , self.m4 , self.m5
		]

	@property
	def selected(self):
		return list(itertools.chain(*[self.m1.selected, self.m3.selected , self.m5.selected , self.m4.selected , self.m2.selected]))

	@property
	def protein(self):
		return self.sum_property("protein")

	@property
	def carbs(self):
		return self.sum_property("carbohydrates")

	@property
	def fat(self):
		return self.sum_property("fat")

	@property
	def calories_achieved(self):
		return self.m1.calories + self.m3.calories + self.m5.calories + self.m2.calories + self.m4.calories

	@property
	def protein_ideal(self):
		return (self.goal.protein * self.calories)/4

	@property
	def carbs_ideal(self):
		return (self.goal.carbs * self.calories) / 4

	@property
	def fat_ideal(self):
		return (self.goal.fat * self.calories) /  9

	@property
	def random(self):
		return [e.name for e in self.m1.random() +self.m2.random() +self.m3.random() +self.m4.random() +self.m5.random()] 

	@property
	def calcium(self):
		cal =  self.sum_property("calcium")
		if self.disease == Osteoporosis:
			return cal + 125
		return cal

	def sum_property(self , property):
		return sum([
			getattr(e , property) for e in self.selected
		])

	@property
	def iron(self):
		return self.sum_property("iron")

	@property
	def vitaminc(self):
		return self.sum_property("vitaminc")

	def makeMeal(self , meal = None):
		assert meal
		m = getattr(meals , meal.upper())
		m = m(self.calories , self.goal)
		setattr(self , meal , m )
		m.build()
		return m