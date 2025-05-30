# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging


class PrimoAccueilService(object):

    def __init__(self, agentd, chatd, confd):
        self.agentd = agentd
        self.chatd = chatd
        self.confd = confd

    def login(self, params, tenant_uuid):
        # Update state and status
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "available" # available / away / unavailable / invisible
        user_args['status'] = "Service accueil"
        self.chatd.user_presences.update(user_args, tenant_uuid)

        # Login the agent
        agent = int(params.get('agentId'))
        extension = params.get('extension')
        context = params.get('context')
        try:
            self.agentd.agents.login_agent(
                agent_id=agent,
                extension=extension,
                context=context,
                tenant_uuid=tenant_uuid)
        except:
            print("Error during agent login")

        return 'OK'

    def logout(self, params, tenant_uuid):
        # Remove skill to agent
        try:
            self._agent_and_skill_association(False, params, tenant_uuid)
        except:
            print("Skill already removed")
        # Unpause the agent
        agent = self._get_agent(params.get('agentId'))
        try:
            self.agentd.agents.unpause_agent_by_number(agent['number'], tenant_uuid)
        except:
            print("Agent not in pause, continue")
        # Update state and status
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "available" # available / away / unavailable / invisible
        user_args['status'] = ""
        self.chatd.user_presences.update(user_args, tenant_uuid)

        # Logout the agent
        try:
            self.agentd.agents.logoff_agent(params.get('agentId'), tenant_uuid)
        except:
            print("Error during agent logout")

        return 'OK'
    
    def activation_primo(self, params, tenant_uuid):
        # Update status => Primo accueil
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "available" # available / away / unavailable / invisible
        user_args['status'] = "Primo accueil"
        self.chatd.user_presences.update(user_args, tenant_uuid)

        # Be sure that agent is not in pause
        agent = self._get_agent(params.get('agentId'))
        try:
            self.agentd.agents.unpause_agent_by_number(agent['number'], tenant_uuid)
        except:
            print("Error unpause agent")

        # Add "PRIMO_ACCUEIL" skill to agent

        try:
            self._agent_and_skill_association(True, params, tenant_uuid)
        except:
            print("Error during skill dassociation")

        return 'OK'
    
    def desactivation_primo(self, params, tenant_uuid):
        # Remove status => Primo accueil
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "available" # available / away / unavailable / invisible
        user_args['status'] = "Service accueil"
        self.chatd.user_presences.update(user_args, tenant_uuid)
       
        # Remove "PRIMO_ACCUEIL" skill to agent

        try:
            self._agent_and_skill_association(False, params, tenant_uuid)
        except:
            print("Error during skill dis-association")

        return 'OK'
    
    def activation_accueil_physique(self, params, tenant_uuid):
        # Pause the agent
        agent = self._get_agent(params.get('agentId'))
        try:
            self.agentd.agents.pause_agent_by_number(agent['number'], tenant_uuid)
        except:
            print("Error pause agent")
        
        # Update status => Accueil physique
        # Update state => DND or unvailable
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "away" # available / away / unavailable / invisible
        user_args['status'] = "Accueil physique"
        self.chatd.user_presences.update(user_args, tenant_uuid)

        return 'OK'
    
    def desactivation_accueil_physique(self, params, tenant_uuid):
        # Unpause the agent
        agent = self._get_agent(params.get('agentId'))
        try:
            self.agentd.agents.unpause_agent_by_number(agent['number'], tenant_uuid)
        except:
            print("Error unpause agent")

        # Remove status => Accueil physique
        # Update state => available
        user_args = {}
        user_args['uuid'] = params.get('userId')
        user_args['state'] = "available" # available / away / unavailable / invisible
        user_args['status'] = "Primo accueil"
        self.chatd.user_presences.update(user_args, tenant_uuid)

        return 'OK'
    
    def _find_skill(self, tenant_uuid):
        # Get skill id based on skill name
        skill_name = "PRIMO_ACCUEIL"
        skills = self.confd.agent_skills.list(tenant_uuid=tenant_uuid)
        for skill in skills['items']:
            print(skill)
            if str(skill['name']) == skill_name:
                return skill['id']
            
    def _agent_and_skill_association(self, associate, params, tenant_uuid):
        # update association agent_id with PRIMO_ACCUEIL skills
        # Get skill id
        skill_id = self._find_skill(tenant_uuid)
        agent_id = params.get('agentId')
        if skill_id:
            if associate:
                # add skill to agent
                return self.confd.agents.relations(agent_id).add_skill(skill_id, weight=10)
            else:
                # remove skill to agent
                return self.confd.agents.relations(agent_id).remove_skill(skill_id)
        else:
            return "skill not found"

    def _get_agent(self, agent_id):
        # Get agent info by ID
        return self.confd.agents.get(agent_id)
