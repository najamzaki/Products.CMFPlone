from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.interfaces.PloneBaseTool import IPloneBaseTool
from Products.CMFPlone.utils import classImplements
from Acquisition import aq_base
from Acquisition import aq_parent
from Acquisition import aq_inner

TempFolderClass = None

# getOAI() and getExprContext copied from CMF 1.5.1+cvs
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
# ZPL 2.1
from Products.CMFCore.ActionInformation import oai
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.utils import getToolByName

def initializeTFC():
    """To work around circular imports ...
    """
    global TempFolderClass
    if TempFolderClass is None:
         from Products.CMFPlone.FactoryTool import TempFolder
         TempFolderClass = TempFolder

def getOAI(context, object=None):
    initializeTFC()
    request = getattr(context, 'REQUEST', None)
    if request:
        cache = request.get('_oai_cache', None)
        if cache is None:
            request['_oai_cache'] = cache = {}
        info = cache.get( id(object), None )
    else:
        info = None
    if info is None:
        if object is None or not hasattr(object, 'aq_base'):
            folder = None
        else:
            folder = object
            # Search up the containment hierarchy until we find an
            # object that claims it's a folder.
            while folder is not None:
                if getattr(aq_base(folder), 'isPrincipiaFolderish', 0):
                    # found it.
                    break
                else:
                    # If the parent of the object at hand is a TempFolder
                    # don't strip off its outer acquisition context (Plone)
                    parent = aq_parent(aq_inner(folder))
                    if getattr(parent, '__class__', None) == TempFolderClass:
                        folder = aq_parent(folder)
                    else:
                        folder = parent
        info = oai(context, folder, object)
        if request:
            cache[ id(object) ] = info
    return info

def getExprContext(context, object=None):
    initializeTFC()
    request = getattr(context, 'REQUEST', None)
    if request:
        cache = request.get('_ec_cache', None)
        if cache is None:
            request['_ec_cache'] = cache = {}
        ec = cache.get( id(object), None )
    else:
        ec = None
    if ec is None:
        utool = getToolByName(context, 'portal_url')
        portal = utool.getPortalObject()
        if object is None or not hasattr(object, 'aq_base'):
            folder = portal
        else:
            folder = object
            # Search up the containment hierarchy until we find an
            # object that claims it's a folder.
            while folder is not None:
                if getattr(aq_base(folder), 'isPrincipiaFolderish', 0):
                    # found it.
                    break
                else:
                    # If the parent of the object at hand is a TempFolder
                    # don't strip off its outer acquisition context (Plone)
                    parent = aq_parent(aq_inner(folder))
                    if getattr(parent, '__class__', None) == TempFolderClass:
                        folder = aq_parent(folder)
                    else:
                        folder = parent
        ec = createExprContext(folder, portal, object)
        if request:
            cache[ id(object) ] = ec
    return ec

class PloneBaseTool:
    """Base class of all tools used in CMFPlone and Plone Core
    """

    security = ClassSecurityInfo()

    __implements__ = IPloneBaseTool

    # overwrite getOAI and getExprContext to use our variants that understand the
    # temp folder of portal factory
    def _getOAI(self, object):
        return getOAI(self, object)

    def _getExprContext(self, object):
        return getExprContext(self, object)

classImplements(PloneBaseTool, PloneBaseTool.__implements__)
InitializeClass(PloneBaseTool)
