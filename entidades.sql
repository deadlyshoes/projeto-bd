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

create trigger definir_chave after insert on planeta for each row execute procedure proxima_chave();
