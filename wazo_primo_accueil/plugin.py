# -*- coding: utf-8 -*-
# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from wazo_agentd_client import Client as AgentdClient
from wazo_auth_client import Client as AuthClient
from wazo_chatd_client import Client as ChatdClient
from wazo_confd_client import Client as ConfdClient

from .http import (
    PrimoAccueilLoginResource,
    PrimoAccueilLogoutResource,
    PrimoAccueilActivationPrimoResource,
    PrimoAccueilDesActivationPrimoResource,
    PrimoAccueilActivationAccueilPhysiqueResource,
    PrimoAccueilDesActivationAccueilPhysiqueResource
)
from .services import PrimoAccueilService

logger = logging.getLogger(__name__)

class Plugin:

    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        agentd_client = AgentdClient(**config['agentd'])
        auth_client = AuthClient(**config['auth'])
        chatd_client = ChatdClient(**config['chatd'])
        confd_client = ConfdClient(**config['confd'])

        token_changed_subscribe(agentd_client.set_token)
        token_changed_subscribe(chatd_client.set_token)
        token_changed_subscribe(confd_client.set_token)

        primo_accueil_service = PrimoAccueilService(agentd_client, chatd_client, confd_client)

        api.add_resource(
            PrimoAccueilLoginResource,
            '/primo_accueil/login',
            resource_class_args=[primo_accueil_service]
        )
        api.add_resource(
            PrimoAccueilLogoutResource,
            '/primo_accueil/logout',
            resource_class_args=[primo_accueil_service]
        )
        api.add_resource(
            PrimoAccueilActivationPrimoResource,
            '/primo_accueil/activation_primo',
            resource_class_args=[primo_accueil_service]
        )
        api.add_resource(
            PrimoAccueilDesActivationPrimoResource,
            '/primo_accueil/desactivation_primo',
            resource_class_args=[primo_accueil_service]
        )
        api.add_resource(
            PrimoAccueilActivationAccueilPhysiqueResource,
            '/primo_accueil/activation_accueil_physique',
            resource_class_args=[primo_accueil_service]
        )
        api.add_resource(
            PrimoAccueilDesActivationAccueilPhysiqueResource,
            '/primo_accueil/desactivation_accueil_physique',
            resource_class_args=[primo_accueil_service]
        )
