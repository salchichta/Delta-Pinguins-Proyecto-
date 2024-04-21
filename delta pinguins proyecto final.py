import pyomo.environ as pyo
import numpy as np
import pyomo.kernel as pmo
import pandas as pd

days = ['l','m','x','j', 'v']
hours = [f"h_{i}" for i in np.arange(10,14,1)]
subjects = [f"SB_{i}" for i in range(8)]
hours_per_subject = dict(zip(subjects, [2 for i in range(8)]))
for i in np.random.choice(subjects, 4):
    hours_per_subject[i]+=1

max_hours_per_day = 2
    
preferences = [
    ('l', f"h_{11}", 'SB_3', 4)
]

constraints = [
    ('l', f"h_{12}", 'SB_1',  1)
]

hours_per_subject


model = pyo.ConcreteModel()

# Sets
model.sDays = pyo.Set(initialize = days, ordered = True)
model.sHours = pyo.Set(initialize = hours, ordered = True)
model.sSubjects = pyo.Set(initialize = subjects)

# Decision variable
model.vbSubjectSchedule = pyo.Var(
                            model.sDays,
                            model.sHours,
                            model.sSubjects,
                            domain = pmo.Binary)
                            
model.pHoursPerSubject = pyo.Param(model.sSubjects, initialize = hours_per_subject)
model.pMinDaysPerSubject = pyo.Param(
                            model.sSubjects,
                            initialize = dict(zip(
                                                hours_per_subject.keys(),
                                                [round(i/max_hours_per_day) for i in list(hours_per_subject.values())]
                                               )
                                         )
                            )

model.pMaxDaysPerSubject = pyo.Param(model.sSubjects, initialize = hours_per_subject)

model.pPreferences = pyo.Param(
    model.sDays,
    model.sHours,
    model.sSubjects,
    initialize = 1.0,
    mutable = True
)


# Helper variables
model.vbSubjectDaysFlags = pyo.Var(model.sDays, model.sSubjects, domain = pmo.Binary)
model.vIcumulatedHours = pyo.Var(model.sDays, model.sHours, model.sSubjects, domain = pyo.NonNegativeIntegers)
model.vIsubjectTotalDays = pyo.Var(domain = pyo.NonNegativeIntegers)
model.vbSubjectSwitches = pyo.Var(model.sDays, model.sHours, model.sSubjects, domain = pmo.Binary)