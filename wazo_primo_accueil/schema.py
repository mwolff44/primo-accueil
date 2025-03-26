# -*- coding: utf-8 -*-
# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from marshmallow import (
    EXCLUDE,
    fields,
    Schema,
)
from marshmallow.validate import Length, Range


class PrimoAccueilSchema(Schema):
    userId = fields.Str(required=True, validate=Length(min=1))
    agentId = fields.Integer(required=True, validate=Range(min=1))
    lineId = fields.Integer(required=True, validate=Range(min=1))
    doNotDisturb = fields.Boolean(required=True)
    state = fields.Str(required=True, validate=Length(min=1))
    status = fields.Str(required=True, validate=Length(min=1))

    class Meta:
        strict = True
        unknown = EXCLUDE

primo_accueil_schema = PrimoAccueilSchema()