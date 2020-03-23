create sequence galaxia_seq start 1 increment 1;
create sequence sistema_seq start 1 increment 1;
create sequence estrela_seq start 1 increment 1;
create sequence planeta_seq start 1 increment 1;
create sequence satelite_seq start 1 increment 1;

create table usuario(
    klogin varchar(45),
    kpassword varchar(45),
    constraint pk_usuario primary key (klogin)
);

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

create table galaxia(
	id_galaxia varchar(45) default 'temp',
  	qt_sistema int,
  	dist_terra int,
  	nome varchar(45),
  	constraint pk_galaxia primary key (id_galaxia)
);

create table sistema(
	id_sistema varchar(45) default 'temp',
  	nome varchar(45),
  	qt_planetas int,
  	qt_estrelas int,
  	idade int,
  	galaxia varchar(45),
  	constraint pk_sistema primary key (id_sistema),
  	constraint fk_galaxia foreign key (galaxia) references galaxia(id_galaxia)
);

create table estrela(
	id_estrela varchar(45) default 'temp',
  	nome varchar(45),
  	tamanho float,
  	idade int,
  	possui_estrela bool,
  	dist_terra float,
  	primary key (id_estrela)
);

create table sistema_estrela(
	sistema varchar(45),
  	sistema_galaxia varchar(45),
  	estrela varchar(45),
  	constraint fk_sistema foreign key (sistema) references sistema(id_sistema),
  	constraint fk_sistema_galaxia foreign key (sistema_galaxia) references galaxia(id_galaxia),
  	constraint fk_estrela foreign key (estrela) references estrela(id_estrela)
);

create table sistema_planeta(
	sistema varchar(45),
  	sistema_galaxia varchar(45),
  	planeta varchar(45),
  	foreign key (sistema) references sistema(id_sistema),
  	foreign key (sistema_galaxia) references galaxia(id_galaxia),
  	foreign key (planeta) references planeta(id_planeta)
);

create table ana_vermelha(
	estrela varchar(45),
  	foreign key (estrela) references estrela(id_estrela)
);

create table ana_branca(
	estrela varchar(45),
  	foreign key (estrela) references estrela(id_estrela)
);

create table gigante_azul(
	estrela varchar(45),
  	foreign key (estrela) references estrela(id_estrela)
);

create table estrela_binaria(
	estrela varchar(45),
  	foreign key (estrela) references estrela(id_estrela)
);

create table gigante_vermelha(
	estrela varchar(45),
  	morte varchar(45),
  	primary key (estrela),
  	foreign key (estrela) references estrela(id_estrela)
);

create table buraco_negro(
	gigante_vermelha varchar(45),
  	foreign key (gigante_vermelha) references gigante_vermelha(estrela)
);


create table satelite(
	id_satelite varchar(45) default 'temp',
  	nome varchar(45),
  	tamanho float,
  	peso float,
  	comp_sn varchar(45),
    constraint pk_satelite primary key (id_satelite)
);

create table orbitar(
	satelite varchar(45),
  	planeta varchar(45),
  	estrela varchar(45),
  	foreign key (satelite) references satelite(id_satelite),
  	foreign key (planeta) references planeta(id_planeta),
  	foreign key (estrela) references estrela(id_estrela)
);

create function proxima_chave() returns trigger as $definir_chave$
    declare
        nome_tabela varchar(45) := TG_TABLE_NAME;
        pk varchar(45) := TG_TABLE_NAME;
        pk_id varchar(45) := TG_TABLE_NAME;
        seq varchar(45) := TG_TABLE_NAME;
        def varchar(4) := 'temp';
        run_seq_num integer := 30;
    begin
        seq := seq || '_seq';
        select nextval(seq) into run_seq_num;
        pk := pk || run_seq_num;
        pk_id := 'id_' || pk_id;
        execute 'update ' || nome_tabela || ' set ' || pk_id || ' = ''' || pk || ''' where ' || pk_id || ' = ''temp''';
        return new;
    end;
$definir_chave$ language plpgsql;

create trigger definir_chave after insert on planeta for each row execute procedure proxima_chave();
create trigger definir_chave after insert on estrela for each row execute procedure proxima_chave();
create trigger definir_chave after insert on galaxia for each row execute procedure proxima_chave();
create trigger definir_chave after insert on sistema for each row execute procedure proxima_chave();
create trigger definir_chave after insert on satelite for each row execute procedure proxima_chave();
