-- Creacion momentanea de la tabla alumno

create table if not exists alumno(

   id_alumno serial primary key ,
   nombre varchar(200) not null,
   codigo varchar(20) unique not null -- Ejemplo 'MAT-1', 'FIS-4'
);


-- Creacion de la tabla materia

create table if not exists materias(

   id_materia serial primary key ,
   nombre varchar(200) not null,
   codigo varchar(10) unique not null, -- Ejemplo 'MAT-1', 'FIS-4'
   grado int not null ,
   
   constraint chk_grado check(grado between 1 and 5)
);

-- Creacion de la tabla puente inscripciones

create table if not EXISTS inscripcion(

   id_inscripcion serial primary key,
   id_materia int not null references materias(id_materia) on delete restrict,
   id_alumno int not null references alumno(id_alumno) on delete restrict,
   periodo varchar(12) not null,
   seccion varchar(1) not null,
   
   constraint chk_periodo check(periodo ~'^\d{4}-\d{4}$'), -- Ejemplo '2025-2026'
   constraint chk_seccion check(seccion in ('A', 'B', 'C', 'D')),
   constraint uq_alumno_materia_periodo unique (id_alumno, id_materia, periodo)
   
);

-- Creacion de la tabla notas

create table if not EXISTS notas(

   id_notas serial primary key,
   id_inscripcion int not null references inscripcion(id_inscripcion) on delete cascade,
   valor_nota decimal(4,2) not null,
   lapso int not null,
   fecha_registro timestamp default current_timestamp,
   
   constraint chk_valor_nota check(valor_nota between 0 and 20), -- Nota solo entre 0 y 20
   constraint chk_lapso check(lapso in (1, 2, 3)),
   constraint uq_inscripcion_lapso unique (id_inscripcion, lapso)
);