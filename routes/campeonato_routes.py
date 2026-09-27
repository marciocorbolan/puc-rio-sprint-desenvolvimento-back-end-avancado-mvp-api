# --- Bibliotecas de Terceiros ---
from flask import Blueprint, jsonify
from integrations.api_futebol import get_dados_api_futebol

# --- Módulos do Projeto ---
from middlewares.decorators import token_required


campeonato_bp = Blueprint('campeonato', __name__)

CAMPEONATO_ID = 10


#########################################################################


@campeonato_bp.route('/', methods=['GET'])
@token_required
def get_campeonato(current_user):
    """
    Retorna os metadados de um campeonato, incluindo todas as suas fases.
    ---
    tags:
      - Campeonato
    responses:
      200:
        description: Detalhes do campeonato retornados com sucesso.
        schema:
          type: object
          properties:
            campeonato_id:
              type: integer
              description: Identificador único do campeonato.
            nome:
              type: string
              description: Nome oficial do campeonato.
            nome_popular:
              type: string
              description: Nome popular/abreviado (ex. Brasileirão).
            slug:
              type: string
              description: Identificador textual amigável para URLs.
            edicao_atual:
              type: object
              description: Edição (temporada) vigente.
              properties:
                edicao_id:
                  type: integer
                temporada:
                  type: string
                nome:
                  type: string
                nome_popular:
                  type: string
                slug:
                  type: string
            fase_atual:
              type: object
              nullable: true
              description: Fase em disputa no momento.
              properties:
                fase_id:
                  type: integer
                nome:
                  type: string
                slug:
                  type: string
                tipo:
                  type: string
                _link:
                  type: string
            rodada_atual:
              type: object
              nullable: true
              description: Rodada vigente quando aplicável (null em mata-mata).
              properties:
                nome:
                  type: string
                slug:
                  type: string
                rodada:
                  type: integer
                status:
                  type: string
            status:
              type: string
              description: Situação do campeonato (andamento, finalizado ou agendado).
            tipo:
              type: string
              description: Formato (Pontos Corridos, Mata-Mata ou Misto).
            logo:
              type: string
              description: URL do escudo/logo do campeonato.
            regiao:
              type: string
              description: Abrangência (nacional, regional ou continental).
            fases:
              type: array
              description: Fases da edição atual.
              items:
                type: object
                properties:
                  fase_id:
                    type: integer
                  edicao:
                    type: object
                  nome:
                    type: string
                  slug:
                    type: string
                  status:
                    type: string
                  tipo:
                    type: string
                  decisivo:
                    type: boolean
                  eliminatorio:
                    type: boolean
                  ida_e_volta:
                    type: boolean
                  grupos:
                    type: boolean
                  chaves:
                    type: boolean
                  rodadas:
                    type: array
                  proxima_fase:
                    type: object
                    nullable: true
                  fase_anterior:
                    type: object
                    nullable: true
                  _link:
                    type: string
      401:
        description: Token JWT ausente ou inválido
      502:
        description: Erro na resposta da API externa
    """

    path = f"/campeonatos/{CAMPEONATO_ID}"
    dados, status = get_dados_api_futebol(path)

    return jsonify(dados), status


#########################################################################


@campeonato_bp.route('/tabela', methods=['GET'])
@token_required
def get_campeonato_tabela(current_user):
    """
    Classificação atualizada do campeonato.
    ---
    tags:
      - Campeonato
    responses:
      200:
        description: Tabela de classificação retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              posicao:
                type: integer
                description: Posição na tabela.
              pontos:
                type: integer
                description: Pontos somados.
              time:
                type: object
                description: Dados do time (time_id, nome_popular, sigla, escudo).
                properties:
                  time_id:
                    type: integer
                  nome_popular:
                    type: string
                  sigla:
                    type: string
                  escudo:
                    type: string
              jogos:
                type: integer
                description: Partidas disputadas.
              vitorias:
                type: integer
                description: Número de vitórias.
              empates:
                type: integer
                description: Número de empates.
              derrotas:
                type: integer
                description: Número de derrotas.
              gols_pro:
                type: integer
                description: Gols marcados.
              gols_contra:
                type: integer
                description: Gols sofridos.
              saldo_gols:
                type: integer
                description: Saldo de gols.
              aproveitamento:
                type: integer
                description: Aproveitamento de pontos (%).
              variacao_posicao:
                type: integer
                description: Variação de posição em relação à rodada anterior.
              ultimos_jogos:
                type: array
                description: Últimos resultados v (vitória), e (empate), d (derrota).
                items:
                  type: string
              faixa_classificacao:
                type: object
                nullable: true
                description: Faixa da tabela (ex. libertadores, rebaixamento).
                properties:
                  nome:
                    type: string
                  cor:
                    type: string
      400:
        description: Parâmetros inválidos
      404:
        description: Cadastro não encontrado
    """
    path = f"/campeonatos/{CAMPEONATO_ID}/tabela"
    dados, status = get_dados_api_futebol(path)

    return jsonify(dados), status


#########################################################################


@campeonato_bp.route('/rodadas', methods=['GET'])
@token_required
def get_campeonato_rodadas(current_user):
    """
    Todas as rodadas de um campeonato de pontos corridos.
    ---
    tags:
      - Campeonato
    responses:
      200:
        description: Rodada retornadas com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              nome:
                type: string
                description: Nome da rodada (ex. 1ª Rodada).
              slug:
                type: string
                description: Slug da rodada.
              rodada:
                type: integer
                description: Número da rodada.
              status:
                type: string
                description: Situacao da rodada (encerrada, andamento ou agendada).
              proxima_rodada:
                type: object
                nullable: true
                description: Resumo da rodada seguinte.
                properties:
                  nome:
                    type: string
                  slug:
                    type: string
                  rodada:
                    type: integer
                  status:
                    type: string
                  _link:
                    type: string
              rodada_anterior:
                type: object
                nullable: true
                description: Resumo da rodada anterior.
                properties:
                  nome:
                    type: string
                  slug:
                    type: string
                  rodada:
                    type: integer
                  status:
                    type: string
                  _link:
                    type: string
              _link:
                type: string
                description: Caminho relativo (HATEOAS) para a rodada.
      400:
        description: Parâmetros inválidos
      404:
        description: Cadastro não encontrado
    """
    path = f"/campeonatos/{CAMPEONATO_ID}/rodadas"
    dados, status = get_dados_api_futebol(path)

    return jsonify(dados), status


#########################################################################


@campeonato_bp.route('/rodadas/<int:id>', methods=['GET'])
@token_required
def get_campeonato_rodada(current_user, id):
    """
    Partidas de uma rodada específica.
    ---
    tags:
      - Campeonato
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Número/ID da rodada
    responses:
      200:
        description: Detalhes da rodada retornados com sucesso
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome da rodada.
            rodada:
              type: integer
              description: Número da rodada.
            status:
              type: string
              description: Situação da rodada.
            partidas:
              type: array
              description: Partidas da rodada (resumo).
              items:
                type: object
                properties:
                  placar:
                    type: string
                    description: Placar formatado (ex. Atlético-MG 2x2 Palmeiras).
                  time_mandante:
                    type: object
                    description: Time da casa (time_id, nome_popular, sigla, escudo).
                    properties:
                      time_id:
                        type: integer
                      nome_popular:
                        type: string
                      sigla:
                        type: string
                      escudo:
                        type: string
                  time_visitante:
                    type: object
                    description: Time visitante.
                    properties:
                      time_id:
                        type: integer
                      nome_popular:
                        type: string
                      sigla:
                        type: string
                      escudo:
                        type: string
                  data_realizacao_iso:
                    type: string
                    description: Data/hora em ISO 8601 com fuso (-0300).
                  estadio:
                    type: object
                    description: Estádio (estadio_id, nome_popular).
                    properties:
                      estadio_id:
                        type: integer
                      nome_popular:
                        type: string
      400:
        description: ID da rodada não informado ou inválido
      404:
        description: Rodada não encontrada
    """
    if not id:
        return jsonify({"message": "ID não informado"}), 400

    path = f"/campeonatos/{CAMPEONATO_ID}/rodadas/{id}"
    dados, status = get_dados_api_futebol(path)

    return jsonify(dados), status