from epilogue.models import Food , GeneratedDietPlan
from .utils import annotate_food , mark_squared_diff
from .goals import Goals
from .medical_conditions import Osteoporosis , Anemia
from knapsack.knapsack_dp import knapsack,display
import heapq ,  re , random , ipdb , math
from numpy.random import choice
from epilogue.manipulation.manipulator import Manipulator
from dietplan.categorizer.categorizers import *
from django.db.models import Q
from random import sample

class CerealTreeSelector():
    
    def cerealReplacer(self):
        self.getCerealFromSelected()
        extra_filter = Q()
        if self.cereal.non_veg == 1:
            extra_filter &= Q(non_veg = 1)
        if self.cereal.vegetables == 1:
            extra_filter &= Q(vegetables = 1)
        if self.cereal.pulse == 1:
            extra_filter &= Q(pulse = 1)
        self.select_cereals(extra_filter = extra_filter)
        return self
    
    def pulseReplacer(self):
        self.getCerealFromSelected()    
        extra_filter = Q()
        if self.cereal.non_veg == 1:
            extra_filter &= Q(non_veg_gravy_items = 1) & Q(vegetable = 1)
        elif self.cereal.vegetables ==1 and self.cereal.pulse == 0:
            extra_filter &= Q(pulse = 1)
        elif self.cereal.vegetables == 0 and self.cereal.pulse == 1:
            extra_filter &= Q(vegetables = 1)
        calories = self.calories_goal - self.cereal.calorie
        if self.selected.get('yogurt'):
            yogurt = self.selected['yogurt']
            calories -= yogurt.calorie
        else:
            dessert = self.selected.get('dessert')
            if dessert:
                calories -= dessert.calorie 
        self.select_pulses(calories = calories , extra_filter = extra_filter)
        return self
    
    def getCerealFromSelected(self):
        self.cereal = self.selected.get('cereal')
        if not self.cereal:
            self.cereal = self.selected.get('cereals')
        if not self.cereal:
            self.cereal = self.selected.get('grains_cereals')


class Base:
    '''
    Base class for Meal classes to inherit from.
    Provides basic method wrappers
    '''
    fieldMapper = {
        Goals.WeightLoss : "squared_diff_weight_loss",
        Goals.MaintainWeight : "squared_diff_weight_maintain",
        Goals.WeightGain : "squared_diff_weight_gain",
        Goals.MuscleGain : "squared_diff_muscle_gain"
    }

    def get_steps(self , item):
        '''
        Returns the steps of 5 calories needed to reach the calories
        '''
        difference = self.calories_goal - self.calories
        unit = item.calarie/(5*item.weight)
        steps = round(difference/unit)
        return steps

    def get_steps_quantity(self,item):
        '''
        Returns the steps of item's quantity required to reach the calories
        '''
        print("Calories Goal",self.calories_goal)
        print("Calories Remaining", self.calories)
        difference = self.calories_goal - self.calories
        unit = item.calarie/item.quantity
        steps = round(difference/unit)
        return steps

    @property
    def calories(self):
        '''
        Return the summed calories of the selected items
        '''
        return sum([i.calorie for i in self.selected.values()])

    @property
    def calories_remaining(self):
        '''
        Return the calories required to achieve the calories goal
        '''
        return self.calories_goal - self.calories

    @property
    def protein_ideal(self):
        '''
        Return the ideal protein required 
        '''
        return (self.goal.protein * self.calories_goal) / 4

    @property
    def carbs_ideal(self):
        '''
        Return the ideal carbs required
        '''
        return (self.goal.carbs * self.calories_goal) / 4

    @property
    def fat_ideal(self):
        '''
        Return the ideal fats required
        '''
        return (self.goal.fat * self.calories_goal ) / 9

    @property
    def protein(self):
        '''
        Return the summed protein from the selected items
        '''
        return sum([i.protein for i in self.selected.values()])

    @property
    def fat(self):
        '''
        Return the summed fat from the selected items
        '''
        return sum([i.fat for i in self.selected.values()])

    @property
    def carbs(self):
        '''
        Return the summed carbs from the selected items
        '''
        return sum([i.carbohydrates for i in self.selected.values()])


    def random(self):
        return random.sample(self.for_random , min(2,len(self.selected.values())))

    @property
    def for_random(self):
        return self.selected

    def get_best(self, select_from , calories , name):
        '''
        Get the item that best suits the calories and nutritional value
        using Knapsack algorithm
        '''
        F,test = knapsack(select_from, calories , self.fieldMapper.get(self.goal) )
        a = [select_from[i] for i in display(F , calories , select_from)]
        setattr(self , name + "_options" , a)
        return a
    
    def get_best_minimum(self , select_from , calories , name):
        '''
        Get the item having minimum penalty with respect to the goal
        '''
        return min(
            self.get_best(select_from , calories , name),
            key = lambda x : getattr(x , self.fieldMapper.get(self.goal))
        )

    def select_best_minimum(self , select_from , calories , name):
        '''
        Get the best item
        '''
        try:
            i = self.get_best_minimum(select_from , calories , name)
        except Exception as e:
            print("Some MF _____" , e)
            i = min(select_from , key = lambda x : abs(calories - x.calorie) )
        else:
            i = min(select_from , key = lambda x : abs(calories - x.calorie))
        finally:
            self.select_item(i , name)
            return i

    def select_item(self , item , key , remove = True):
        '''
        Add the `item` to self.selected 
        '''
        if item is None:
            return
        self.selected.update({
            key : item
        })
        if remove:
            self.marked.exclude(id = item.id)
        return item

    def unselect_item(self , item , append = True):
        '''
        Remove the item from self.selected
        '''
        self.selected.remove(item)
        if append:
            self.selected.append(item)
        return self

    def select_items(self , *items):
        '''
        Add the given `items` to self.selected
        '''
        [self.select_item(e) for e in items]
        return self

    def rethink(self):
        '''
        Rethink the diet plan
        '''
        for item in self.selected.values():
            if self.calories < self.calories_goal:
                if "Parantha" in item.name or "Roti" in item.name or "Cheela" in item.name:
                    if item.quantity < 2:
                        item.update_quantity(2)
                elif "Tea" not in item.name or "Coffee" not in item.name and not bool(item.yogurt):
                    item.update_weight(1.5)

    def build(self):
        '''
        Build the diet plan
        '''
        if self.disease is not None:
            pass

    def __getitem__(self , key):
        return self.selected[key]

class M1(Base):
    '''
    Breakfast Generation
    '''
    percent = .25

    def __init__(self , calories , goal , exclude=  "" , extra = 0 , disease = None , exclusion_conditions = Q() , selected = None):
        self.calories_goal = calories*self.percent + extra
        self.goal = goal
        self.exclude = exclude
        self.disease = disease
        self.exclusion_conditions = exclusion_conditions
        self.queryset = Food.m1_objects.exclude(name__in = exclude)
        self.queryset = self.queryset.filter(self.exclusion_conditions)

        if goal == Goals.WeightLoss : 
            self.queryset = self.queryset.filter(for_loss = '1').all()
        
        if self.disease and hasattr(self.disease , "queryset_filter"): 
            self.queryset = self.queryset.filter(self.disease.queryset_filter)      
        
        self.marked = self.queryset
        self.selected = selected
        
        #buildMapper is required for replacement
        self.buildMapper = {
            'snack' : self.select_snack,
            'drink' : self.select_drink
        }
        backwardMapper ={
            'snaks' : self.select_snack,
            'pulses' : self.select_snack
        }
        self.buildMapper.update(backwardMapper)

    def allocate_restrictions(self):
        '''
        Allocate Breakfast necessary restrictions
        1. Allocate a drink
        2. Allocate Egg 
        '''
        self.drink = self.select_item(self.get_drink() , "drink")
        self.remove_drinks()

        if  ('egg' , 0) not in self.exclusion_conditions.children and not hasattr(self,"egg"):
            self.egg = Food.m1_objects.filter(name = "Boiled Egg White").first()
            self.select_item(self.egg , "egg" ,remove = False)

    def get_drink(self):
        
        #Get the list from which drink is to be selected
        self.drink_list = self.marked.filter(drink = '1').filter(size = "Teacup")
        
        #If the user does not want dairy, remove all dairy items from drink list
        if ('dairy',0) not in self.exclusion_conditions.children:
            self.drink_list = self.drink_list.filter(dairy = '1')

        if not self.drink_list.count():
            return
        
        #Get multiple sizes/portions for drinks
        m = Manipulator(items = self.drink_list , categorizers = [DrinkCategoriser])
        self.drink_list = m.categorize().get_final_list()

        return min(self.drink_list , key = lambda x : abs(self.calories_goal * 0.15 - x.calorie))

    def select_drink(self):
        self.select_item(self.get_drink() , "drink")

    def remove_drinks(self):
        # self.marked = list(set(self.marked) - set(self.drink_list))
        self.marked = self.marked.exclude(name__in = [e.name for e in self.drink_list])
        return self

    def rethink(self):
        print("Running M1 rethink")
        selected = self.snack
        if self.calories_remaining > 0 and isinstance(selected, Food):  
            if "Roti" in selected.name or "Dosa" in selected.name or "Cheela" in selected.name or "Bun" in selected.name:
                steps = math.floor(self.calories_remaining * selected.quantity/(selected.calarie))
                new_quantity = steps + selected.quantity
                selected.update_quantity(new_quantity/selected.quantity)
            else:
                print("Updatin " , selected , selected.weight)
                steps = math.floor(self.calories_remaining * selected.weight/(selected.calarie*10))
                new_weight =  selected.weight + steps * 10
                selected.update_weight(new_weight/selected.weight)
                print("New weight" , selected.weight)
    
    def select_snack(self):
        '''
        Select a snack for breakfast
        '''
        calories = self.calories_goal
        
        #if dairy is not excluded by user, only allocated 85% of calories to snack
        if ("dairy",0) not in self.exclusion_conditions:
            calories *= 0.85

        food_list = self.marked.filter(snaks = '1').filter(dairy = 0)

        #if egg has been allocated, deduct 36 calories from the snack calories
        if not ("egg",0) in self.exclusion_conditions.children:
            food_list = food_list.exclude(egg = 1   )
            calories -= 36
        
        #Get multiple sizes/portions of items
        m = Manipulator(items = food_list , categorizers = [ParanthaCategoriser])
        food_list = m.categorize().get_final_list()
        
        #Select the best item
        self.snack = self.select_best_minimum(food_list , calories , name = "snack")
         
    def build(self):
        '''
        Build the breakfast
        '''
        self.allocate_restrictions()
        self.select_snack()

        #If breakfast does not have sufficient protein, add more eggs
        if self.protein_ideal - self.protein > 8 and hasattr(self , "egg"):
            self.egg.update_quantity(1.5)
        #self.rethink()
        return self


class M2(Base):
    '''
    Generate the Mid day Snack
    '''
    percent = 0.15

    def __init__(self , calories , goal , exclude , extra = 0 , disease = None , exclusion_conditions = None , selected = None):
        self.calories_goal = calories*self.percent + extra
        self.goal = goal
        self.exclude = exclude
        self.queryset = self.getDefaultQueryset().exclude(name__in = exclude)

        if self.goal == Goals.WeightLoss:
            self.queryset = self.queryset.filter(for_loss = 1)

        self.marked = self.queryset
        self.selected = selected
        self.exclusion_conditions = exclusion_conditions

        if self.exclusion_conditions : 
            self.queryset = self.queryset.filter(self.exclusion_conditions)

        self.buildMapper = {
            'nut' : self.select_nut,
            'salad' : self.select_salad,
            'fruit' : self.select_fruit,
            'snack' : self.select_snacks
        }
        backwardMapper = {
            'fruits' : self.select_fruit,
            'nuts' : self.select_nut,
            'pulses' : self.select_snacks,
            'snaks' : self.select_snacks
        }
        self.buildMapper.update(backwardMapper)

    def getDefaultQueryset(self):
        return Food.m2_objects

    def select_fruit(self):
        self.option = "fruit"
        calories = self.calories_goal
        fruit_items = Food.m2_objects.filter(fruit= 1)
        try:
            self.fruit = self.select_best_minimum(fruit_items , calories , name = "fruit")
        except Exception as e:
            print("From M2 Fruit " , e)
            self.fruit = random.choice(fruit_items)
            self.select_item(self.fruits , "fruits")

    def select_salad(self):
        self.option = "salad"
        calories = self.calories_goal
        salad_items = self.marked.filter(salad = 1)
        try:
            self.salad = self.select_best_minimum(salad_items , calories , name = "salad")
        except Exception as e:
            self.salad = random.choice(salad_items)
            self.select_item(self.salad , "salad")

    def select_nut(self):
        self.option = "nut"
        calories = self.calories_goal
        nuts_items = self.marked.filter(Q(name__startswith = "Handful")).all()
        if not nuts_items.count():
            nuts_items = self.getDefaultQueryset().filter(Q(name__startswith = "Handful"))
        try:
            self.nuts = self.select_best_minimum(nuts_items , calories , name = "nuts")
        except Exception as e:
            # ipdb.set_trace()
            self.nuts = random.choice(nuts_items)
            self.select_item(self.nuts , "nuts")

    def select_snacks(self):
        '''
        Select a snack
        '''
        self.option = "snack"
        calories = self.calories_goal
        snack_items = self.marked.filter(snaks = 1)
        try:
            self.snack = self.select_best_minimum(snack_items , calories , name = "snack")
        except Exception as e: #Exception generally occurs when the a suitable item is not available
            self.snack = random.choice(snack_items)
            self.select_item(self.snack , "snack")

    def get_probability(self):
        '''
        Return the probability distribution through which fruits and nuts
        need to be selected
        '''
        if ('nuts' , 0) in self.exclusion_conditions.children:
            return [1,0] # select fruit with probability 1 and nuts with 0

        return [0.5,0.5]

    def build(self):
        '''
        Build the Mid day snack
        '''

        #Select fruits in case user does not want nuts
        if ('nuts' , 0) in self.exclusion_conditions.children:
            self.select_fruit()
        else:
            #Select fruit or nut with equal probability
            self.choice = choice([self.select_fruit , self.select_nut],
                size = 1,
                p = [0.5 , 0.5]
            )[0]
            self.choice()
        return self


class M3(Base , CerealTreeSelector):
    '''
    Generate Lunch
    '''
    percent = 0.25

    def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , make_combination = False , make_dessert = False ,  exclude2 = None , selected = None):
        self.calories_goal = calories*self.percent + extra
        self.extra = extra
        self.goal = goal
        self.disease = disease
        self.exclude2 = exclude2
        self.selected = selected
        self.queryset = self.getQuerysetFromGoal().exclude(name__in = exclude)
        self.exclude = exclude
        if self.goal == Goals.WeightLoss:
            self.queryset = self.queryset.filter(for_loss = 1)

        if self.disease:
            self.queryset = self.queryset.filter(self.disease.queryset_filter)

        self.exclusion_conditions = exclusion_conditions
        self.queryset = self.queryset.filter(exclusion_conditions)
        self.marked = self.queryset
        self.make_combination = make_combination
        self.make_dessert = make_dessert
        self.isYogurt = False

        self.buildMapper = {
            'yogurt' : self.select_yogurt,
            'dessert' : self.select_dessert,
            'vegetable' : self.select_vegetables,
            'pulse' : self.pulseReplacer,
            'cereal' : self.cerealReplacer,
            'combination' : self.makeCombinations
        }
        backwardMapper = {
            'cereals' : self.cerealReplacer,
            'grains_cereals' : self.cerealReplacer,
            'pulses' : self.cerealReplacer,
        }
        self.buildMapper.update(backwardMapper)

    def getQuerysetFromGoal(self):
        '''
        Return default queryset for this meal
        '''
        f = Food.m3_objects
        if self.goal == Goals.WeightLoss:
            f = f.filter(for_loss = 1)
        return f

    def select_yogurt(self):
        self.isYogurt = True
        calories = 0.15*self.calories_goal
        food_list = self.marked.filter(yogurt = 1)
        food_list = food_list.filter(self.exclusion_conditions)
        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(yogurt = 1)
        m = Manipulator(items = food_list , categorizers = [YogurtCategoriser])
        food_list = m.categorize().get_final_list()
        # ipdb.set_trace()
        self.yogurts = self.select_best_minimum(food_list , calories , name="yogurt")
        
        if isinstance(self.yogurts , Food):
            steps = round( (calories - self.yogurts.calorie) * self.yogurts.weight/(self.yogurts.calorie*10))
            new_weight = min(250,self.yogurts.weight + steps * 10)
            self.yogurts.update_weight(new_weight/self.yogurts.weight)

    def select_dessert(self):
        self.isYogurt = False
        calories = 0.12*self.calories_goal
        food_list = self.marked.filter(dessert = 1)
        self.dessert = self.select_best_minimum(food_list , calories , name = "dessert")

    def select_vegetables(self , calories = None):
        if self.isYogurt : 
            percent = 0.25
        else:
            percent = 0.18
        
        if not calories:
            calories = percent * self.calories_goal

        food_list = self.marked.filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")

        if self.disease and hasattr(self.disease , "vegetable_filter"):
            food_list = food_list.filter(self.disease.vegetable_filter)

        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic").filter(extra_filter)

        m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
        food_list = m.categorize().get_final_list()

        self.vegetable = self.select_best_minimum(food_list , calories , "vegetable")
        
        if isinstance(self.vegetable , Food):
            steps = round((calories - self.vegetable.calarie ) * self.vegetable.weight/(self.vegetable.calarie*10))
            new_weight = min(250,self.vegetable.weight + steps * 10)
            self.vegetable.update_weight(new_weight/self.vegetable.weight)


    def select_cereals(self , percent = 0.37,extra_filter = Q()):       
        calories = percent * self.calories_goal
        
        if self.exclude2:
            food_list = self.getQuerysetFromGoal().exclude(name__in = self.exclude2).filter(grains_cereals = 1)
            food_list = food_list.filter(self.exclusion_conditions)
        else:
            food_list = self.marked.filter(grains_cereals = 1)
            food_list = food_list.filter(self.exclusion_conditions)
        
        food_list = food_list.filter(cuisine = "Generic").filter(extra_filter)
        # ipdb.set_trace()
        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(grains_cereals = 1).exclude(name__in = self.exclude[len(self.exclude)//2:])
            food_list = food_list.filter(self.exclusion_conditions).filter(extra_filter)
        m = Manipulator(items = food_list , categorizers = [GrainsCerealsCategoriser])
        food_list = m.categorize().get_final_list()
        print("Selecting Cereals")
        self.cereal = self.select_best_minimum(food_list , calories , "cereals")
        
    def select_pulses(self , calories = None , extra_filter = Q()):
        if self.isYogurt : 
            percent = 0.23
        else:
            percent = 0.18
        
        if not calories:
            calories = percent * self.calories_goal
        else:
            calories = calories
        
        food_list = self.marked.filter(pulses = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
        food_list = food_list.filter(extra_filter)
        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(pulses = 1).filter(grains_cereals = 0).filter(cuisine = "Generic").filter(self.exclusion_conditions).filter(extra_filter)
        m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
        food_list = m.categorize().get_final_list()
        try:
            self.pulses = self.select_best_minimum(food_list , calories , "pulse")
        except Exception as e:
            self.pulses = min(food_list , key = lambda x : abs(calories - x.calarie))
            self.select_item(self.pulses , "pulse")

    def makeGeneric(self):
        self.select_cereals()

        if self.cereal.non_veg == 1:
            self.select_pulses(calories = self.calories_remaining , extra_filter =  Q(vegetables = 1))
            return self

        #Already Implemented
        if self.cereal.vegetables == 1 and self.cereal.pulse == 0:
            self.select_pulses(calories = self.calories_remaining , extra_filter = Q(pulse = 1))
        
        elif self.cereal.vegetables == 0 and self.cereal.pulse == 1:
            self.select_pulses(calories = self.calories_remaining , extra_filter = Q(vegetables = 1))
        
        #Already Implemented
        elif self.cereal.vegetables == 1 and self.cereal.pulse == 1:
            self.select_pulses(calories = self.calories_remaining)

        if self.cereal.vegetables == 0 and self.cereal.pulse == 0:
            self.select_pulses()
            self.select_vegetables()    
        return self

    def makeCombinations(self):
        calories = self.calories_remaining

        if self.make_dessert:
            calories *= 0.88
        else:
            calories *= 0.85

        food_list = self.marked.filter(cuisine = "Combination")
        m = Manipulator(items = food_list , categorizers = [CombinationCategoriser])
        food_list = m.categorize().get_final_list()
        self.combination = self.select_best_minimum(food_list , calories , name = "combination")

    def rethink(self):
        if self.calories < self.calories_goal:
            if hasattr(self,"combination"):
                selected = self.combination
            elif hasattr(self , "pulses" ):
                selected = self.pulses
            elif hasattr(self , "vegetables"):
                selected = self.vegetables
            try:
                new_weight = min(200,selected.weight +  self.get_steps(selected)*5) 
            except Exception as e:
                # ipdb.set_trace()
                pass
            selected.update_weight(new_weight/selected.weight)

    def build(self):
        '''
        Build M3
        '''
        if self.make_dessert:
            self.select_dessert()

        elif ('dairy' , 0) not in self.exclusion_conditions.children:
            self.select_yogurt()
        
        if self.make_combination:
            self.makeCombinations()
        else:
            self.makeGeneric()
        
        return self

    @property
    def for_random(self):
        return list(filter( lambda x : not bool(x.dessert) , self.selected))

class M4(Base):
    percent = 0.15


    def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , selected = None):
        self.calories_goal = calories*self.percent + extra
        self.goal = goal
        self.exclusion_conditions = exclusion_conditions 
        self.queryset = Food.m4_objects.exclude(name__in = exclude)

        if self.goal == Goals.WeightLoss:
            self.queryset = self.queryset.filter(for_loss = 1)

        if exclusion_conditions : 
            self.queryset = self.queryset.filter(exclusion_conditions)
        
        self.exclude = exclude
        self.disease = disease
        self.marked = self.queryset
        if disease :
            self.marked = disease.get_queryset(self.queryset)
        self.selected = selected
        self.buildMapper = {
            'drink' : self.select_drink,
            'fruit' : self.get_random_item,
            'salad' : self.get_random_item,
            'nuts'  : self.get_random_item,
            'snack' : self.get_random_item
        }
        backwardMapper = {
            'pulses' : self.get_random_item,
            'snacks' : self.get_random_item,
            'snaks' : self.get_random_item
        }
        self.buildMapper.update(backwardMapper)

    def select_drink(self):
        calories = 0.15*self.calories_goal
        food_list = self.marked.filter(drink = 1)
        m = Manipulator(items = food_list , categorizers=[DrinkCategoriser])
        food_list = m.categorize().get_final_list()
        if self.disease == Osteoporosis:
            food_list.filter(Q(name__contains = "Lassi"))
        try:
            self.drink = self.select_best_minimum(food_list , calories , "drink")
        except Exception as e:
            self.drink = random.choice(food_list)
            self.select_item(self.drink , "drink")

    def select_fruit(self , calories = 0 ):
        if calories == 0:
            calories = 0.85*self.calories_goal
        self.option = "fruits"
        fruit_items = self.marked.filter(fruit = 1).exclude(name__contains = "Handful")
        self.fruits = self.select_best_minimum(fruit_items , calories , "fruit")
        #self.fruits.update_quantity(2)

    def select_salad(self , calories = 0):
        print("Calling Select Salad")
        if calories == 0:
            calories = 0.85*self.calories_goal
        self.option = "salad"
        salad_items = self.marked.filter(salad = 1 ).filter(~Q(name__startswith = "Handful")).all()
        m = Manipulator(items = salad_items , categorizers = [SaladCategoriser] )
        salad_items = m.categorize().get_final_list()
        self.salad = self.select_best_minimum(salad_items , calories , "salad")
        #self.salad.update_weight(1.5)

    def select_nut(self , calories = 0):
        print("Calling Select Nuts")
        if calories == 0:
            calories = 0.85*self.calories_goal
        self.option = "nuts"
        nuts_items = self.marked.filter(nuts = 1)
        self.nuts = self.select_best_minimum(nuts_items , calories , "nuts")
        steps = self.get_steps_quantity(self.nuts)
        print("Nuts Steps",steps)
        self.nuts.update_quantity((self.nuts.quantity + steps)/self.nuts.quantity)

    def select_snacks(self , calories = 0):
        print("Calling Select Snacks")
        if calories == 0:
            calories = 0.85*self.calories_goal
        self.option = "snacks"
        snack_items = self.marked.filter(snaks = 1).filter(dessert = 0)
        self.snacks = self.select_best_minimum(snack_items , calories , "snacks")

    def rethink(self):
        selected = getattr(self , self.option)
        if self.option == "fruits" or self.option == "nuts":
            steps = round(self.calories_remaining * selected.quantity/(selected.calarie))
            new_quantity = steps + selected.quantity
            selected.update_quantity(new_quantity/selected.quantity)
        else:
            steps = min( 5 , round(self.calories_remaining * selected.weight/(selected.calarie*10)))
            new_weight = min(250,selected.weight + steps * 10)
            selected.update_weight(new_weight/selected.weight)

    def get_probabilities(self):
        if ("nuts" , 0) in self.exclusion_conditions.children:
            return [1/3,0,1/3,1/3]
        return [ 0.33 , 0.33 , 0.33]
    
    def get_random_item(self):
            probability = self.get_probabilities()
            if self.disease and hasattr(self.disease , "nuts_probability"):
                probability = self.disease.nuts_probability
            func = sample([
                self.select_fruit , self.select_snacks , self.select_salad
            ], 1)[0]
            if hasattr(self , "drink"):
                cals = self.calories_remaining
            else:
                cals = self.calories_goal * 0.85    
            func(calories = cals)
            return self

    def build(self):
        if self.disease and hasattr( self.disease , "m4_build"):
            getattr(self.disease , "m4_build")(self)
        else:
            self.select_drink()
            self.get_random_item()
        return self

class M5(Base,CerealTreeSelector):
    percent = 0.20

    def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , exclude2 = None , make_combination = False , selected = None):
        self.exclusion_conditions = exclusion_conditions
        self.calories_goal = calories*self.percent + extra
        self.goal = goal
        self.disease = disease
        self.exclude = exclude
        self.exclude2 = exclude2
        self.queryset = self.getQuerysetFromGoal()
        self.make_combination = make_combination

        self.queryset = self.queryset.exclude(name__in = exclude).filter(calarie__gt = 0)
        if self.disease:
            self.queryset = self.queryset.filter(self.disease.queryset_filter)

        if exclusion_conditions : 
            self.queryset = self.queryset.filter(exclusion_conditions)

        self.marked = self.queryset
        self.selected = selected

        self.buildMapper = {
            'vegetable' : self.select_vegetables,
            'cereal' : self.cerealReplacer,
            'pulse' : self.pulseReplacer,
            'combination' : self.makeCombination
        }
        backwardMapper = {
            'grains_cereals' : self.cerealReplacer,
            'pulses' : self.pulseReplacer,
        }
        self.buildMapper.update(backwardMapper)

    def getQuerysetFromGoal(self):
        if self.goal == Goals.WeightLoss : 
            queryset = Food.m5loss_objects
        if self.goal == Goals.WeightGain or self.goal == Goals.MuscleGain:
            queryset = Food.m5gain_objects
        if self.goal == Goals.MaintainWeight:
            queryset = Food.m5stable_objects
        return queryset

    def select_vegetables(self , percent = 0.22):
        calories = percent*self.calories_goal
        self.vegetable_calories = calories
        food_list = self.marked.filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
        if food_list.count() < 3 : 
            food_list = self.getQuerysetFromGoal().filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
            food_list = food_list.filter(exclusion_conditions)
        if self.disease and hasattr(self.disease , "m5_vegetable_filter"):
            food_list = food_list.filter(self.disease.m5_vegetable_filter)
        m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
        food_list = m.categorize().get_final_list()
        self.vegetable_list = food_list
        self.vegetables = self.select_best_minimum(food_list , calories , "vegetable")


    def select_cereals(self,extra_filter = Q()):
        calories = 0.39*self.calories_goal
        if self.exclude2:
            food_list = self.getQuerysetFromGoal().exclude(name__in = self.exclude2).exclude(name__in = self.exclude).filter(grains_cereals = 1).filter(cuisine = "Generic")
            food_list = food_list.filter(self.exclusion_conditions)
        else:
            food_list = self.marked.filter(grains_cereals = 1).filter(cuisine = "Generic")
        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(grains_cereals = 1).filter(cuisine = "Generic")
            food_list = food_list.filter(self.exclusion_conditions)
        food_list = food_list.filter(extra_filter)
        m = Manipulator(items = food_list , categorizers = [GrainsCerealsCategoriser])
        final_food_list = m.categorize().get_final_list()
        self.cereals = self.select_best_minimum(final_food_list , calories , "cereal")

    def select_pulses(self , percent = 0.39, extra_filter = Q()):
        calories = percent * self.calories_goal
        food_list = self.marked.filter(pulses = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
        food_list = food_list.filter(extra_filter)
        if food_list.count() < 3:
            food_list = self.getQuerysetFromGoal().filter(pulses = 1).filter(extra_filter).filter(self.exclusion_conditions) 
        m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
        food_list = m.categorize().get_final_list()
        self.pulse = self.select_best_minimum(food_list , calories , "pulse")

    def makeGeneric(self):
        self.select_cereals()
        
        #In case the item is non vegetarian cereal, only a pulse is required
        if self.cereals.non_veg == 1:
            self.select_pulses(percent = 0.61 , extra_filter = Q(vegetables = 1))
            return self

        if self.cereals.vegetables == 1 and self.cereals.pulse == 0:
            self.select_pulses(percent = 0.61 , extra_filter = Q(pulse = 1))
        elif self.cereals.vegetables == 0 and self.cereals.pulse == 1:
            self.select_pulses(percent = 0.61,extra_filter = Q(vegetables = 1))
        elif self.cereals.vegetables == 1 and self.cereals.pulse == 1:
            self.select_pulses(percent = 0.61)
        if self.cereals.vegetables == 0 and self.cereals.pulse == 0:
            self.select_pulses()
            self.select_vegetables()
        return self

    def makeCombination(self):
        food_list = self.marked.filter(cuisine = "Combination") 
        m = Manipulator(items = food_list , categorizers = [CombinationCategoriser])
        food_list = m.categorize().get_final_list()
        self.combination = self.select_best_minimum(food_list , self.calories_goal , name = "combination")
        
    def pulseReplacer(self):
        self.getCerealFromSelected()    
        extra_filter = Q()
        percent = 0.39
        if self.cereal.non_veg == 1:
            extra_filter &= Q(non_veg_gravy_items = 1) & Q(vegetable = 1)
            percent = 0.61
        elif self.cereal.vegetables ==1 and self.cereal.pulse == 0:
            extra_filter &= Q(pulse = 1)
            percent = 0.61
        elif self.cereal.vegetables == 0 and self.cereal.pulse == 1:
            extra_filter &= Q(vegetables = 1)
            percent = 0.61  
        self.select_pulses(percent = percent , extra_filter = extra_filter)
        return self
    
    def rethink(self):
        if not hasattr(self , "combination"):
            if self.calories < self.calories_goal:
                new_weight = min(self.pulse.weight +  self.get_steps(self.pulse)*5) 
                self.pulse.update_weight(new_weight/self.pulse.weight)

    def build(self):
        if self.make_combination:
            self.makeCombination()
        else:
            self.makeGeneric()
        return self

