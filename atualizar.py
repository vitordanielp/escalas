from os import system as sys
from time import sleep

print("Dados sendo atualizados... aguarde.")
sys("main.py")
sys("git add .")
sys('git commit -m "dados atualizados"')
sys('git push')
sleep(2)
print("Finalizado!")
exit()
