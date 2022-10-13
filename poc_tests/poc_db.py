from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime



Base = declarative_base()


class Distrito_sanitario(Base):
    __tablename__ = "distrito_sanitario"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    municipio =  Column(String)

    distrito_bairro = relationship("Bairro", cascade="all, delete-orphan", backref="distrito_sanitario")
    distritos_b = association_proxy('distrito_bairro', 'bairro')

    def __init__(self, id, nome, municipio) -> None:
        self.id = id
        self.nome = nome
        self.municipio = municipio

    def __repr__(self) -> str:
        return "<DistritoSanitario(ID=%s, Nome=%s, Municipio=%s \
            )>" % (self.id, self.nome, self.municipio)


class Bairro(Base):
    __tablename__ = "bairro"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    distrito_sanitario_id = Column(Integer, ForeignKey(Distrito_sanitario.id)) # FK >- Distrito_sanitario.id

    bairro_solicitacao = relationship("Solicitacao",
                                      cascade="all, delete-orphan",
                                      backref="bairro")
    bairro_s = association_proxy('bairro', 'solicitacao')

    def __init__(self, id, nome, distritoID) -> None:
        self.id = id
        self.nome = nome
        self.distrito_sanitario_id = distritoID

    def __repr__(self) -> str:
        return "<Bairro(ID=%s, Nome=%s, DistritoID=%s)>" % (self.id,
            self.nome, self.distrito_sanitario_id)


class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    sexo = Column(String(1))
    idade = Column(Integer)
    bairro_id = Column(Integer, ForeignKey(Bairro.id))
    origem = Column(String)
    situacao = Column(String)
    sistema_saude = Column(String)
    motivo_descarte = Column(String)
    acompanhamento_medico = Column(Boolean)
    data_acionamento = Column(DateTime)
    data_chegada = Column(DateTime)
    data_conclusao = Column(DateTime)
    data_remocao = Column(DateTime)

    solicitacao_remocao = relationship("Remocao",
                                       cascade="all, delete-orphan",
                                       backref="solicitacao")
    solicitacao_r = association_proxy('solicitacao', 'remocao')

    
    def __init__(self, id, data, p_sexo, p_idade, bairroID, origem, situacao,
                 sistema_saude, motivo_descarte, acompanhamento_medico,
                 data_acionamento, data_chegada, data_conclusao, data_remocao
                )-> None:   

        self.id = id
        self.data = data
        self.sexo = p_sexo
        self.idade = p_idade
        self.bairro_id = bairroID
        self.origem = origem
        self.situacao = situacao
        self.sistema_saude = sistema_saude
        self.motivo_descarte = motivo_descarte
        self.acompanhamento_medico = acompanhamento_medico
        self.data_acionamento = data_acionamento
        self.data_chegada = data_chegada
        self.data_conclusao = data_conclusao
        self.data_remocao = data_remocao

    def __repr__(self) -> str:
        return "<Solicitação(ID='%s', Data='%s', Sexo=%s, Idade=%s, \
            BairroId=%s, Origem=%s, Situação=%s, SistemaSaude=%s, \
            MotivoDescarte=%s, AcompanhamentoMedico=%s, DAcionamento=%s, \
            DChegada=%s, DConclusão=%s, DRemoção=%s)>" % ( self.id, self.data,
            self.sexo, self.idade, self.bairro_id, self.origem, self.situacao,
            self.sistema_saude, self.motivo_descarte,
            self.acompanhamento_medico, self.data_acionamento,
            self.data_chegada, self.data_conclusao, self.data_remocao)


class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    bairro_id = Column(Integer, ForeignKey(Bairro.id)) # FK >- Bairro.id

    hospital_remocao = relationship("Bairro", backref="hospital")                             
    hospital_r = association_proxy('hospital', 'bairro')

    hospital_especialidade = relationship("Especialidade",
                                          cascade="all, delete-orphan",
                                          backref="hospital")
    hospital_e = association_proxy('hospital', 'especialidade')

    def __init__(self, id, nome, bairroID) -> None:
        self.id = id
        self.nome = nome
        self.bairro_id = bairroID 

    def __repr__(self) -> str:
        return "<Hospital(ID=%s, Nome=%s, BairroID=%s)>" % (self.id,
            self.nome, self.bairro_id) 


class Remocao(Base):
    __tablename__ = "remocao"

    id = Column(Integer, autoincrement=True, primary_key=True)
    solicitacao_id = Column(Integer, ForeignKey(Solicitacao.id))  # FK >- Solicitacao
    remocao_sequencial = Column(Integer) 
    hospital_id = Column(Integer, ForeignKey(Hospital.id)) # FK >- Hospital.id
    data = Column(DateTime)
    remocao_aceitacao = Column(Boolean)
    nao_aceitacao_descricao = Column(String)

    def __init__(self, solicID, remocaoSeq, hospID, data, RAceitacao,
                 NAceitacao) -> None:

        # self.id = id autoincrement=True
        self.solicitacao_id = solicID
        self.remocao_sequencial = remocaoSeq 
        self.hospital_id = hospID
        self.data = data
        self.remocao_aceitacao = RAceitacao
        self.nao_aceitacao_descricao = NAceitacao
            
    def __repr__(self) -> str:
        return "<Remocao(ID=%s, SolicitacaoID=%s, RemocaoSeq=%s, \
            HospitalID=%s, Data=%s, RemocaoAceita=%s, NãoAceitacaoDesc=%s) \
            >" % (self.id, self.solicitacao_id, self.remocao_sequencial,
            self.hospital_id, self.data, self.remocao_aceitacao,
            self.nao_aceitacao_descricao)


class Especialidade(Base):
    __tablename__ = "especialidade"

    hospital_id = Column(Integer, ForeignKey(Hospital.id), primary_key=True) # FK >- Hospital.id
    especialidade = Column(String, primary_key=True)

    def __init__(self, hospital_id, especialidade) -> None:
        self.hospital_id = hospital_id
        self.especialidade = especialidade

    def __repr__(self) -> str:
        return "<Viatura(HospitalID=%s, Especialidade=%s)>" % (
            self.hospital_id, self.especialidade)


class Viatura(Base):
    __tablename__ = "viatura"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    distrito_sanitario_id = Column(Integer, ForeignKey(Distrito_sanitario.id)) # FK >- Distrito_sanitario.id
    tipo_viatura = Column(String)

    def __init__(self, id, desc, distroID, tipo_viatura) -> None:
        self.id = id
        self.descricao = desc
        self.distrito_sanitario_id = distroID
        self.tipo_viatura = tipo_viatura

    def __repr__(self) -> str:
        return "<Viatura(ID=%s, Desc=%s, DistritoID=%s, TipoViatura=%s)>" % (
            self.id, self.descricao, self.distrito_sanitario_id,
            self.tipo_viatura)


# SMALL SAMPLE TEST

engine = create_engine('sqlite:///SAMU_TEST.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()


### DISTRITO SANITARIO
distrito_ex1 = Distrito_sanitario(1, 'DISTRITO 01', 'Recife')
distrito_ex2 = Distrito_sanitario(2, 'DISTRITO 02', 'Recife')
distrito_ex3 = Distrito_sanitario(3, 'DISTRITO 03', 'Recife')

session.add(distrito_ex1)
session.add(distrito_ex2)
session.add(distrito_ex3)


### BAIRO
bairro_ex1 = Bairro(19, 'CENTRO', 1)
bairro_ex2 = Bairro(27, 'SANTO ANTONIO', 1)
bairro_ex3 = Bairro(35, 'SAO JOSE', 1)
bairro_ex4 = Bairro(175, 'ENCRUZILHADA', 2)
bairro_ex5 = Bairro(140, 'DERBY', 3)

session.add(bairro_ex1)
session.add(bairro_ex2)
session.add(bairro_ex3)
session.add(bairro_ex4)
session.add(bairro_ex5)


### SOLICITACAO
solicitacao_ex1 = Solicitacao(1119819, datetime.strptime('2015-01-01 04:56', '%Y-%m-%d %H:%M'), 'F', 0.0,	19,  'VIA PÚBLICA', 'DESCARTADA', 	None, 	            'DESISTENCIA DA SOLICITAÇÃO', 	 0,    None, 	                                                None, 	                                                    datetime.strptime('2015-01-01 05:19', '%Y-%m-%d %H:%M'), 	None)
solicitacao_ex2 = Solicitacao(1119893, datetime.strptime('2015-01-01 07:01', '%Y-%m-%d %H:%M'), 'M', 60.0, 	19,  'VIA PÚBLICA', 'DESCARTADA', 	None, 	            'REMOVIDO ANTES DO ATENDIMENTO', 0,    datetime.strptime('2015-01-01 07:16', '%Y-%m-%d %H:%M'), None, 	                                                    datetime.strptime('2015-01-01 08:03', '%Y-%m-%d %H:%M'), 	None)
solicitacao_ex3 = Solicitacao(1121924, datetime.strptime('2015-01-05 04:21', '%Y-%m-%d %H:%M'), 'M', 22.0, 	19,  'VIA PÚBLICA', 'DESCARTADA', 	None, 	            'SOLICITAÇÃO DUPLICADA', 	     0,    None,           	                                        None, 	                                                    datetime.strptime('2015-01-05 04:41', '%Y-%m-%d %H:%M'), 	None)
solicitacao_ex4 = Solicitacao(1119988, datetime.strptime('2015-01-01 10:29', '%Y-%m-%d %H:%M'), 'F', 0.0,	27,  'VIA PÚBLICA', 'DESCARTADA', 	None, 	            'DESISTENCIA DA SOLICITAÇÃO', 	 0,    None, 	                                                None, 	                                                    datetime.strptime('2015-01-01 11:04', '%Y-%m-%d %H:%M'), 	None)
solicitacao_ex5 = Solicitacao(1121124, datetime.strptime('2015-01-03 15:07', '%Y-%m-%d %H:%M'), 'F', 35.0, 	27,  'VIA PÚBLICA', 'DESCARTADA', 	None, 	            'CIODS - BOMBEIRO', 	         0,    datetime.strptime('2015-01-03 15:24', '%Y-%m-%d %H:%M'), None, 	                                                    datetime.strptime('2015-01-03 15:38', '%Y-%m-%d %H:%M'), 	None)
solicitacao_ex6 = Solicitacao(1121419, datetime.strptime('2015-01-04 03:24', '%Y-%m-%d %H:%M'), 'M', 17.0, 	35,  'VIA PÚBLICA', 'CONCLUIDA',	'CAUSAS EXTERNAS', 	None, 	                         1,    datetime.strptime('2015-01-04 03:29', '%Y-%m-%d %H:%M'), datetime.strptime('2015-01-04 04:11', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-04 04:12', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-04 04:11', '%Y-%m-%d %H:%M'))
solicitacao_ex7 = Solicitacao(1121682, datetime.strptime('2015-01-04 17:12', '%Y-%m-%d %H:%M'), 'M', 85.0, 	35,  'VIA PÚBLICA', 'CONCLUIDA',	'DOENÇAS DA PELE', 	None, 	                         0,    datetime.strptime('2015-01-04 17:18', '%Y-%m-%d %H:%M'), datetime.strptime('2015-01-04 17:35', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-04 18:32', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-04 18:32', '%Y-%m-%d %H:%M'))
solicitacao_ex8 = Solicitacao(1121534, datetime.strptime('2015-01-04 11:06', '%Y-%m-%d %H:%M'), 'M', 48.0, 	175, 'VIA PÚBLICA', 'CONCLUIDA',	'CAUSAS EXTERNAS', 	None, 	                         0,    datetime.strptime('2015-01-04 11:22', '%Y-%m-%d %H:%M'), datetime.strptime('2015-01-04 12:18', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-04 12:18', '%Y-%m-%d %H:%M'),	datetime.strptime('2015-01-04 12:18', '%Y-%m-%d %H:%M'))
solicitacao_ex9 = Solicitacao(1119986, datetime.strptime('2015-01-01 10:26', '%Y-%m-%d %H:%M'), 'M', 0.0,	140, 'VIA PÚBLICA', 'CONCLUIDA',	'CAUSAS EXTERNAS', 	None, 	                         0,    datetime.strptime('2015-01-01 10:34', '%Y-%m-%d %H:%M'), datetime.strptime('2015-01-01 12:13', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-01 12:14', '%Y-%m-%d %H:%M'), 	datetime.strptime('2015-01-01 12:14', '%Y-%m-%d %H:%M'))

session.add(solicitacao_ex1)
session.add(solicitacao_ex2)
session.add(solicitacao_ex3)
session.add(solicitacao_ex4)
session.add(solicitacao_ex5)
session.add(solicitacao_ex6)
session.add(solicitacao_ex7)
session.add(solicitacao_ex8)
session.add(solicitacao_ex9)


### REMOÇÂO
remocao_ex1 = Remocao(1119986, 1, 9,   datetime.strptime('2015-01-01 12:14:15', '%Y-%m-%d %H:%M:%S'), 1, None)
remocao_ex2 = Remocao(1121419, 1, 9,   datetime.strptime('2015-01-04 04:11:05', '%Y-%m-%d %H:%M:%S'), 1, None)
remocao_ex3 = Remocao(1121534, 1, 109, datetime.strptime('2015-01-04 12:18:31', '%Y-%m-%d %H:%M:%S'), 1, None)
remocao_ex4 = Remocao(1121682, 1, 116, datetime.strptime('2015-01-04 18:32:02', '%Y-%m-%d %H:%M:%S'), 1, None)

session.add(remocao_ex1)
session.add(remocao_ex2)
session.add(remocao_ex3)
session.add(remocao_ex4)


### HOSPITAL 
hospital_ex1 = Hospital(9, 'HOSPITAL DA RESTAURACAO', 140)
hospital_ex2 = Hospital(109, 'UPA OLINDA', 2028)
hospital_ex3 = Hospital(116, 'UPA TORRÕES', 701)

session.add(hospital_ex1)
session.add(hospital_ex2)
session.add(hospital_ex3)


### ESPECIALIDADE
especialidade_ex1 = Especialidade(9,  'TRAUMATOLOGIA')
especialidade_ex2 = Especialidade(9,  'NEUROLOGIA')
especialidade_ex3 = Especialidade(9,  'PEDIATRIA')
especialidade_ex4 = Especialidade(9,  'CIRURGIA GERAL')
especialidade_ex5 = Especialidade(9,  'CLINICA GERAL')
especialidade_ex6 = Especialidade(9,  'QUEIMADOS')
especialidade_ex7 = Especialidade(9,  'OTORRINOLARINGO')
especialidade_ex8 = Especialidade(9,  'OFTALMO')
especialidade_ex9 = Especialidade(9,  'BUCOMAXILAR')
especialidade_ex10 = Especialidade(9, 'CL.VASCULAR')

session.add(especialidade_ex1)
session.add(especialidade_ex2)
session.add(especialidade_ex3)
session.add(especialidade_ex4)
session.add(especialidade_ex5)
session.add(especialidade_ex6)
session.add(especialidade_ex7)
session.add(especialidade_ex8)
session.add(especialidade_ex9)
session.add(especialidade_ex10)


### VIATURA
viatura_ex1 = Viatura(160, 'USB 25 Extra - Recife', 1, 'Básica')
viatura_ex2 = Viatura(161, 'USB 26 Extra - Recife', 1, 'Básica')
viatura_ex3 = Viatura(15, 'USB 15 - Recife',        2, 'Básica')
viatura_ex4 = Viatura(72, 'MOTO 02 - Recife',       2, 'Apoio rápido')
viatura_ex5 = Viatura(65, 'Helicóptero PRF',        3, 'Helicóptero')
viatura_ex6 = Viatura(73, 'MOTO 03 - Recife',       3, 'Apoio rápido')

session.add(viatura_ex1)
session.add(viatura_ex2)
session.add(viatura_ex3)
session.add(viatura_ex4)
session.add(viatura_ex5)
session.add(viatura_ex6)

session.commit()

session.close()

