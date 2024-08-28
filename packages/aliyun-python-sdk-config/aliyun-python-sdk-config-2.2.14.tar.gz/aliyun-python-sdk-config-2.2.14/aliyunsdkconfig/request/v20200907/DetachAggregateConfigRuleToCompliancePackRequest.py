# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkconfig.endpoint import endpoint_data

class DetachAggregateConfigRuleToCompliancePackRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Config', '2020-09-07', 'DetachAggregateConfigRuleToCompliancePack','config')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ConfigRuleIds(self): # String
		return self.get_query_params().get('ConfigRuleIds')

	def set_ConfigRuleIds(self, ConfigRuleIds):  # String
		self.add_query_param('ConfigRuleIds', ConfigRuleIds)
	def get_AggregatorId(self): # String
		return self.get_query_params().get('AggregatorId')

	def set_AggregatorId(self, AggregatorId):  # String
		self.add_query_param('AggregatorId', AggregatorId)
	def get_CompliancePackId(self): # String
		return self.get_query_params().get('CompliancePackId')

	def set_CompliancePackId(self, CompliancePackId):  # String
		self.add_query_param('CompliancePackId', CompliancePackId)
