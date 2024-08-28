## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('tempmon.appliances.dashboard'):
      <li>${h.link_to("Go to the Dashboard", url('tempmon.dashboard'))}</li>
  % endif
</%def>

<%def name="modify_vue_vars()">
  ${parent.modify_vue_vars()}
  <script>
    ${form.vue_component}Data.probesData = ${json.dumps(probes_data)|n}
  </script>
</%def>
