# -*- coding: utf-8 -*-
import scrapy
import json
from candcontas.items import CandcontasItem


class DivulgacandcontasSpider(scrapy.Spider):
    name = "divulgacandcontas"
    allowed_domains = ["divulgacandcontas.tse.jus.br"]

    def start_requests(self):
        url = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/ordinarias/"
        yield scrapy.Request(url, self.parse_eleicoes_ordinarias)

    def parse_eleicoes_ordinarias(self, response):
        self.logger.info("Pegando os anos das eleições")
        eleicoes = json.loads(response.body)

        uf_estados = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES",
                      "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE",
                      "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
                      "SE", "SP", "TO", ]

        for eleicao in eleicoes:
            ano = eleicao["ano"]
            id_eleicao = eleicao["id"]
            nome_eleicao = eleicao["nomeEleicao"]

            if ano in [2020]:
                for uf_estado in uf_estados:
                    url = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/" \
                          "buscar/{fuf}/{fcodEleicao}/municipios"\
                        .format(fuf=uf_estado,
                                fcodEleicao=id_eleicao)

                    # item = CandcontasItem()
                    # item["ano_eleicao"] = eleicao["ano"]
                    # item["id_eleicao"] =
                    # item["nome_eleicao"] =

                    yield scrapy.Request(url,
                                         self.parse_municipios,
                                         meta={"ano": ano,
                                               "id_eleicao": id_eleicao,
                                               "nome_eleicao": nome_eleicao,
                                               "uf": uf_estado})
                    #break
            #break

    def parse_municipios(self, response):
        self.logger.info("Pegando os municípios de uma determinada UF")
        municipios = json.loads(response.body)

        tipos_candidatos = {"prefeito": 11, "vice_prefeito": 12, "vereador": 13}

        for tipo_candidato in tipos_candidatos:
            if tipo_candidato in ["vereador"]:
                for municipio in municipios["municipios"]:
                    # nm_municipio =pio["nome"]
                    cod_municipio = municipio["codigo"]

                    url = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/" \
                          "listar/{fano}/{fcod_municipio}/{fcod_eleicao}/{ftipo_candidato}/candidatos" \
                        .format(fano=response.meta["ano"],
                                fcod_municipio=cod_municipio,
                                fcod_eleicao=response.meta["id_eleicao"],
                                ftipo_candidato=tipos_candidatos[tipo_candidato])

                    yield scrapy.Request(url,
                                         self.parse_candidatos,
                                         meta={"ano": response.meta["ano"],
                                               "cod_municipio": cod_municipio,
                                               "id_eleicao": response.meta["id_eleicao"],
                                               "nome_eleicao": response.meta["nome_eleicao"],
                                               "tipo_candidato": tipo_candidato})
                    #break
            #break

    def parse_candidatos(self, response):
        self.logger.info("Pegando os candidatos")
        candidatos = json.loads(response.body)

        uf = candidatos["unidadeEleitoral"]["sigla"]
        cidade = candidatos["unidadeEleitoral"]["nome"]

        for candidato in candidatos["candidatos"]:
            url = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/"\
                  "buscar/{fano}/{fcod_municipio}/{fid_eleicao}/candidato/{fcod_candidato}"\
                .format(fano=response.meta["ano"],
                        fcod_municipio=response.meta["cod_municipio"],
                        fid_eleicao=response.meta["id_eleicao"],
                        fcod_candidato=candidato["id"])

            yield scrapy.Request(url,
                                 self.parse_candidato_info,
                                 meta={"ano": response.meta["ano"],
                                       "id_eleicao": response.meta["id_eleicao"],
                                       "nome_eleicao": response.meta["nome_eleicao"]})

            #break

    def parse_candidato_info(self, response):
        self.logger.info("Detalhando o candidato")
        candidato = json.loads(response.body)

        item = CandcontasItem()
        item["localCandidatura"] = candidato["localCandidatura"]
        item["ufSuperiorCandidatura"] = candidato["ufSuperiorCandidatura"]
        item["eleicaoAno"] = candidato["eleicao"]["ano"]
        item["eleicaoId"] = candidato["eleicao"]["id"]
        item["ufCandidatura"] = candidato["ufCandidatura"]
        item["cargoId"] = candidato["cargo"]["codigo"]
        item["cargoEleicao"] = candidato["cargo"]["nome"]
        item["partido"] = candidato["partido"]["sigla"]
        item["candidatoId"] = candidato["id"]
        item["nomeUrna"] = candidato["nomeUrna"]
        item["nomeCompleto"] = candidato["nomeCompleto"]
        item["cpf"] = candidato["cpf"]
        item["descricaoSituacao"] = candidato["descricaoSituacao"]
        item["descricaoEstadoCivil"] = candidato["descricaoEstadoCivil"]
        item["descricaoCorRaca"] = candidato["descricaoCorRaca"]
        item["grauInstrucao"] = candidato["grauInstrucao"]
        item["ocupacao"] = candidato["ocupacao"]
        item["gastoCampanha1T"] = candidato["gastoCampanha1T"]
        item["gastoCampanha2T"] = candidato["gastoCampanha2T"]
        item["totalBens"] = 0
        for bem in candidato["bens"]:
            item["totalBens"] += bem["valor"]


        yield item