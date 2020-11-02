# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from dataclasses import dataclass


class CandcontasItem(Item):
    ufSuperiorCandidatura = Field()
    localCandidatura = Field()
    eleicaoAno = Field()
    eleicaoId = Field()
    ufCandidatura = Field()
    cargoId = Field()
    cargoEleicao = Field()
    partido = Field()
    candidatoId = Field()
    nomeUrna = Field()
    nomeCompleto = Field()
    cpf = Field()
    descricaoSituacao = Field()
    descricaoEstadoCivil = Field()
    descricaoCorRaca = Field()
    grauInstrucao = Field()
    ocupacao = Field()
    gastoCampanha1T = Field()
    gastoCampanha2T = Field()
    totalBens = Field()