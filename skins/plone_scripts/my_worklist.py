## Script (Python) "my_worklist"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=time=None
##title=
##

if context.portal_membership.isAnonymousUser():
    return []

wf_wlist_map = context.getWorklists() #getWorklists is currently a external method ;(
catalog=context.portal_catalog
avail_objs = []

for wlist_map_sequence in wf_wlist_map.values():
    for wlist_map in wlist_map_sequence:
        permission=wlist_map['guard_permissions']
        catalog_vars=wlist_map['catalog_vars']
        for result in catalog.searchResults(catalog_vars):
	    o = results.getObject()
	    if context.portal_membership.checkPermission(permission, o) and \
                o.absolute_url() not in [a.absolute_url() for a in avail_objs] :
                avail_objs.append(o)

return context.sort_modified_ascending(avail_objs)

