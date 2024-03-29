# Generated by Django 3.0.14 on 2023-01-29 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('date_of_birth', models.DateField()),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbCalendarioVacina',
            fields=[
                ('id_vacina', models.AutoField(primary_key=True, serialize=False)),
                ('cod_vacina', models.CharField(max_length=8)),
                ('descricao_vacina', models.CharField(max_length=45)),
                ('observacao', models.CharField(max_length=45)),
                ('meses', models.IntegerField()),
                ('status_vacina', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'verbose_name': 'Tabela de vacina',
                'verbose_name_plural': 'Tabela de vacinas',
                'db_table': 'tb_calendario_vacina',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbLoginUsuario',
            fields=[
                ('id_log_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('user_name_login', models.CharField(max_length=45)),
                ('user_password', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'tb_login_usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbMunicipioBrasil',
            fields=[
                ('id_municipiobrasil', models.AutoField(primary_key=True, serialize=False)),
                ('ibge7', models.IntegerField(blank=True, db_column='IBGE7', null=True)),
                ('uf', models.TextField(blank=True, db_column='UF', null=True)),
                ('município', models.TextField(blank=True, db_column='Município', null=True)),
                ('região', models.TextField(blank=True, db_column='Região', null=True)),
                ('população_2010', models.IntegerField(blank=True, db_column='População 2010', null=True)),
            ],
            options={
                'db_table': 'tb_municipio_brasil',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbMunicipios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ibge7', models.IntegerField(blank=True, db_column='IBGE7', null=True)),
                ('uf', models.TextField(blank=True, db_column='UF', null=True)),
                ('município', models.TextField(blank=True, db_column='Município', null=True)),
                ('região', models.TextField(blank=True, db_column='Região', null=True)),
                ('população_2010', models.IntegerField(blank=True, db_column='População 2010', null=True)),
            ],
            options={
                'verbose_name': 'Tabela de municipio',
                'verbose_name_plural': 'Tabela de municipios',
                'db_table': 'tb_municipios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbUbsDadosBrasil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnes', models.TextField(db_column='CNES')),
                ('uf', models.IntegerField(blank=True, db_column='UF', null=True)),
                ('ibge', models.IntegerField(blank=True, db_column='IBGE', null=True)),
                ('nome', models.TextField(blank=True, db_column='NOME', null=True)),
                ('logradouro', models.TextField(blank=True, db_column='LOGRADOURO', null=True)),
                ('bairro', models.TextField(blank=True, db_column='BAIRRO', null=True)),
                ('latitude', models.TextField(blank=True, db_column='LATITUDE', null=True)),
                ('longitude', models.TextField(blank=True, db_column='LONGITUDE', null=True)),
            ],
            options={
                'db_table': 'tb_ubs_dados_brasil',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbUbsDadosSp',
            fields=[
                ('codigoubs', models.IntegerField(db_column='codigoUBS')),
                ('codigonacionalsaude', models.IntegerField(db_column='codigoNacionalSaude')),
                ('endereçoubs', models.TextField(db_column='endereçoUBS')),
                ('numeroenderecoubs', models.CharField(db_column='numeroEnderecoUBS', max_length=10)),
                ('cepubs', models.CharField(db_column='cepUBS', max_length=10)),
                ('bairroenderecoubs', models.CharField(db_column='bairroEnderecoUBS', max_length=45)),
                ('horariofuncionamentoubs', models.CharField(db_column='horarioFuncionamentoUBS', max_length=45)),
                ('tipoprimeironivelubs', models.CharField(blank=True, db_column='tipoPrimeiroNivelUBS', max_length=45, null=True)),
                ('tiposegundonivelubs', models.CharField(blank=True, db_column='tipoSegundoNivelUBS', max_length=45, null=True)),
                ('nometipoprimeironivel', models.CharField(blank=True, db_column='nomeTipoPrimeiroNivel', max_length=45, null=True)),
                ('telefone1ubs', models.CharField(blank=True, db_column='telefone1UBS', max_length=45, null=True)),
                ('telefone2ubs', models.CharField(blank=True, db_column='telefone2UBS', max_length=45, null=True)),
                ('exibirreferenciaubs', models.CharField(blank=True, db_column='exibirReferenciaUBS', max_length=45, null=True)),
                ('informacoesidentificacaoubs', models.TextField(blank=True, db_column='informacoesIdentificacaoUBS', null=True)),
                ('latitude', models.CharField(blank=True, max_length=50, null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, null=True)),
                ('idubsbrasil_field', models.AutoField(db_column="idubsbrasil'", primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Tabela de UBS',
                'verbose_name_plural': 'Tabela de UBS',
                'db_table': 'tb_ubs_dados_sp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vacinas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao_vacina', models.CharField(max_length=45)),
                ('observacao', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'vacinas',
                'managed': False,
            },
        ),
    ]
