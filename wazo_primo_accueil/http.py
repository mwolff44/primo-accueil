# -*- coding: utf-8 -*-
# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import request
from flask_restful import Resource
from xivo.tenant_flask_helpers import Tenant

from wazo_calld.auth import required_acl
from wazo_calld.http import AuthResource

from .schema import (
    primo_accueil_schema,
)


class PrimoAccueilLoginResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        success = self._primo_accueil_service.login(request_body, tenant.uuid)

        if success:
            return "Successfull login", 201
        else:
            return "Error", 400

class PrimoAccueilLogoutResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        result = self._primo_accueil_service.logout(request_body, tenant.uuid)

        return result, 201
    
class PrimoAccueilActivationPrimoResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        success = self._primo_accueil_service.activation_primo(request_body, tenant.uuid)

        if success:
            return "Successfull login", 201
        else:
            return "Error", 400

class PrimoAccueilDesActivationPrimoResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        result = self._primo_accueil_service.desactivation_primo(request_body, tenant.uuid)

        return result, 201

class PrimoAccueilActivationAccueilPhysiqueResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        success = self._primo_accueil_service.activation_accueil_physique(request_body, tenant.uuid)

        if success:
            return "Successfull login", 201
        else:
            return "Error", 400

class PrimoAccueilDesActivationAccueilPhysiqueResource(AuthResource):

    def __init__(self, primo_accueil_service):
        self._primo_accueil_service = primo_accueil_service

    #@required_acl('confd.primo_accueil.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = primo_accueil_schema.load(request.get_json(force=True))
        result = self._primo_accueil_service.desactivation_accueil_physique(request_body, tenant.uuid)

        return result, 201