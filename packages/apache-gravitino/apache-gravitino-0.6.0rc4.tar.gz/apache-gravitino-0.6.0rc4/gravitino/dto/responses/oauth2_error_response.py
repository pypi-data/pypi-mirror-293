"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from dataclasses import dataclass, field
from dataclasses_json import config

from gravitino.dto.responses.error_response import ErrorResponse
from gravitino.exceptions.base import IllegalArgumentException


@dataclass
class OAuth2ErrorResponse(ErrorResponse):
    """Represents the response of an OAuth2 error."""

    _type: str = field(metadata=config(field_name="error"))
    _message: str = field(metadata=config(field_name="error_description"))

    def type(self):
        return self._type

    def message(self):
        return self._message

    def validate(self):
        if self._type is None:
            raise IllegalArgumentException("OAuthErrorResponse should contain type")
