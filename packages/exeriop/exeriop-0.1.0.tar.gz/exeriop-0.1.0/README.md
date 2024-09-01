# Hack4u Academy Courses Library

 Una Biblioteca Python para consutar los cursos de Hack4u.

## Cursos Disponibles

- Introduccion a linux [ 15 horas ]
- Personalizacion de Linux [ 3 horas ]
- Introduccion al Hacking [ 53 horas ]
- Python Ofensivo [ 35 horas ]

## Instalacion

Instala el paquete usando `pip3`:

```python3
pip3 install Hack4u
```

## Uso basico 

### Listar todos los cursos

```python
from Hack4u import list_courses

for course in courses():
    print(course)
```

### Obtener curso por nombre

```python
form Hack4u import get_course_by_name

course = get_course_by_name("Introduccion a Linux")
print(course)
```

### Calculadora duracion total de los cursos

```python3
from Hack4u.untils import total_duration

print(f"Duracion total: {total_duration()} horas")
```
