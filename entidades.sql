create sequence planeta_seq start 1 increment 1;

create table planeta(
	id_planeta int default nextval('planeta_seq'),
	nome varchar(45),
    tamanho float,
    peso float,
    vel_rotacao float,
    possui_sn bool,
    comp_planeta varchar(45),
	constraint pk_planeta primary key (id_planeta)
);
