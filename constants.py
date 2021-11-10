BASAL_REPRODUCTION = 2.5   # r0 – dimensionless

INFECTION_TIME = 2.9    # T_inf – [days]
INCUBATION_TIME = 5.2   # T_inc – [days]

ICU_DEMAND = 0.03   # 3%

TIME_IN_ICU = 7.0   # [days]

# Compute some important constants
CONSTANT_1 = BASAL_REPRODUCTION / INFECTION_TIME
CONSTANT_2 = 1.0 / INCUBATION_TIME
CONSTANT_3 = 1.0 / INFECTION_TIME