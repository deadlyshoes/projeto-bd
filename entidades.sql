create sequence planeta_seq start 1 increment 1;

create table planeta(
	id_planeta varchar(45) default 'temp',
	nome varchar(45),
    tamanho float,
    peso float,
    vel_rotacao float,
    possui_sn bool,
    comp_planeta varchar(45),
	constraint pk_planeta primary key (id_planeta)
);

create function proxima_chave() returns trigger as $definir_chave$
    declare
        pk varchar(45) := 'planeta';
        run_seq_num integer := 30;
    begin
        select nextval('planeta_seq') into run_seq_num;
        pk := pk || run_seq_num;
        update planeta set id_planeta = pk where id_planeta = 'temp';
        return new;
    end;
$definir_chave$ language plpgsql;

create trigger definir_chave after insert on planeta for each row execute procedure proxima_chave()

create table galaxia(
	id_galaxia int,
  	qt_sistema int,
  	dist_terra int,
  	nome varchar(45),
  	constraint pk_galaxia primary key (id_galaxia)
);

create table sistema(
	id_sistema int,
  	nome varchar(45),
  	qt_planetas int,
  	qt_estrelas int,
  	idade int,
  	galaxia int,
  	constraint pk_sistema primary key (id_sistema),
  	constraint fk_galaxia foreign key (galaxia) references galaxia(id_galaxia)
);

create table sistema_estrela(
	sistema int,
  	sistema_galaxia int,
  	estrela int,
  	constraint fk_sistema foreign key (sistema) references sistema(id_sistema),
  	constraint fk_sistema_galaxia foreign key (sistema_galaxia) references galaxia(id_galaxia),
  	constraint fk_estrela foreign key (estrela) references estrela(id_estrela)
);

create table sistema_planeta(
	sistema int,
  	sistema_galaxia int,
  	planeta int,
  	foreign key (sistema) references sistema(id_sistema),
  	foreign key (sistema_galaxia) references galaxia(id_galaxia),
  	foreign key (planeta) references planeta(id_planeta)
);

create table estrela(
	id_estrela int,
  	nome varchar(45),
  	tamanho float,
  	idade int,
  	possui_estrela bool,
  	dist_terra float,
  	primary key (id_estrela)
);

create table ana_vermelha(
	estrela int,
  	foreign key (estrela) references estrela(id_estrela)
);

create table ana_branca(
	estrela int,
  	foreign key (estrela) references estrela(id_estrela)
);

create table gigante_azul(
	estrela int,
  	foreign key (estrela) references estrela(id_estrela)
);

create table estrela_binaria(
	estrela int,
  	foreign key (estrela) references estrela(id_estrela)
);

create table gigante_vermelha(
	estrela int,
  	morte varchar(45),
  	primary key (estrela),
  	foreign key (estrela) references estrela(id_estrela)
);

create table buraco_negro(
	gigante_vermelha int,
  	foreign key (gigante_vermelha) references gigante_vermelha(estrela)
);

create table orbitar(
	satelite int,
  	planeta int,
  	estrela int,
  	foreign key (satelite) references satelite(id_satelite),
  	foreign key (planeta) references planeta(id_planeta),
  	foreign key (estrela) references estrela(id_estrela)
);

create table satelite(
	id_satelite int,
  	nome varchar(45),
  	tamanho float,
  	peso float,
  	comp_sn varchar(45)
);