import random 
import math 
import simpy

TOTAL_COHETES = 5
NUMERO_PLATAFORMAS = 1 
MIN_ESPERA_COHETE = 200 
MAX_ESPERA_COHETE = 300
T_LLEGADAS = 200

def lanzar(cohete):
  R = random.random()
  tiempo = MAX_ESPERA_COHETE - MIN_ESPERA_COHETE
  tiempo_lanzamiento  = MIN_ESPERA_COHETE + (tiempo * R)
  yield env.timeout(tiempo_lanzamiento)
  print("\o/  %s lanzado con exito en %.2f minutos" %(cohete,tiempo_lanzamiento)) 

def cohete (env,name,plataformas):
  llega = env.now
  print('---> %s llego a plataforma en minuto %.2f' %(name,llega))
  with plataformas.request() as request:
    yield request 
    pasa = env.now
    espera = pasa - llega
    print('*** %s pasa a la plataforma de lanzamiento en el minuto %.2f habiendo esperado %.2f minutos ' %(name,llega,espera))
    yield env.process(lanzar(name))

def principal (env,plataformas):
  llegada = 0 
  for i in range(TOTAL_COHETES):
    R = random.random()
    llegada = -T_LLEGADAS * math.log(R)
    yield env.timeout(llegada)
    env.process(cohete(env,'Cohete %d' % (i+1), plataformas))

env = simpy.Environment()
plataformas = simpy.Resource(env,NUMERO_PLATAFORMAS)
env.process(principal(env,plataformas))
env.run()