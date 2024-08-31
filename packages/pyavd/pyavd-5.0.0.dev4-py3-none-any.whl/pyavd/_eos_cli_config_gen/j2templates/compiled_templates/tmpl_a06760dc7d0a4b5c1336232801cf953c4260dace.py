from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/port-channel-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
    l_0_encapsulation_dot1q_interfaces = resolve('encapsulation_dot1q_interfaces')
    l_0_flexencap_interfaces = resolve('flexencap_interfaces')
    l_0_namespace = resolve('namespace')
    l_0_port_channel_interface_pvlan = resolve('port_channel_interface_pvlan')
    l_0_port_channel_interface_vlan_xlate = resolve('port_channel_interface_vlan_xlate')
    l_0_evpn_es_po_interfaces = resolve('evpn_es_po_interfaces')
    l_0_evpn_dfe_po_interfaces = resolve('evpn_dfe_po_interfaces')
    l_0_evpn_mpls_po_interfaces = resolve('evpn_mpls_po_interfaces')
    l_0_link_tracking_interfaces = resolve('link_tracking_interfaces')
    l_0_port_channel_interface_ipv4 = resolve('port_channel_interface_ipv4')
    l_0_ip_nat_interfaces = resolve('ip_nat_interfaces')
    l_0_port_channel_interface_ipv6 = resolve('port_channel_interface_ipv6')
    l_0_port_channel_interfaces_isis = resolve('port_channel_interfaces_isis')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.list_compress']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.list_compress' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['arista.avd.range_expand']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.range_expand' found.")
    try:
        t_5 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_6 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_7 = environment.filters['map']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'map' found.")
    try:
        t_8 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_9 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    pass
    if t_8((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces)):
        pass
        yield '\n### Port-Channel Interfaces\n\n#### Port-Channel Interfaces Summary\n\n##### L2\n\n| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |\n| --------- | ----------- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |\n'
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            l_1_description = resolve('description')
            l_1_mode = resolve('mode')
            l_1_vlans = resolve('vlans')
            l_1_native_vlan = resolve('native_vlan')
            l_1_trunk_groups = resolve('trunk_groups')
            l_1_lacp_fallback_timeout = resolve('lacp_fallback_timeout')
            l_1_lacp_fallback_mode = resolve('lacp_fallback_mode')
            l_1_mlag = resolve('mlag')
            l_1_esi = resolve('esi')
            _loop_vars = {}
            pass
            if ((((((t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'mode')) or t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan'))) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan'))) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True)) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan'))) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'groups'))) and ((not t_8(environment.getattr(l_1_port_channel_interface, 'type'))) or (t_8(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') not in ['switched', 'routed'])))):
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_mode = t_1(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'mode'), '-')
                _loop_vars['mode'] = l_1_mode
                if (t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan')) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan'))):
                    pass
                    l_1_vlans = []
                    _loop_vars['vlans'] = l_1_vlans
                    if t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan')):
                        pass
                        context.call(environment.getattr((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans), 'append'), environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'access_vlan'), _loop_vars=_loop_vars)
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan')):
                        pass
                        context.call(environment.getattr((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans), 'extend'), t_7(context, t_4(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'allowed_vlan')), 'int'), _loop_vars=_loop_vars)
                    l_1_vlans = t_2((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans))
                    _loop_vars['vlans'] = l_1_vlans
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True):
                    pass
                    l_1_native_vlan = 'tag'
                    _loop_vars['native_vlan'] = l_1_native_vlan
                else:
                    pass
                    l_1_native_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'native_vlan'), '-')
                    _loop_vars['native_vlan'] = l_1_native_vlan
                l_1_trunk_groups = t_5(context.eval_ctx, t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'groups'), ['-']), ', ')
                _loop_vars['trunk_groups'] = l_1_trunk_groups
                l_1_lacp_fallback_timeout = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_timeout'), '-')
                _loop_vars['lacp_fallback_timeout'] = l_1_lacp_fallback_timeout
                l_1_lacp_fallback_mode = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_mode'), '-')
                _loop_vars['lacp_fallback_mode'] = l_1_lacp_fallback_mode
                l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                _loop_vars['mlag'] = l_1_mlag
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'identifier'), '-')
                _loop_vars['esi'] = l_1_esi
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str(t_1((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans), '-'))
                yield ' | '
                yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                yield ' | '
                yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                yield ' | '
                yield str((undefined(name='lacp_fallback_timeout') if l_1_lacp_fallback_timeout is missing else l_1_lacp_fallback_timeout))
                yield ' | '
                yield str((undefined(name='lacp_fallback_mode') if l_1_lacp_fallback_mode is missing else l_1_lacp_fallback_mode))
                yield ' | '
                yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' |\n'
            elif t_8(environment.getattr(l_1_port_channel_interface, 'type'), 'switched'):
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_mode = t_1(environment.getattr(l_1_port_channel_interface, 'mode'), '-')
                _loop_vars['mode'] = l_1_mode
                l_1_vlans = t_1(environment.getattr(l_1_port_channel_interface, 'vlans'), '-')
                _loop_vars['vlans'] = l_1_vlans
                if t_8(environment.getattr(l_1_port_channel_interface, 'native_vlan_tag'), True):
                    pass
                    l_1_native_vlan = 'tag'
                    _loop_vars['native_vlan'] = l_1_native_vlan
                else:
                    pass
                    l_1_native_vlan = t_1(environment.getattr(l_1_port_channel_interface, 'native_vlan'), '-')
                    _loop_vars['native_vlan'] = l_1_native_vlan
                l_1_trunk_groups = t_5(context.eval_ctx, t_1(environment.getattr(l_1_port_channel_interface, 'trunk_groups'), ['-']), ', ')
                _loop_vars['trunk_groups'] = l_1_trunk_groups
                l_1_lacp_fallback_timeout = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_timeout'), '-')
                _loop_vars['lacp_fallback_timeout'] = l_1_lacp_fallback_timeout
                l_1_lacp_fallback_mode = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_mode'), '-')
                _loop_vars['lacp_fallback_mode'] = l_1_lacp_fallback_mode
                l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                _loop_vars['mlag'] = l_1_mlag
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'identifier'), '-')
                _loop_vars['esi'] = l_1_esi
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans))
                yield ' | '
                yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                yield ' | '
                yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                yield ' | '
                yield str((undefined(name='lacp_fallback_timeout') if l_1_lacp_fallback_timeout is missing else l_1_lacp_fallback_timeout))
                yield ' | '
                yield str((undefined(name='lacp_fallback_mode') if l_1_lacp_fallback_mode is missing else l_1_lacp_fallback_mode))
                yield ' | '
                yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' |\n'
        l_1_port_channel_interface = l_1_description = l_1_mode = l_1_vlans = l_1_native_vlan = l_1_trunk_groups = l_1_lacp_fallback_timeout = l_1_lacp_fallback_mode = l_1_mlag = l_1_esi = missing
        l_0_encapsulation_dot1q_interfaces = []
        context.vars['encapsulation_dot1q_interfaces'] = l_0_encapsulation_dot1q_interfaces
        context.exported_vars.add('encapsulation_dot1q_interfaces')
        l_0_flexencap_interfaces = []
        context.vars['flexencap_interfaces'] = l_0_flexencap_interfaces
        context.exported_vars.add('flexencap_interfaces')
        for l_1_port_channel_interface in (undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces):
            _loop_vars = {}
            pass
            if (t_1(environment.getattr(l_1_port_channel_interface, 'type')) in ['l3dot1q', 'l2dot1q']):
                pass
                if t_8(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                elif t_8(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_6((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces)) > 0):
            pass
            yield '\n##### Encapsulation Dot1q\n\n| Interface | Description | Vlan ID | Dot1q VLAN Tag |\n| --------- | ----------- | ------- | -------------- |\n'
            for l_1_port_channel_interface in t_3((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'name'):
                l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_port_channel_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_encapsulation_dot1q_vlan = t_1(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan'), '-')
                _loop_vars['encapsulation_dot1q_vlan'] = l_1_encapsulation_dot1q_vlan
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='encapsulation_dot1q_vlan') if l_1_encapsulation_dot1q_vlan is missing else l_1_encapsulation_dot1q_vlan))
                yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = missing
        if (t_6((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces)) > 0):
            pass
            yield '\n##### Flexible Encapsulation Interfaces\n\n| Interface | Description | Vlan ID | Client Unmatched | Client Dot1q VLAN | Client Dot1q Outer Tag | Client Dot1q Inner Tag | Network Retain Client Encapsulation | Network Dot1q VLAN | Network Dot1q Outer Tag | Network Dot1q Inner Tag |\n| --------- | ----------- | ------- | -----------------| ----------------- | ---------------------- | ---------------------- | ----------------------------------- | ------------------ | ----------------------- | ----------------------- |\n'
            for l_1_port_channel_interface in t_3((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'name'):
                l_1_description = l_1_vlan_id = l_1_client_unmatched = l_1_client_dot1q_vlan = l_1_client_dot1q_outer = l_1_client_dot1q_inner = l_1_network_client = l_1_network_dot1q_vlan = l_1_network_dot1q_outer = l_1_network_dot1q_inner = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_port_channel_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_client_unmatched = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'unmatched'), False)
                _loop_vars['client_unmatched'] = l_1_client_unmatched
                l_1_client_dot1q_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan'), '-')
                _loop_vars['client_dot1q_vlan'] = l_1_client_dot1q_vlan
                l_1_client_dot1q_outer = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'), '-')
                _loop_vars['client_dot1q_outer'] = l_1_client_dot1q_outer
                l_1_client_dot1q_inner = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner'), '-')
                _loop_vars['client_dot1q_inner'] = l_1_client_dot1q_inner
                l_1_network_client = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'client'), False)
                _loop_vars['network_client'] = l_1_network_client
                l_1_network_dot1q_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan'), '-')
                _loop_vars['network_dot1q_vlan'] = l_1_network_dot1q_vlan
                l_1_network_dot1q_outer = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'), '-')
                _loop_vars['network_dot1q_outer'] = l_1_network_dot1q_outer
                l_1_network_dot1q_inner = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner'), '-')
                _loop_vars['network_dot1q_inner'] = l_1_network_dot1q_inner
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='client_unmatched') if l_1_client_unmatched is missing else l_1_client_unmatched))
                yield ' | '
                yield str((undefined(name='client_dot1q_vlan') if l_1_client_dot1q_vlan is missing else l_1_client_dot1q_vlan))
                yield ' | '
                yield str((undefined(name='client_dot1q_outer') if l_1_client_dot1q_outer is missing else l_1_client_dot1q_outer))
                yield ' | '
                yield str((undefined(name='client_dot1q_inner') if l_1_client_dot1q_inner is missing else l_1_client_dot1q_inner))
                yield ' | '
                yield str((undefined(name='network_client') if l_1_network_client is missing else l_1_network_client))
                yield ' | '
                yield str((undefined(name='network_dot1q_vlan') if l_1_network_dot1q_vlan is missing else l_1_network_dot1q_vlan))
                yield ' | '
                yield str((undefined(name='network_dot1q_outer') if l_1_network_dot1q_outer is missing else l_1_network_dot1q_outer))
                yield ' | '
                yield str((undefined(name='network_dot1q_inner') if l_1_network_dot1q_inner is missing else l_1_network_dot1q_inner))
                yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_vlan_id = l_1_client_unmatched = l_1_client_dot1q_vlan = l_1_client_dot1q_outer = l_1_client_dot1q_inner = l_1_network_client = l_1_network_dot1q_vlan = l_1_network_dot1q_outer = l_1_network_dot1q_inner = missing
        l_0_port_channel_interface_pvlan = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_pvlan'] = l_0_port_channel_interface_pvlan
        context.exported_vars.add('port_channel_interface_pvlan')
        if not isinstance(l_0_port_channel_interface_pvlan, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_pvlan['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (((t_8(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping')) or t_8(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'))) or t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'pvlan_mapping'))) or t_8(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'))):
                pass
                if not isinstance(l_0_port_channel_interface_pvlan, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_pvlan['configured'] = True
                break
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_pvlan') if l_0_port_channel_interface_pvlan is missing else l_0_port_channel_interface_pvlan), 'configured'):
            pass
            yield '\n##### Private VLAN\n\n| Interface | PVLAN Mapping | Secondary Trunk |\n| --------- | ------------- | ----------------|\n'
            for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_row_pvlan_mapping = l_1_row_trunk_private_vlan_secondary = missing
                _loop_vars = {}
                pass
                l_1_row_pvlan_mapping = t_1(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'pvlan_mapping'), environment.getattr(l_1_port_channel_interface, 'pvlan_mapping'), '-')
                _loop_vars['row_pvlan_mapping'] = l_1_row_pvlan_mapping
                l_1_row_trunk_private_vlan_secondary = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'), environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'), '-')
                _loop_vars['row_trunk_private_vlan_secondary'] = l_1_row_trunk_private_vlan_secondary
                if (((undefined(name='row_pvlan_mapping') if l_1_row_pvlan_mapping is missing else l_1_row_pvlan_mapping) != '-') or ((undefined(name='row_trunk_private_vlan_secondary') if l_1_row_trunk_private_vlan_secondary is missing else l_1_row_trunk_private_vlan_secondary) != '-')):
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='row_pvlan_mapping') if l_1_row_pvlan_mapping is missing else l_1_row_pvlan_mapping))
                    yield ' | '
                    yield str((undefined(name='row_trunk_private_vlan_secondary') if l_1_row_trunk_private_vlan_secondary is missing else l_1_row_trunk_private_vlan_secondary))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_row_pvlan_mapping = l_1_row_trunk_private_vlan_secondary = missing
        l_0_port_channel_interface_vlan_xlate = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_vlan_xlate'] = l_0_port_channel_interface_vlan_xlate
        context.exported_vars.add('port_channel_interface_vlan_xlate')
        if not isinstance(l_0_port_channel_interface_vlan_xlate, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_vlan_xlate['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations')) or t_8(environment.getattr(l_1_port_channel_interface, 'vlan_translations'))):
                pass
                if not isinstance(l_0_port_channel_interface_vlan_xlate, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_vlan_xlate['configured'] = True
                break
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_vlan_xlate') if l_0_port_channel_interface_vlan_xlate is missing else l_0_port_channel_interface_vlan_xlate), 'configured'):
            pass
            yield '\n##### VLAN Translations\n\n| Interface |  Direction | From VLAN ID(s) | To VLAN ID | From Inner VLAN ID | To Inner VLAN ID | Network | Dot1q-tunnel |\n| --------- |  --------- | --------------- | ---------- | ------------------ | ---------------- | ------- | ------------ |\n'
            for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations')):
                    pass
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_both'), 'from'):
                        _loop_vars = {}
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                        yield ' | both | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str(environment.getattr(l_2_vlan_translation, 'to'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), '-'))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = missing
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_in'), 'from'):
                        _loop_vars = {}
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                        yield ' | in | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str(environment.getattr(l_2_vlan_translation, 'to'))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = missing
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'switchport'), 'vlan_translations'), 'direction_out'), 'from'):
                        l_2_dot1q_tunnel = resolve('dot1q_tunnel')
                        l_2_to_vlan_id = resolve('to_vlan_id')
                        _loop_vars = {}
                        pass
                        if t_8(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')):
                            pass
                            l_2_dot1q_tunnel = 'True'
                            _loop_vars['dot1q_tunnel'] = l_2_dot1q_tunnel
                            l_2_to_vlan_id = environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')
                            _loop_vars['to_vlan_id'] = l_2_to_vlan_id
                        else:
                            pass
                            l_2_to_vlan_id = t_1(environment.getattr(l_2_vlan_translation, 'to'), '-')
                            _loop_vars['to_vlan_id'] = l_2_to_vlan_id
                        yield '| '
                        yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                        yield ' | out | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str((undefined(name='to_vlan_id') if l_2_to_vlan_id is missing else l_2_to_vlan_id))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_to'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1((undefined(name='dot1q_tunnel') if l_2_dot1q_tunnel is missing else l_2_dot1q_tunnel), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = l_2_dot1q_tunnel = l_2_to_vlan_id = missing
                elif t_8(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
                    pass
                    for l_2_vlan_translation in t_3(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
                        l_2_row_direction = resolve('row_direction')
                        _loop_vars = {}
                        pass
                        if (t_8(environment.getattr(l_2_vlan_translation, 'from')) and t_8(environment.getattr(l_2_vlan_translation, 'to'))):
                            pass
                            l_2_row_direction = t_1(environment.getattr(l_2_vlan_translation, 'direction'), 'both')
                            _loop_vars['row_direction'] = l_2_row_direction
                            yield '| '
                            yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                            yield ' | '
                            yield str((undefined(name='row_direction') if l_2_row_direction is missing else l_2_row_direction))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'from'))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'to'))
                            yield ' | - | - | - | - |\n'
                    l_2_vlan_translation = l_2_row_direction = missing
            l_1_port_channel_interface = missing
        l_0_evpn_es_po_interfaces = []
        context.vars['evpn_es_po_interfaces'] = l_0_evpn_es_po_interfaces
        context.exported_vars.add('evpn_es_po_interfaces')
        l_0_evpn_dfe_po_interfaces = []
        context.vars['evpn_dfe_po_interfaces'] = l_0_evpn_dfe_po_interfaces
        context.exported_vars.add('evpn_dfe_po_interfaces')
        l_0_evpn_mpls_po_interfaces = []
        context.vars['evpn_mpls_po_interfaces'] = l_0_evpn_mpls_po_interfaces
        context.exported_vars.add('evpn_mpls_po_interfaces')
        l_0_link_tracking_interfaces = []
        context.vars['link_tracking_interfaces'] = l_0_link_tracking_interfaces
        context.exported_vars.add('link_tracking_interfaces')
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment')):
                pass
                context.call(environment.getattr((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                if t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                if t_8(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
            if t_8(environment.getattr(l_1_port_channel_interface, 'link_tracking_groups')):
                pass
                context.call(environment.getattr((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_6((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces)) > 0):
            pass
            yield '\n##### EVPN Multihoming\n\n####### EVPN Multihoming Summary\n\n| Interface | Ethernet Segment Identifier | Multihoming Redundancy Mode | Route Target |\n| --------- | --------------------------- | --------------------------- | ------------ |\n'
            for l_1_evpn_es_po_interface in t_3((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces), 'name'):
                l_1_esi = l_1_redundancy = l_1_rt = missing
                _loop_vars = {}
                pass
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'identifier'), environment.getattr(l_1_evpn_es_po_interface, 'esi'), '-')
                _loop_vars['esi'] = l_1_esi
                l_1_redundancy = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'redundancy'), 'all-active')
                _loop_vars['redundancy'] = l_1_redundancy
                l_1_rt = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'route_target'), '-')
                _loop_vars['rt'] = l_1_rt
                yield '| '
                yield str(environment.getattr(l_1_evpn_es_po_interface, 'name'))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' | '
                yield str((undefined(name='redundancy') if l_1_redundancy is missing else l_1_redundancy))
                yield ' | '
                yield str((undefined(name='rt') if l_1_rt is missing else l_1_rt))
                yield ' |\n'
            l_1_evpn_es_po_interface = l_1_esi = l_1_redundancy = l_1_rt = missing
            if (t_6((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces)) > 0):
                pass
                yield '\n####### Designated Forwarder Election Summary\n\n| Interface | Algorithm | Preference Value | Dont Preempt | Hold time | Subsequent Hold Time | Candidate Reachability Required |\n| --------- | --------- | ---------------- | ------------ | --------- | -------------------- | ------------------------------- |\n'
                for l_1_evpn_dfe_po_interface in t_3((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces), 'name'):
                    l_1_df_po_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
                    _loop_vars = {}
                    pass
                    l_1_df_po_settings = environment.getattr(environment.getattr(l_1_evpn_dfe_po_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')
                    _loop_vars['df_po_settings'] = l_1_df_po_settings
                    l_1_algorithm = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'algorithm'), 'modulus')
                    _loop_vars['algorithm'] = l_1_algorithm
                    l_1_pref_value = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'preference_value'), '-')
                    _loop_vars['pref_value'] = l_1_pref_value
                    l_1_dont_preempt = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'dont_preempt'), False)
                    _loop_vars['dont_preempt'] = l_1_dont_preempt
                    l_1_hold_time = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'hold_time'), '-')
                    _loop_vars['hold_time'] = l_1_hold_time
                    l_1_subsequent_hold_time = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'subsequent_hold_time'), '-')
                    _loop_vars['subsequent_hold_time'] = l_1_subsequent_hold_time
                    l_1_candidate_reachability = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'candidate_reachability_required'), False)
                    _loop_vars['candidate_reachability'] = l_1_candidate_reachability
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_dfe_po_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='algorithm') if l_1_algorithm is missing else l_1_algorithm))
                    yield ' | '
                    yield str((undefined(name='pref_value') if l_1_pref_value is missing else l_1_pref_value))
                    yield ' | '
                    yield str((undefined(name='dont_preempt') if l_1_dont_preempt is missing else l_1_dont_preempt))
                    yield ' | '
                    yield str((undefined(name='hold_time') if l_1_hold_time is missing else l_1_hold_time))
                    yield ' | '
                    yield str((undefined(name='subsequent_hold_time') if l_1_subsequent_hold_time is missing else l_1_subsequent_hold_time))
                    yield ' | '
                    yield str((undefined(name='candidate_reachability') if l_1_candidate_reachability is missing else l_1_candidate_reachability))
                    yield ' |\n'
                l_1_evpn_dfe_po_interface = l_1_df_po_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
            if (t_6((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces)) > 0):
                pass
                yield '\n####### EVPN-MPLS summary\n\n| Interface | Shared Index | Tunnel Flood Filter Time |\n| --------- | ------------ | ------------------------ |\n'
                for l_1_evpn_mpls_po_interface in t_3((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces)):
                    l_1_shared_index = l_1_tff_time = missing
                    _loop_vars = {}
                    pass
                    l_1_shared_index = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_po_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index'), '-')
                    _loop_vars['shared_index'] = l_1_shared_index
                    l_1_tff_time = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_po_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time'), '-')
                    _loop_vars['tff_time'] = l_1_tff_time
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_mpls_po_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='shared_index') if l_1_shared_index is missing else l_1_shared_index))
                    yield ' | '
                    yield str((undefined(name='tff_time') if l_1_tff_time is missing else l_1_tff_time))
                    yield ' |\n'
                l_1_evpn_mpls_po_interface = l_1_shared_index = l_1_tff_time = missing
        if (t_6((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces)) > 0):
            pass
            yield '\n##### Link Tracking Groups\n\n| Interface | Group Name | Direction |\n| --------- | ---------- | --------- |\n'
            for l_1_link_tracking_interface in t_3((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces), 'name'):
                _loop_vars = {}
                pass
                for l_2_link_tracking_group in t_3(environment.getattr(l_1_link_tracking_interface, 'link_tracking_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    if (t_8(environment.getattr(l_2_link_tracking_group, 'name')) and t_8(environment.getattr(l_2_link_tracking_group, 'direction'))):
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_link_tracking_interface, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'direction'))
                        yield ' |\n'
                l_2_link_tracking_group = missing
            l_1_link_tracking_interface = missing
        l_0_port_channel_interface_ipv4 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv4'] = l_0_port_channel_interface_ipv4
        context.exported_vars.add('port_channel_interface_ipv4')
        if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv4['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((t_9(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_9(environment.getattr(l_1_port_channel_interface, 'ip_address'))):
                pass
                if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv4['configured'] = True
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_ipv4') if l_0_port_channel_interface_ipv4 is missing else l_0_port_channel_interface_ipv4), 'configured'):
            pass
            yield '\n##### IPv4\n\n| Interface | Description | MLAG ID | IP Address | VRF | MTU | Shutdown | ACL In | ACL Out |\n| --------- | ----------- | ------- | ---------- | --- | --- | -------- | ------ | ------- |\n'
            for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_description = resolve('description')
                l_1_mlag = resolve('mlag')
                l_1_ip_address = resolve('ip_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_acl_in = resolve('acl_in')
                l_1_acl_out = resolve('acl_out')
                _loop_vars = {}
                pass
                if ((t_9(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_8(environment.getattr(l_1_port_channel_interface, 'ip_address'))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                    _loop_vars['mlag'] = l_1_mlag
                    l_1_ip_address = t_1(environment.getattr(l_1_port_channel_interface, 'ip_address'), '-')
                    _loop_vars['ip_address'] = l_1_ip_address
                    l_1_vrf = t_1(environment.getattr(l_1_port_channel_interface, 'vrf'), 'default')
                    _loop_vars['vrf'] = l_1_vrf
                    l_1_mtu = t_1(environment.getattr(l_1_port_channel_interface, 'mtu'), '-')
                    _loop_vars['mtu'] = l_1_mtu
                    l_1_shutdown = t_1(environment.getattr(l_1_port_channel_interface, 'shutdown'), '-')
                    _loop_vars['shutdown'] = l_1_shutdown
                    l_1_acl_in = t_1(environment.getattr(l_1_port_channel_interface, 'access_group_in'), '-')
                    _loop_vars['acl_in'] = l_1_acl_in
                    l_1_acl_out = t_1(environment.getattr(l_1_port_channel_interface, 'access_group_out'), '-')
                    _loop_vars['acl_out'] = l_1_acl_out
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                    yield ' | '
                    yield str((undefined(name='ip_address') if l_1_ip_address is missing else l_1_ip_address))
                    yield ' | '
                    yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                    yield ' | '
                    yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                    yield ' | '
                    yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                    yield ' | '
                    yield str((undefined(name='acl_in') if l_1_acl_in is missing else l_1_acl_in))
                    yield ' | '
                    yield str((undefined(name='acl_out') if l_1_acl_out is missing else l_1_acl_out))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_mlag = l_1_ip_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_acl_in = l_1_acl_out = missing
        l_0_ip_nat_interfaces = (undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces)
        context.vars['ip_nat_interfaces'] = l_0_ip_nat_interfaces
        context.exported_vars.add('ip_nat_interfaces')
        template = environment.get_template('documentation/interfaces-ip-nat.j2', 'documentation/port-channel-interfaces.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'evpn_dfe_po_interfaces': l_0_evpn_dfe_po_interfaces, 'evpn_es_po_interfaces': l_0_evpn_es_po_interfaces, 'evpn_mpls_po_interfaces': l_0_evpn_mpls_po_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interface_pvlan': l_0_port_channel_interface_pvlan, 'port_channel_interface_vlan_xlate': l_0_port_channel_interface_vlan_xlate, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis})):
            yield event
        l_0_port_channel_interface_ipv6 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv6'] = l_0_port_channel_interface_ipv6
        context.exported_vars.add('port_channel_interface_ipv6')
        if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv6['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((t_9(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_9(environment.getattr(l_1_port_channel_interface, 'ipv6_address'))):
                pass
                if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv6['configured'] = True
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_ipv6') if l_0_port_channel_interface_ipv6 is missing else l_0_port_channel_interface_ipv6), 'configured'):
            pass
            yield '\n##### IPv6\n\n| Interface | Description | MLAG ID | IPv6 Address | VRF | MTU | Shutdown | ND RA Disabled | Managed Config Flag | IPv6 ACL In | IPv6 ACL Out |\n| --------- | ----------- | ------- | -------------| --- | --- | -------- | -------------- | ------------------- | ----------- | ------------ |\n'
            for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_description = resolve('description')
                l_1_mlag = resolve('mlag')
                l_1_ipv6_address = resolve('ipv6_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_ipv6_nd_ra_disabled = resolve('ipv6_nd_ra_disabled')
                l_1_ipv6_nd_managed_config_flag = resolve('ipv6_nd_managed_config_flag')
                l_1_ipv6_acl_in = resolve('ipv6_acl_in')
                l_1_ipv6_acl_out = resolve('ipv6_acl_out')
                _loop_vars = {}
                pass
                if ((t_9(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_8(environment.getattr(l_1_port_channel_interface, 'ipv6_address'))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                    _loop_vars['mlag'] = l_1_mlag
                    l_1_ipv6_address = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_address'), '-')
                    _loop_vars['ipv6_address'] = l_1_ipv6_address
                    l_1_vrf = t_1(environment.getattr(l_1_port_channel_interface, 'vrf'), 'default')
                    _loop_vars['vrf'] = l_1_vrf
                    l_1_mtu = t_1(environment.getattr(l_1_port_channel_interface, 'mtu'), '-')
                    _loop_vars['mtu'] = l_1_mtu
                    l_1_shutdown = t_1(environment.getattr(l_1_port_channel_interface, 'shutdown'), '-')
                    _loop_vars['shutdown'] = l_1_shutdown
                    l_1_ipv6_nd_ra_disabled = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_ra_disabled'), '-')
                    _loop_vars['ipv6_nd_ra_disabled'] = l_1_ipv6_nd_ra_disabled
                    if t_8(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_managed_config_flag')):
                        pass
                        l_1_ipv6_nd_managed_config_flag = environment.getattr(l_1_port_channel_interface, 'ipv6_nd_managed_config_flag')
                        _loop_vars['ipv6_nd_managed_config_flag'] = l_1_ipv6_nd_managed_config_flag
                    else:
                        pass
                        l_1_ipv6_nd_managed_config_flag = '-'
                        _loop_vars['ipv6_nd_managed_config_flag'] = l_1_ipv6_nd_managed_config_flag
                    l_1_ipv6_acl_in = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_in'), '-')
                    _loop_vars['ipv6_acl_in'] = l_1_ipv6_acl_in
                    l_1_ipv6_acl_out = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_out'), '-')
                    _loop_vars['ipv6_acl_out'] = l_1_ipv6_acl_out
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                    yield ' | '
                    yield str((undefined(name='ipv6_address') if l_1_ipv6_address is missing else l_1_ipv6_address))
                    yield ' | '
                    yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                    yield ' | '
                    yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                    yield ' | '
                    yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                    yield ' | '
                    yield str((undefined(name='ipv6_nd_ra_disabled') if l_1_ipv6_nd_ra_disabled is missing else l_1_ipv6_nd_ra_disabled))
                    yield ' | '
                    yield str((undefined(name='ipv6_nd_managed_config_flag') if l_1_ipv6_nd_managed_config_flag is missing else l_1_ipv6_nd_managed_config_flag))
                    yield ' | '
                    yield str((undefined(name='ipv6_acl_in') if l_1_ipv6_acl_in is missing else l_1_ipv6_acl_in))
                    yield ' | '
                    yield str((undefined(name='ipv6_acl_out') if l_1_ipv6_acl_out is missing else l_1_ipv6_acl_out))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_mlag = l_1_ipv6_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_ipv6_nd_ra_disabled = l_1_ipv6_nd_managed_config_flag = l_1_ipv6_acl_in = l_1_ipv6_acl_out = missing
        l_0_port_channel_interfaces_isis = []
        context.vars['port_channel_interfaces_isis'] = l_0_port_channel_interfaces_isis
        context.exported_vars.add('port_channel_interfaces_isis')
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (((((((t_8(environment.getattr(l_1_port_channel_interface, 'isis_enable')) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_bfd'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_metric'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_passive'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'))) or t_8(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'))):
                pass
                context.call(environment.getattr((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_6((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis)) > 0):
            pass
            yield '\n##### ISIS\n\n| Interface | ISIS Instance | ISIS BFD | ISIS Metric | Mode | ISIS Circuit Type | Hello Padding | Authentication Mode |\n| --------- | ------------- | -------- | ----------- | ---- | ----------------- | ------------- | ------------------- |\n'
            for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'name'):
                l_1_isis_instance = l_1_isis_bfd = l_1_isis_metric = l_1_isis_circuit_type = l_1_isis_hello_padding = l_1_isis_authentication_mode = l_1_mode = missing
                _loop_vars = {}
                pass
                l_1_isis_instance = t_1(environment.getattr(l_1_port_channel_interface, 'isis_enable'), '-')
                _loop_vars['isis_instance'] = l_1_isis_instance
                l_1_isis_bfd = t_1(environment.getattr(l_1_port_channel_interface, 'isis_bfd'), '-')
                _loop_vars['isis_bfd'] = l_1_isis_bfd
                l_1_isis_metric = t_1(environment.getattr(l_1_port_channel_interface, 'isis_metric'), '-')
                _loop_vars['isis_metric'] = l_1_isis_metric
                l_1_isis_circuit_type = t_1(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'), '-')
                _loop_vars['isis_circuit_type'] = l_1_isis_circuit_type
                l_1_isis_hello_padding = t_1(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'), '-')
                _loop_vars['isis_hello_padding'] = l_1_isis_hello_padding
                l_1_isis_authentication_mode = t_1(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'), '-')
                _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                if t_8(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'), True):
                    pass
                    l_1_mode = 'point-to-point'
                    _loop_vars['mode'] = l_1_mode
                elif t_8(environment.getattr(l_1_port_channel_interface, 'isis_passive'), True):
                    pass
                    l_1_mode = 'passive'
                    _loop_vars['mode'] = l_1_mode
                else:
                    pass
                    l_1_mode = '-'
                    _loop_vars['mode'] = l_1_mode
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='isis_instance') if l_1_isis_instance is missing else l_1_isis_instance))
                yield ' | '
                yield str((undefined(name='isis_bfd') if l_1_isis_bfd is missing else l_1_isis_bfd))
                yield ' | '
                yield str((undefined(name='isis_metric') if l_1_isis_metric is missing else l_1_isis_metric))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str((undefined(name='isis_circuit_type') if l_1_isis_circuit_type is missing else l_1_isis_circuit_type))
                yield ' | '
                yield str((undefined(name='isis_hello_padding') if l_1_isis_hello_padding is missing else l_1_isis_hello_padding))
                yield ' | '
                yield str((undefined(name='isis_authentication_mode') if l_1_isis_authentication_mode is missing else l_1_isis_authentication_mode))
                yield ' |\n'
            l_1_port_channel_interface = l_1_isis_instance = l_1_isis_bfd = l_1_isis_metric = l_1_isis_circuit_type = l_1_isis_hello_padding = l_1_isis_authentication_mode = l_1_mode = missing
        yield '\n#### Port-Channel Interfaces Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/port-channel-interfaces.j2', 'documentation/port-channel-interfaces.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'evpn_dfe_po_interfaces': l_0_evpn_dfe_po_interfaces, 'evpn_es_po_interfaces': l_0_evpn_es_po_interfaces, 'evpn_mpls_po_interfaces': l_0_evpn_mpls_po_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interface_pvlan': l_0_port_channel_interface_pvlan, 'port_channel_interface_vlan_xlate': l_0_port_channel_interface_vlan_xlate, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=79&17=82&20=94&27=96&28=98&29=100&31=102&32=104&33=106&35=107&36=109&38=110&40=112&41=114&43=118&45=120&46=122&47=124&48=126&49=128&50=131&52=151&53=153&54=155&55=157&56=159&57=161&59=165&61=167&62=169&63=171&64=173&65=175&66=178&70=199&71=202&72=205&73=208&74=210&75=212&76=213&77=215&81=217&87=220&88=224&89=226&90=228&91=231&94=240&100=243&101=247&102=249&103=251&104=253&105=255&106=257&107=259&108=261&109=263&110=265&111=268&115=291&116=294&117=297&118=300&122=302&123=305&126=307&132=310&133=314&134=316&135=318&136=321&141=328&142=331&143=334&144=337&146=339&147=342&150=344&156=347&157=350&158=352&159=356&161=369&162=373&164=386&165=391&166=393&167=395&169=399&171=402&173=415&174=417&175=421&176=423&177=426&184=436&185=439&186=442&187=445&188=448&189=451&190=453&191=454&192=456&194=457&195=459&198=460&199=462&203=464&211=467&212=471&213=473&214=475&215=478&217=487&223=490&224=494&225=496&226=498&227=500&228=502&229=504&230=506&231=509&234=524&240=527&241=531&242=533&243=536&248=543&254=546&255=549&256=552&257=555&263=563&264=566&265=569&266=572&267=574&270=578&276=581&277=592&278=594&279=596&280=598&281=600&282=602&283=604&284=606&285=608&286=611&291=630&292=633&294=636&295=639&296=642&297=645&298=647&301=651&307=654&308=667&309=669&310=671&311=673&312=675&313=677&314=679&315=681&316=683&317=685&319=689&321=691&322=693&323=696&328=719&329=722&330=725&338=727&341=729&347=732&348=736&349=738&350=740&351=742&352=744&353=746&354=748&355=750&356=752&357=754&359=758&361=761&368=779'