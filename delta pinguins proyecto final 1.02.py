import pyomo.environ as pyo

# Creación del modelo
modelo = pyo.ConcreteModel()

# Sets
modelo.dias = pyo.Set(initialize=days)
modelo.horas = pyo.Set(initialize=hours)
modelo.hora_ocupada = pyo.Set(initialize=subjects)

# Parámetros
modelo.horas_por_orario = pyo.Param(modelo.hora_ocupada, initialize=hours_per_subject)
modelo.min_dias = pyo.Param(modelo.hora_ocupada, initialize=min_days_per_subject)
modelo.max_dias = pyo.Param(modelo.hora_ocupada, initialize=max_days_per_subject)
modelo.preferencias = pyo.Param(modelo.dias, modelo.horas, modelo.hora_ocupada, initialize=preferences)

# Variables de decisión
modelo.vbSubjectSchedule = pyo.Var(modelo.dias, modelo.horas, modelo.hora_ocupada, domain=pyo.Binary)

# Restricciones
# Asignación única
modelo.ctOnlyOneSubject = pyo.ConstraintList()
for i in modelo.dias:
    for j in modelo.horas:
        modelo.ctOnlyOneSubject.add(sum(modelo.vbSubjectSchedule[i, j, k] for k in modelo.hora_ocupada) <= 1)

# Impartir exactamente el número de horas lectivas de cada asignatura
modelo.ctCoverAllHours = pyo.ConstraintList()
for k in modelo.hora_ocupada:
    modelo.ctCoverAllHours.add(sum(modelo.vbSubjectSchedule[i, j, k] for i in modelo.dias for j in modelo.horas) == modelo.horas_por_orario[k])

# Respetar el máximo de horas lectivas por asignatura diario
modelo.ctMaxDailyHours = pyo.ConstraintList()
for k in modelo.hora_ocupada:
    for i in modelo.dias:
        modelo.ctMaxDailyHours.add(sum(modelo.vbSubjectSchedule[i, j, k] for j in modelo.horas) <= max_hours_per_day)

# Restricción de apoyo para la variable indicativa
modelo.ctSubjectDaysFlags = pyo.ConstraintList()
for k in modelo.hora_ocupada:
    for i in modelo.dias:
        modelo.ctSubjectDaysFlags.add(max_hours_per_day * modelo.vbSubjectDaysFlags[i, k] >= sum(modelo.vbSubjectSchedule[i, j, k] for j in modelo.horas))

# Máximo y mínimo número de días lectivos por asignatura
modelo.ctSubjectDays = pyo.ConstraintList()
for k in modelo.hora_ocupada:
    modelo.ctSubjectDays.add(sum(modelo.vbSubjectDaysFlags[i, k] for i in modelo.dias) <= modelo.max_dias[k])
    modelo.ctSubjectDays.add(sum(modelo.vbSubjectDaysFlags[i, k] for i in modelo.dias) >= modelo.min_dias[k])

# Asignaciones en bloques horarios consecutivos
modelo.ctSubjectSwitches = pyo.ConstraintList()
for k in modelo.hora_ocupada:
    for i in modelo.dias:
        for j in modelo.horas:
            modelo.ctSubjectSwitches.add(modelo.vbSubjectSchedule[i, j, k] - modelo.vbSubjectSchedule[i, modelo.horas.prevw(j), k] <= modelo.vbSubjectSwitches[i, j, k])
            modelo.ctSubjectSwitches.add(-modelo.vbSubjectSchedule[i, j, k] + modelo.vbSubjectSchedule[i, modelo.horas.prevw(j), k] <= modelo.vbSubjectSwitches[i, j, k])
        modelo.ctSubjectSwitches.add(sum(modelo.vbSubjectSwitches[i, j,