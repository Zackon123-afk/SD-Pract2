CLIENT

Llibreries:
xmlrpc

Definició:
Arxiu python que donarà peticions de feina al servidor

Peticions:
create() -> crea worker
number()-> nº de workers
lista() -> llista de workers
delete(id) -> borra worker segons paràmetre
suma(urls) -> conta el nº de paràmetres
count(urls)
wordcount(urls)




SERVER

Llibreries:
xmlrpc
multiprocessing
redis
json
threading

Definició:
Arxiu python que gestiona els workers i tracta les peticions delegant-les als workers

Funcions:
create_worker() -> crea worker
delete_worker(id) -> borra worker segons paràmetre
numberOfWorkers() -> nº de workers
list_workers() -> llista de workers
do_tasks(func, params) -> envia la funció a una cua que tracten els workers, indicada per primer paràmetre i els paràmetres en el segon

Observacions:
Al final del arxiu, es pot observar com registrem la informació enviada desde el client al servidor.
El servidor es capaç de gestionar invocacions simples i múltiples.




WORKER

Llibreries:
json
re
urllib.request

Definició:
Arxiu python que tracta les peticions desde una cua i envia el resultat al SERVER

Funcions:
start_worker() -> Cicle infinit del worker, on tracta les peticions
merge() -> funció que ajunta els resultats d'una tasca i ho retorna al SERVER
llegirFitxer() -> obra un fitxer i retorna el text d'una web
suma() -> suma 1 a la cua
countingWords() -> conta les paraules d'un fitxer
wordCount() -> crea un diccionari amb els cops que apareix cada paraula

