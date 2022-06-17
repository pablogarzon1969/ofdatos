from src.business.proyectBusiness import ProyectBusiness
import time
   
if __name__ == "__main__":
    inicio = time.time()
    
    ProyectBusiness.execute_proyect()
    
    print(time.time()-inicio)