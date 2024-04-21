# Delta-Pinguins-Proyecto-
Proyecto optimizacion de horarios


import pyomo.environ as pyo
import numpy as np
import pyomo.kernel as pmo
import pandas as pd
In [3]:
# Args 
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
                            domain = pmo.Binary
# Parameters
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
In [6]:
# Helper variables
model.vbSubjectDaysFlags = pyo.Var(model.sDays, model.sSubjects, domain = pmo.Binary)
model.vIcumulatedHours = pyo.Var(model.sDays, model.sHours, model.sSubjects, domain = pyo.NonNegativeIntegers)
model.vIsubjectTotalDays = pyo.Var(domain = pyo.NonNegativeIntegers)
model.vbSubjectSwitches = pyo.Var(model.sDays, model.sHours, model.sSubjects, domain = pmo.Binary)

# Constraints 
#-------- single assignment constraints
# :: Only one subject can be held in the classroom at the same time
model.ctOnlyOneSubject = pyo.ConstraintList()
for i in model.sDays:
    for j in model.sHours:
        model.ctOnlyOneSubject.add(sum(model.vbSubjectSchedule[i,j,k] for k in model.sSubjects)<=1)

model.ctCoverAllHours = pyo.ConstraintList()
for k in model.sSubjects:
    model.ctCoverAllHours.add(
        sum(model.vbSubjectSchedule[i,j,k] for i in model.sDays for j in model.sHours)<=model.pHoursPerSubject[k]
    )
    
    model.ctCoverAllHours.add(
        sum(model.vbSubjectSchedule[i,j,k] for i in model.sDays for j in model.sHours)>=model.pHoursPerSubject[k]
    )

# :: the total hours per day must be lower than the max total
model.ctMaxDailyHours = pyo.ConstraintList()
for k in model.sSubjects:
    for i in model.sDays:
        model.ctMaxDailyHours.add(
            sum(model.vbSubjectSchedule[i,j,k] for j in model.sHours)<=max_hours_per_day
        )

model.ctSubjectDaysFlags = pyo.ConstraintList()
for k in model.sSubjects:
    for i in model.sDays:
        model.ctSubjectDaysFlags.add(
            max_hours_per_day*model.vbSubjectDaysFlags[i,k]>=sum(model.vbSubjectSchedule[i,j,k] for j in model.sHours)

# :: Each subject can be assigned to at most hours/max hours DAYS and at least 1 hour on each of the days it has been scheduled.
model.ctSubjectDays = pyo.ConstraintList()
for k in model.sSubjects:
    model.ctSubjectDays.add(
        sum(model.vbSubjectDaysFlags[i,k] for i in model.sDays)<=model.pMaxDaysPerSubject[k]
    )
    
    model.ctSubjectDays.add(
        sum(model.vbSubjectDaysFlags[i,k] for i in model.sDays)>=model.pMinDaysPerSubject[k]
    )

# :: Each subject must be given in consecutive blocks
model.ctSubjectSwitches = pyo.ConstraintList()
for k in model.sSubjects:
    for i in model.sDays:
        for j in model.sHours:
            model.ctSubjectSwitches.add(
                expr = model.vbSubjectSchedule[i,j,k] - model.vbSubjectSchedule[i,model.sHours.prevw(j), k] <= model.vbSubjectSwitches[i,j,k]
            )
            model.ctSubjectSwitches.add(
                expr = -model.vbSubjectSchedule[i,j,k] + model.vbSubjectSchedule[i,model.sHours.prevw(j), k] <= model.vbSubjectSwitches[i,j,k]
            )

        model.ctSubjectSwitches.add(
            expr = sum(model.vbSubjectSwitches[i,j,k] for j in model.sHours)==2*model.vbSubjectDaysFlags[i,k]
        )

        if max_hours_per_day < len(model.sHours):
            model.ctSubjectSwitches.add(
                expr = model.vbSubjectSchedule[i,model.sHours.first(), k] + model.vbSubjectSchedule[i,model.sHours.last(), k] <= 1
            )

model.ctCumulativeHours = pyo.ConstraintList()
model.ctCumulativeHours.add(
    model.vIsubjectTotalDays == sum(model.vbSubjectDaysFlags[i,k] for i in model.sDays for k in model.sSubjects)-sum(model.pMinDaysPerSubject[k] for k in model.sSubjects)
)

penalty = -5


for k in preferences:
    model.pPreferences[k[0],k[1],k[2]]=k[3]

model.ctFixedSlots = pyo.ConstraintList()
for k in constraints:
    v = k[3]
    if v==1:
        model.ctFixedSlots.add(expr = model.vbSubjectSchedule[k[0],k[1],k[2]]==v)

# Objective function
maximize = 1
model.objSchedule= pyo.Objective(
    sense = -maximize,
    expr  = penalty*(model.vIsubjectTotalDays) + sum(model.pPreferences[i,j,k]*model.vbSubjectSchedule[i,j,k] for i in model.sDays for j in model.sHours for k in model.sSubjects)
)

opt = pyo.SolverFactory('cbc')
res = opt.solve(model)
print(res)


def print_schedule(model):

    hours = []
    subjects = []
    days = []
    bool_class = []
    for i in model.sDays:
        for j in model.sHours:
            for k in model.sSubjects:
                hours.append(j)
                days.append(i)
                subjects.append(k)
                bool_class.append(model.vbSubjectSchedule[i,j,k].value)

    df_schedule = pd.DataFrame({'day':days, 'hour':hours, 'subject':subjects, 'class':bool_class})
    df_schedule = df_schedule[df_schedule['class']>0].pivot(index = 'hour', columns = 'day', values = 'subject')

    return df_schedule.loc[[h for h in model.sHours] , [d for d in model.sDays]]
