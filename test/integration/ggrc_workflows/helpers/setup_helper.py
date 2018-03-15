# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Package contains Workflow related setup helper.

They help to setup data for Workflow related tests.
"""

from ggrc.access_control import role
from ggrc.models import all_models
from ggrc_workflows import ac_roles
from integration.ggrc.models import factories
from integration.ggrc_workflows.models import factories as wf_factories
from integration.ggrc_workflows.helpers import person_setup


class WorkflowSetup(person_setup.PersonSetup):
  """Setup helper for Workflow related objects setup."""

  def __init__(self):
    super(WorkflowSetup, self).__init__(all_models.Workflow.__name__)

  def _setup_wf_person(self, g_rname, wf_rname, workflow):
    """Generate Person with Global + Workflow Scope role.

    Args:
        g_rname: Global Role name.
        wf_rname: Workflow Access Control Role name.
        workflow: Workflow instance, in which scope person should have role.
    """
    wf_person = self.setup_person(g_rname, wf_rname)
    wf_acr = role.get_ac_roles_for(all_models.Workflow.__name__)[wf_rname]
    factories.AccessControlListFactory(ac_role=wf_acr, object=workflow,
                                       person=wf_person)

  def setup_workflow(self, wfa_g_rnames, wfm_g_rnames=()):
    """Setup Workflow object for tests usage.

    Args:
        wfa_g_rnames: Tuple with Global Role names who should be WF Admin.
        wfm_g_rnames: Tuple with Global Role names who should be WF Member.

    Returns:
        Workflow instance generated by Factory.
    """
    workflow = wf_factories.WorkflowFactory()

    for g_rname in wfa_g_rnames:
      self._setup_wf_person(g_rname, ac_roles.workflow.ADMIN_NAME, workflow)

    for g_rname in wfm_g_rnames:
      self._setup_wf_person(g_rname, ac_roles.workflow.MEMBER_NAME, workflow)

    return workflow
