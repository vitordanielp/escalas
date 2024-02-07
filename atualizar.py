from os import system as sys
from time import sleep

sys("main.py")
# sleep(10)
sys("git add .")
# sleep()
sys('git commit -m "dados atualizados"')
print("Dados sendo atualizados... aguarde.")
sleep(3)
print("Finalizado!")
sleep(1.5)
exit()
