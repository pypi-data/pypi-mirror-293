# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: A =CS-Unit= as equivalent of facter in py and remotely with rpyc.
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+BEGIN_SRC emacs-lisp
(setq-local b:dblockControls t) ; (setq-local b:dblockControls nil)
(put 'b:dblockControls 'py3:cs:Classification "cs-u") ; one of cs-mu, cs-u, cs-lib, bpf-lib, pyLibPure
#+END_SRC
#+RESULTS:
: cs-u
#+end_org """
####+END:

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
** Best read and edited  with Blee in Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/facter/py3/bisos/facter/facter_csu.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['facter_csu'], }
csInfo['version'] = '202403270908'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'facter_csu-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/COMEEGA/_nodeBase_/fullUsagePanel-en.org][BISOS COMEEGA Panel]]
This a =Cs-Unit= for running the equivalent of facter in py and remotely with rpyc.
With BISOS, it is used in CMDB remotely.

** Relevant Panels:
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]

#+end_org """
####+END:

####+BEGIN: b:py3:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:orgItem/basic :type "=PyImports= "  :title "*Py Library IMPORTS*" :comment "-- Framework and External Packages Imports"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS* -- Framework and External Packages Imports  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

# import os
import collections
# import pathlib
# import invoke

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
** Imports Based On Classification=cs-u
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

from gi.repository import Gio,GLib

import pathlib

####+BEGIN: b:py3:cs:orgItem/basic :type "=Executes=  "  :title "CSU-Lib Executions" :comment "-- cs.invOutcomeReportControl"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Executes=   [[elisp:(outline-show-subtree+toggle)][||]] CSU-Lib Executions -- cs.invOutcomeReportControl  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

g_rosmu = cs.G.icmMyName()

cs.invOutcomeReportControl(cmnd=True, ro=True)

####+BEGIN: b:py3:cs:orgItem/section :title "Common Parameters Specification" :comment "based on cs.param.CmndParamDict -- As expected from CSU-s"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Common Parameters Specification* based on cs.param.CmndParamDict -- As expected from CSU-s  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:func/typing :funcName "commonParamsSpecify" :comment "~CSU Specification~" :funcType "ParSpc" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-ParSpc [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/  ~CSU Specification~  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
####+END:
        csParams: cs.param.CmndParamDict,
) -> None:
    pass

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Direct Command Services" :anchor ""  :extraInfo "Examples and CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Direct Command Services_: |]]  Examples and CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "examples_csu" :comment "" :parsMand "" :parsOpt "perfName" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<examples_csu>>  =verify= parsOpt=perfName ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class examples_csu(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ 'perfName', ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             perfName: typing.Optional[str]=None,  # Cs Optional Param
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {'perfName': perfName, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
        perfName = csParam.mappedValue('perfName', perfName)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Basic example command.
        #+end_org """)

        od = collections.OrderedDict
        cmnd = cs.examples.cmndEnter
        literal = cs.examples.execInsert

        cs.examples.menuChapter('Discover Schema and Key Values')

        literal("gsettings list-recursively > /tmp/gsettings.before")
        literal("echo then run gnome-tweaks or gnome-extensions-app")
        literal("gsettings list-recursively > /tmp/gsettings.after")
        literal("diff /tmp/gsettings.before /tmp/gsettings.after")
        
        cs.examples.menuChapter('Favorite Apps -- Get, Set, Add, Remove')

        cmnd('favoriteApps_get',  comment=" # As list of strings")
        cmnd('favoriteApps_set', args='''"['firefox-esr.desktop', 'google-chrome.desktop', 'org.gnome.Evolution.desktop', 'libreoffice-writer.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Software.desktop', 'yelp.desktop']"''', comment=" # As list of strings")
        cmnd('favoriteApps_remove',  comment=" # As list of strings")
        cmnd('favoriteApps_addAfter',  comment=" # As list of strings")
        cmnd('favoriteApps_append',  comment=" # As list of strings")

        cs.examples.menuChapter('Enabled Extensions -- Get, Set, Add, Remove')

        cmnd('extensionsEnabled_get',  comment=" # As list of strings")
        cmnd('extensionsEnabled_set',  comment=" # As list of strings")
        cmnd('extensionsEnabled_remove',  comment=" # As list of strings")
        cmnd('extensionsEnabled_add',  comment=" # As list of strings")

        cs.examples.menuChapter('Gnome Tweaks -- Get, Set')

        cmnd('general_overAmplification', args='get', comment=" # As list of strings")
        cmnd('general_overAmplification', args='true', comment=" # As list of strings")
        cmnd('general_overAmplification', args='false', comment=" # As list of strings")

        cmnd('windowsTitlebars_minAndMax', args='get', comment=" # As list of strings")
        cmnd('windowsTitlebars_minAndMax', args='on', comment=" # As list of strings")
        cmnd('windowsTitlebars_minAndMax', args='off', comment=" # As list of strings")

        cmnd('windowsTitlebars_maximize', args='get', comment=" # OBSOLETED")
        cmnd('windowsTitlebars_maximize', args='on', comment=" # OBSOLETED")
        cmnd('windowsTitlebars_maximize', args='off', comment=" # OBSOLETED")

        cmnd('windowsTitlebars_minimize', args='get', comment=" # OBSOLETED")
        cmnd('windowsTitlebars_minimize', args='on', comment=" # OBSOLETED")
        cmnd('windowsTitlebars_minimize', args='off', comment=" # OBSOLETED")

        cs.examples.menuChapter('Dash-to-Panel Customization -- Select')

        cmnd('dashToPanelCustomize', args='get', comment=" # As list of strings")
        cmnd('dashToPanelCustomize', args='rawBisos', comment=" # As list of strings")

        cs.examples.menuChapter('Desktop Background -- Select')

        cmnd('desktopBackground', args='get', comment=" # As list of strings")
        cmnd('desktopBackground', args='freshDebian', comment=" # As list of strings")
        cmnd('desktopBackground', args='rawBisos', comment=" # As list of strings")

        cs.examples.menuChapter('=Raw Command Examples=')

        literal("gnomeBisos.cs")

        return(cmndOutcome)


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Favorite Apps" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Favorite Apps_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteApps_get" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteApps_get>>  =verify= ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteApps_get(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns runFacterAndGetJsonOutputBytes.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i favoriteApps_get
#+end_src
#+RESULTS:
: ['firefox-esr.desktop', 'google-chrome.desktop', 'libreoffice-writer.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Software.desktop', 'yelp.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Settings.desktop', 'virt-manager.desktop', 'org.keepassxc.KeePassXC.desktop', 'xsane.desktop', 'org.pipewire.Helvum.desktop', 'org.gnome.Extensions.desktop', 'emacsclient.desktop', 'org.gnome.tweaks.desktop', 'blee3-doom-sys.desktop', 'kodi.desktop', 'org.gnome.Calculator.desktop']
        #+end_org """)


        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('favorite-apps').unpack()

        # if item in gvalues: gvalues.remove(item)
        # gschema.set_value('favorite-apps', GLib.Variant('as', gvalues))

        return cmndOutcome.set(opResults=gvalues,)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteApps_set" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteApps_set>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteApps_set(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i favoriteApps_set "['firefox-esr.desktop', 'google-chrome.desktop', 'org.gnome.Evolution.desktop', 'libreoffice-writer.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Software.desktop', 'yelp.desktop']"
#+end_src
#+RESULTS:
: ['firefox-esr.desktop', 'google-chrome.desktop', 'org.gnome.Evolution.desktop', 'libreoffice-writer.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Software.desktop', 'yelp.desktop']
        #+end_org """)

        favListArgs = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        favSetStr = favListArgs[0]

        return cmndOutcome.set(opResults=favSetStr,)

        # gschema = Gio.Settings('org.gnome.shell')

        # gschema.set_value('favorite-apps', GLib.Variant('as', gvalues))

        # return cmndOutcome.set(opResults=gvalues,)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="favListArgs",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteApps_remove" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteApps_remove>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteApps_remove(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i favoriteApps_remove "org.gnome.Settings.desktop"
#+end_src
#+RESULTS:
: org.gnome.Settings.desktop found will be removed.
: ['org.gnome.Settings.desktop']
        #+end_org """)

        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('favorite-apps').unpack()

        favNames = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        for each in favNames:
            if each in gvalues:
                print(f"{each} found will be removed.")
                gvalues.remove(each)
                gschema.set_value('favorite-apps', GLib.Variant('as', gvalues))
            else:
               print(f"{each} not found -- Nothing  removed.")

        return cmndOutcome.set(opResults=favNames,)



####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="favNames",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteApps_addAfter" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 2 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteApps_addAfter>>  =verify= argsMin=2 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteApps_addAfter(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 2, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i favoriteApps_set "[]"
#+end_src
#+RESULTS:
: [{'networking.primary': 'eno1'}, {'os.distro.id': 'Debian'}]
        #+end_org """)

        result = []

        factNames = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        for eachFactName in factNames:
            factValue = facter._getWithGetattr(eachFactName, cache=cache, fromFile=fromFile, fromData=fromData)
            result.append({eachFactName: factValue})

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="after",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        cmndArgsSpecDict.argsDictAdd(
            argPosition="1&9999",
            argName="favNames",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteApps_append" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteApps_append>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteApps_append(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i favoriteApps_append org.gnome.Calculator.qdesktop
#+end_src
#+RESULTS:
: org.gnome.Calculator.qdesktop Already in Favs, append skipped
: ['org.gnome.Calculator.qdesktop']
        #+end_org """)

        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('favorite-apps').unpack()

        favNames = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        for each in favNames:
            alreadyInFavs = False
            if each in gvalues:
                alreadyInFavs = True
                print(f"{each} Already in Favs, append skipped")

            if  alreadyInFavs == False:
                gvalues.append(each)
                gschema.set_value('favorite-apps', GLib.Variant('as', gvalues))
                print(f"{each} Appended to Favs")

        return cmndOutcome.set(opResults=favNames,)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="favNames",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Enabled Extensions -- Get, Set, Add, Remove" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Enabled Extensions -- Get, Set, Add, Remove_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "extensionsEnabled_get" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<extensionsEnabled_get>>  =verify= ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class extensionsEnabled_get(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns runFacterAndGetJsonOutputBytes.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i extensionsEnabled_get
#+end_src
#+RESULTS:
: ['dash-to-dock@micxgx.gmail.com', 'dash-to-panel@jderose9.github.com', 'gsconnect@andyholmes.github.io', 'workspace-indicator@gnome-shell-extensions.gcampax.github.com']
        #+end_org """)

        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('enabled-extensions').unpack()

        return cmndOutcome.set(opResults=gvalues,)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "extensionsEnabled_set" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<extensionsEnabled_set>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class extensionsEnabled_set(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i extensionsEnabled_set "[NOTYET]"
#+end_src
#+RESULTS:
: [NOTYET]
        #+end_org """)

        favListArgs = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        favSetStr = favListArgs[0]

        return cmndOutcome.set(opResults=favSetStr,)

        # gschema = Gio.Settings('org.gnome.shell')

        # gschema.set_value('enabled-extensions', GLib.Variant('as', gvalues))

        # return cmndOutcome.set(opResults=gvalues,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="favList",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "extensionsEnabled_remove" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<extensionsEnabled_remove>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class extensionsEnabled_remove(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i extensionsEnabled_remove 'NOTYET'
#+end_src
#+RESULTS:
: NOTYET not found -- Nothing  removed.
: ['NOTYET']
        #+end_org """)

        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('enabled-extensions').unpack()

        favNames = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        for each in favNames:
            if each in gvalues:
                print(f"{each} found will be removed.")
                gvalues.remove(each)
                gschema.set_value('enabled-extensions', GLib.Variant('as', gvalues))
            else:
               print(f"{each} not found -- Nothing  removed.")

        return cmndOutcome.set(opResults=favNames,)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="favNames",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "extensionsEnabled_add" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<extensionsEnabled_add>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class extensionsEnabled_add(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i extensionsEnabled_add NOTYET
#+end_src
#+RESULTS:
: NOTYET Appended to Extensions
: ['NOTYET']
        #+end_org """)

        gschema = Gio.Settings('org.gnome.shell')
        gvalues=gschema.get_value('enabled-extensions').unpack()

        extensionNames = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        for each in extensionNames:
            alreadyInFavs = False
            if each in gvalues:
                alreadyInFavs = True
                print(f"{each} Already in extensions, append skipped")

            if  alreadyInFavs == False:
                gvalues.append(each)
                gschema.set_value('enabled-extensions', GLib.Variant('as', gvalues))
                print(f"{each} Appended to Extensions")

        return cmndOutcome.set(opResults=extensionNames,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="extensionNames",
            argDefault='',
            argChoices=[],
            argDescription=""
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Gnome Tweaks" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Gnome Tweaks_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "general_overAmplification" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<general_overAmplification>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class general_overAmplification(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] diff obtained from gnome-tweaks
< org.gnome.desktop.sound allow-volume-above-100-percent false
---
> org.gnome.desktop.sound allow-volume-above-100-percent true

        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i general_overAmplification get
#+end_src
#+RESULTS:
: False
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i general_overAmplification false
#+end_src
#+RESULTS:
: False
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i general_overAmplification true
#+end_src
#+RESULTS:
: True

        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        cmnd = runArgs[0]

        gschema = Gio.Settings('org.gnome.desktop.sound')

        if cmnd == "get":
            pass
        elif cmnd == "true":
            gschema.set_value('allow-volume-above-100-percent', GLib.Variant('b', True))
        elif cmnd == "false":
            gschema.set_value('allow-volume-above-100-percent', GLib.Variant('b', False))
        else:
            print(f"Bad Usage: unsupported  cmnd={cmnd}")

        result=gschema.get_value('allow-volume-above-100-percent').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="cmnd",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "windowsTitlebars_minAndMax" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<windowsTitlebars_minAndMax>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class windowsTitlebars_minAndMax(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minAndMax get
#+end_src
#+RESULTS:
: appmenu:minimize,maximize,close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minAndMax off
#+end_src
#+RESULTS:
: appmenu:close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minAndMax on
#+end_src
#+RESULTS:
: appmenu:minimize,maximize,close

        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        cmnd = runArgs[0]

        gschema = Gio.Settings('org.gnome.desktop.wm.preferences')

        if cmnd == "get":
            pass
        elif cmnd == "on":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:minimize,maximize,close'))
        elif cmnd == "off":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:close'))
        else:
            print(f"Bad Usage: unsupported  cmnd={cmnd}")

        result=gschema.get_value('button-layout').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="cmnd",
            argDefault='',
            argChoices=[],
            argDescription=""
        )

        return cmndArgsSpecDict




####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "windowsTitlebars_maximize" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<windowsTitlebars_maximize>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class windowsTitlebars_maximize(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_maximize get
#+end_src
#+RESULTS:
: appmenu:minimize,maximize,close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_maximize off
#+end_src
#+RESULTS:
: appmenu:minimize,close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_maximize on
#+end_src
#+RESULTS:
: appmenu:minimize,maximize,close

        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        cmnd = runArgs[0]

        gschema = Gio.Settings('org.gnome.desktop.wm.preferences')

        if cmnd == "get":
            pass
        elif cmnd == "on":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:minimize,maximize,close'))
        elif cmnd == "off":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:minimize,close'))
        else:
            print(f"Bad Usage: unsupported  cmnd={cmnd}")

        result=gschema.get_value('button-layout').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="cmnd",
            argDefault='',
            argChoices=[],
            argDescription=""
        )

        return cmndArgsSpecDict


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "windowsTitlebars_minimize" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<windowsTitlebars_minimize>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class windowsTitlebars_minimize(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minimize get
#+end_src
#+RESULTS:
: appmenu:minimize,close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minimize off
#+end_src
#+RESULTS:
: appmenu:close
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i windowsTitlebars_minimize on
#+end_src
#+RESULTS:
: appmenu:minimize,close

        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        cmnd = runArgs[0]

        gschema = Gio.Settings('org.gnome.desktop.wm.preferences')

        if cmnd == "get":
            pass
        elif cmnd == "on":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:minimize,close'))
        elif cmnd == "off":
            gschema.set_value('button-layout', GLib.Variant('s', 'appmenu:close'))
        else:
            print(f"Bad Usage: unsupported  cmnd={cmnd}")

        result=gschema.get_value('button-layout').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="cmnd",
            argDefault='',
            argChoices=[],
            argDescription=""
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Customize Dash-to-Panel Extension" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Customize Dash-to-Panel Extension_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "dashToPanelCustomize" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<dashToPanelCustomize>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class dashToPanelCustomize(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Customize the dash-to-panel extension based on specification.
When spec=rawBisos --PanelInteliHide=enabled, panleLength=100%, The panel hides for maximized windows.

1917c1917
< org.gnome.shell.extensions.dash-to-panel animate-appicon-hover-animation-extent {'RIPPLE': 4, 'PLANK': 4}
---
> org.gnome.shell.extensions.dash-to-panel animate-appicon-hover-animation-extent {'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}
2023c2023
< org.gnome.shell.extensions.dash-to-panel intellihide false
---
> org.gnome.shell.extensions.dash-to-panel intellihide true
2025c2025
< org.gnome.shell.extensions.dash-to-panel intellihide-behaviour 'FOCUSED_WINDOWS'
---
> org.gnome.shell.extensions.dash-to-panel intellihide-behaviourintellihide-behaviour 'MAXIMIZED_WINDOWS'
2028c2028
< org.gnome.shell.extensions.dash-to-panel intellihide-hide-from-windows false
---
> org.gnome.shell.extensions.dash-to-panel intellihide-hide-from-windows true
2046c2046
< org.gnome.shell.extensions.dash-to-panel panel-anchors '{}'
---
> org.gnome.shell.extensions.dash-to-panel panel-anchors '{"0":"MIDDLE"}'
2051c2051
< org.gnome.shell.extensions.dash-to-panel panel-lengths '{}'animate-appicon-hover-animation-extent
---
> org.gnome.shell.extensions.dash-to-panel panel-lengths '{"0":100}'
2055c2055
< org.gnome.shell.extensions.dash-to-panel panel-sizes '{}'
---
> org.gnome.shell.extensions.dash-to-panel panel-sizes '{"0":48}'

        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i dashToPanelCustomize get
#+end_src
#+RESULTS:
: #77767B
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i dashToPanelCustomize rawBisos
#+end_src
#+RESULTS:
: #77767B
        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        spec = runArgs[0]

        gschema = Gio.Settings('org.gnome.shell.extensions.dash-to-panel')

        if spec == "get":
            pass

        elif spec == "rawBisos":
            gschema.set_value('animate-appicon-hover-animation-extent', GLib.Variant('a{si}', {'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}))
            gschema.set_value('intellihide', GLib.Variant('b', True))
            gschema.set_value('intellihide-behaviour', GLib.Variant('s', 'MAXIMIZED_WINDOWS'))
            gschema.set_value('intellihide-hide-from-windows', GLib.Variant('b', True))
            gschema.set_value('panel-anchors', GLib.Variant('s', '{"0":"MIDDLE"}'))
            gschema.set_value('panel-lengths', GLib.Variant('s', '{"0":100}'))
            gschema.set_value('panel-sizes', GLib.Variant('s', '{"0":48}'))

        else:
            print(f"Bad Usage: unsupported  background={background}")

        result=gschema.get_value('intellihide').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="backgroundColor",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict



####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Desktop Background" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Desktop Background_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "desktopBackground" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<desktopBackground>>  =verify= argsMin=1 argsMax=1 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class desktopBackground(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns factValue for specified factName. Uses the safe getattr to do so. See factName cmnd.

gsettings set org.gnome.desktop.background picture-uri ''
# Disable Dark Wallpaper Picture
gsettings set org.gnome.desktop.background picture-uri-dark ''
# Set Background Color
gsettings set org.gnome.desktop.background primary-color 'blue'
gsettings set org.gnome.desktop.background primary-color '#ddd'
gsettings set org.gnome.desktop.background primary-color 'rgb(255, 255, 255)'

> org.gnome.Settings last-panel 'background'
651,654c651,654
< org.gnome.desktop.background picture-uri 'file:///usr/share/images/desktop-base/desktop-background.xml'
< org.gnome.desktop.background picture-uri-dark 'file:///usr/share/backgrounds/gnome/adwaita-d.webp'
< org.gnome.desktop.background primary-color '#023c88'
< org.gnome.desktop.background secondary-color '#5789ca'
---


> org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/gnome/vnc-l.webp'
> org.gnome.desktop.background picture-uri-dark 'file:///usr/share/backgrounds/gnome/vnc-d.webp'
> org.gnome.desktop.background primary-color '#77767B'
> org.gnome.desktop.background secondary-color '#000000'
809,811c809,811
< org.gnome.desktop.screensaver picture-uri 'file:///usr/share/images/desktop-base/desktop-lockscreen.xml'
< org.gnome.desktop.screensaver primary-color '#023c88'
< org.gnome.desktop.screensaver secondary-color '#5789ca'
---
> org.gnome.desktop.screensaver picture-uri 'file:///usr/share/backgrounds/gnome/vnc-l.webp'
> org.gnome.desktop.screensaver primary-color '#77767B'
> org.gnome.desktop.screensaver secondary-color '#000000'


        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i desktopBackground get
#+end_src
#+RESULTS:
: #77767B
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i desktopBackground freshDebian
#+end_src
#+RESULTS:
: #023c88
#+begin_src sh :results output :session shared
  gnomeCustomize.cs -i desktopBackground rawBisos
#+end_src
#+RESULTS:
: #77767B
        #+end_org """)

        runArgs  = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)
        background = runArgs[0]

        gschema = Gio.Settings('org.gnome.desktop.background')

        if background == "get":
            pass
        
        elif background == "freshDebian":
            gschema.set_value('picture-uri', GLib.Variant('s', 'file:///usr/share/images/desktop-base/desktop-background.xml'))
            gschema.set_value('picture-uri-dark', GLib.Variant('s', 'file:///usr/share/backgrounds/gnome/adwaita-d.webp'))
            gschema.set_value('primary-color', GLib.Variant('s', '#023c88'))
            gschema.set_value('secondary-color', GLib.Variant('s', '#5789ca'))
            gschema = Gio.Settings('org.gnome.desktop.screensaver')
            gschema.set_value('picture-uri', GLib.Variant('s', 'file:///usr/share/images/desktop-base/desktop-background.xml'))
            gschema.set_value('primary-color', GLib.Variant('s', '#023c88'))
            gschema.set_value('secondary-color', GLib.Variant('s', '#5789ca'))

        elif background == "rawBisos":
            gschema.set_value('picture-uri', GLib.Variant('s', 'file:///usr/share/backgrounds/gnome/vnc-l.webp'))
            gschema.set_value('picture-uri-dark', GLib.Variant('s', 'file:///usr/share/backgrounds/gnome/vnc-d.webp'))
            gschema.set_value('primary-color', GLib.Variant('s', '#77767B'))
            gschema.set_value('secondary-color', GLib.Variant('s', '#023c88'))
            gschema = Gio.Settings('org.gnome.desktop.screensaver')
            gschema.set_value('picture-uri', GLib.Variant('s', 'file:///usr/share/backgrounds/gnome/vnc-l.webp'))
            gschema.set_value('primary-color', GLib.Variant('s', '#77767B'))
            gschema.set_value('secondary-color', GLib.Variant('s', '#023c88'))

        else:
            print(f"Bad Usage: unsupported  background={background}")


        result=gschema.get_value('primary-color').unpack()

        return cmndOutcome.set(opResults=result,)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="backgroundColor",
            argDefault='',
            argChoices=[],
            argDescription="One argument, any string for a factName"
        )

        return cmndArgsSpecDict




####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
