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
** This File: /bisos/git/bxRepos/bisos-pip/gnome/py3/bisos/gnome/gnomeBisos.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['gnomeBisos'], }
csInfo['version'] = '202408274257'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'gnomeBisos-Panel.org'
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

import collections

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] *Imports* =Based on Classification=cs-u=
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

from bisos.gnome import gnomeApi
from bisos.debian import configFile

from gi.repository import Gio,GLib

import pathlib
import datetime

####+BEGIN: b:py3:cs:orgItem/basic :type "=Executes=  "  :title "CSU-Lib Executions" :comment "-- cs.invOutcomeReportControl"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Executes=   [[elisp:(outline-show-subtree+toggle)][||]] CSU-Lib Executions -- cs.invOutcomeReportControl  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

g_rosmu = cs.G.icmMyName()

cs.invOutcomeReportControl(cmnd=True, ro=True)



####+BEGIN: bx:cs:py3:section :title "Exported Instances"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Exported Instances*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


# sysdUnitSiteReg = bifSystemd.UserUnit("siteReg")


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

        configFile.examples_csu(concreteConfigFile='gnomeBisosAutostart', sectionTitle="default")

        bcbArgs='''commonCaps'''

        cs.examples.menuChapter('=Customize Gnome for BISOS Capability Bundles=')
        cmnd('gnomeCustomizeForBCBs', args=bcbArgs)

        cs.examples.menuChapter('=BISOS Favorite Apps Commands=')
        cmnd('bisosFavoriteApps_list', args=bcbArgs)
        cmnd('favoriteAppsForBCBs', args=bcbArgs)

        cs.examples.menuChapter('=BISOS Enabled Extensions Commands=')
        cmnd('bisosEnabledExtensions_list', args=bcbArgs)
        cmnd('enabledExtensionsForBCBs', args=bcbArgs)

        cs.examples.menuChapter('=BISOS Gnome Tweaks Commands=')
        cmnd('gnomeTweaksForBCBs', args=bcbArgs)

        cs.examples.menuChapter('=BISOS Favorite Apps Commands=')
        cmnd('deskBackgroundForBCBs', args=bcbArgs)

        cs.examples.menuChapter('=Raw Command Examples=')

        literal("gnomeCustomize.cs")

        return(cmndOutcome)

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Customize Gnome for BISOS Capability Bundles" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Customize Gnome for BISOS Capability Bundles_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:func/typing :funcName "bcb_favoriteAppsList" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /bcb_favoriteAppsList/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def bcb_favoriteAppsList(
####+END:
        bcb: str,
) -> list[str]:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    commonFavoriteAppsList = [
        'org.gnome.Terminal.desktop',
        'org.gnome.Settings.desktop',
        'blee3-doom-sys.desktop'
    ]

    result = commonFavoriteAppsList

    if bcb == "commonBcb":
        result = commonFavoriteAppsList
    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

    return result


####+BEGIN: b:py3:cs:func/typing :funcName "bcb_enabledExtList" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /bcb_enabledExtList/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def bcb_enabledExtList(
####+END:
        bcb: str,
) -> list[str]:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    commonEnabledExtList = [
        'dash-to-panel@jderose9.github.com',
        'gsconnect@andyholmes.github.io',
        'workspace-indicator@gnome-shell-extensions.gcampax.github.com',
    ]

    result = commonEnabledExtList

    if bcb == "commonBcb":
        result = commonEnabledExtList
    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

    return result


####+BEGIN: b:py3:cs:func/typing :funcName "bcb_gnomeTweaks" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /bcb_gnomeTweaks/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def bcb_gnomeTweaks(
####+END:
        bcb: str,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    result = None

    if bcb == "commonBcb":

        results = gnomeApi.general_overAmplification().pyCmnd(
            argsList=['get'],
        ).results
        print(f"general_overAmplification -- get -- results={results}")

        results = gnomeApi.general_overAmplification().pyCmnd(
            argsList=['true'],
        ).results
        print(f"general_overAmplification -- true -- results={results}")

        results = gnomeApi.windowsTitlebars_minAndMax().pyCmnd(
            argsList=['get'],
        ).results
        print(f"windowsTitlebars_minAndMax -- get -- results={results}")

        results = gnomeApi.windowsTitlebars_minAndMax().pyCmnd(
            argsList=['on'],
        ).results
        print(f"windowsTitlebars_minAndMax -- on -- results={results}")

    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

    return result


####+BEGIN: b:py3:cs:func/typing :funcName "bcb_gnomeTweaksObsoleted" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /bcb_gnomeTweaksObsoleted/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def bcb_gnomeTweaksObsoleted(
####+END:
        bcb: str,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    result = None

    if bcb == "commonBcb":

        results = gnomeApi.general_overAmplification().pyCmnd(
            argsList=['get'],
        ).results
        print(f"general_overAmplification -- get -- results={results}")

        results = gnomeApi.general_overAmplification().pyCmnd(
            argsList=['true'],
        ).results
        print(f"general_overAmplification -- true -- results={results}")

        results = gnomeApi.windowsTitlebars_maximize().pyCmnd(
            argsList=['get'],
        ).results
        print(f"windowsTitlebars_maximize -- get -- results={results}")

        results = gnomeApi.windowsTitlebars_maximize().pyCmnd(
            argsList=['on'],
        ).results
        print(f"windowsTitlebars_maximize -- on -- results={results}")

        results = gnomeApi.windowsTitlebars_minimize().pyCmnd(
            argsList=['get'],
        ).results
        print(f"windowsTitlebars_miimize -- get -- results={results}")

        results = gnomeApi.windowsTitlebars_minimize().pyCmnd(
            argsList=['on'],
        ).results
        print(f"windowsTitlebars_minimize -- on -- results={results}")

    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

    return result

####+BEGIN: b:py3:cs:func/typing :funcName "bcb_desktopBackground" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /bcb_desktopBackground/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def bcb_desktopBackground(
####+END:
        bcb: str,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    result = None

    if bcb == "commonBcb":
        results = gnomeApi.desktopBackground().pyCmnd(
            argsList=['get'],
        ).results
        print(f"desktopBackground -- get (Pre)-- results={results}")

        results = gnomeApi.desktopBackground().pyCmnd(
            argsList=['rawBisos'],
        ).results
        print(f"desktopBackground -- set rawBisos -- results={results}")

    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

    return result


####+BEGIN: b:py3:cs:func/typing :funcName "gnomeCustomizeForBcb" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /gnomeCustomizeForBcb/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def gnomeCustomizeForBcb(
####+END:
        bcb: str,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    if bcb == "commonBcb":
        favApps = bcb_favoriteAppsList(bcb)
        print(f"processing commonBcb -- favApps={favApps}")
        enabledExt = bcb_enabledExtList(bcb)
        print(f"processing commonBcb -- enabled={enabledExt}")

        bcb_gnomeTweaks(bcb)
        bcb_desktopBackground(bcb)

    elif  bcb == "outerRimEnv":
        print("processing outerRimEnv")
    elif  bcb == "innerRimEnv":
        print("processing innerRimEnv")
    elif  bcb == "exposedRimEnv":
        print("processing exposedRimEnv")
    elif  bcb == "mediaCenter":
        print("processing mediaCenter")
    elif  bcb == "lcntProduction":
        print("processing lcntProduction")
    else:
        print(f"unknown bcb={bcb}")

####+BEGIN: b:py3:cs:func/typing :funcName "effectiveBcb" :funcType "Typed" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-Typed  [[elisp:(outline-show-subtree+toggle)][||]] /effectiveBcb/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def effectiveBcb(
####+END:
        bcbs: list[str],
) -> str:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
#+end_org """

    for eachBcb in bcbs:
        # Later we will process the list
        pass
    return "commonBcb"

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "gnomeAutostartPrep" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<gnomeAutostartPrep>>  =verify= ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class gnomeAutostartPrep(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             fromData: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Creates ~/.config/autostart and ~/.config/bisos/gnomeBisosCustomizationCompleted
        Repeats gnomeCustomizeForBCBs because otherwise it wont work.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeBisos.cs -i gnomeAutostartPrep
#+end_src
#+RESULTS:
: /bxo/usg/bystar/.config/bisos/gnomeBisosCustomizationCompleted
        #+end_org """)

        autostartDir = pathlib.Path.joinpath(pathlib.Path.home(), ".config/autostart")
        autostartDir.mkdir(parents=True, exist_ok=True)

        bisosAppsDir = pathlib.Path.joinpath(pathlib.Path.home(), ".config/bisos")
        bisosAppsDir.mkdir(parents=True, exist_ok=True)

        controlFile = pathlib.Path.joinpath(bisosAppsDir, "gnomeBisosCustomizationCompleted")

        return cmndOutcome.set(opResults=controlFile,)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "gnomeAutostartForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<gnomeAutostartForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class gnomeAutostartForBCBs(cs.Cmnd):
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
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Creates ~/.config/autostart and ~/.config/bisos/gnomeBisosCustomizationCompleted
        Repeats gnomeCustomizeForBCBs because otherwise it wont work.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  gnomeBisos.cs -i gnomeAutostartForBCBs commonBcb
#+end_src
#+RESULTS:
: 08/29/2024, 22:07:18
: Already Customized.
: 08/29/2024, 22:07:18
        #+end_org """)

        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        print(f"{timestamp}")

        controlFileStr = gnomeAutostartPrep().pyCmnd().results

        controlFile = pathlib.Path(controlFileStr)

        if not controlFile.is_file():
            for i in range(5):
                # Capture output in bisosAppsDir
                results = gnomeCustomizeForBCBs().pyCmnd(
                    argsList=argsList,
                ).results
            controlFile.touch()
        else:
            print(f"Already Customized.")

        return cmndOutcome.set(opResults=timestamp,)


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
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "gnomeCustomizeForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<gnomeCustomizeForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class gnomeCustomizeForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i gnomeCustomizeForBCBs commonBcb
#+end_src
#+RESULTS:
: general_overAmplification
: windowsTitlebars_maximize
: windowsTitlebars_minimize
: Desktop Background Color
: []
        #+end_org """)

        results = favoriteAppsForBCBs().pyCmnd(
            argsList=argsList,
        ).results

        results = enabledExtensionsForBCBs().pyCmnd(
            argsList=argsList,
        ).results

        results = gnomeTweaksForBCBs().pyCmnd(
            argsList=argsList,
        ).results

        results = dashToPanelCustomizeForBCBs().pyCmnd(
            argsList=argsList,
        ).results


        results = deskBackgroundForBCBs().pyCmnd(
            argsList=argsList,
        ).results

        result = []

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "BISOS Favorite Apps" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _BISOS Favorite Apps_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "bisosFavoriteApps_list" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<bisosFavoriteApps_list>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class bisosFavoriteApps_list(cs.Cmnd):
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
  gnomeBisos.cs -i favoriteAppsForBCBs commonBcb
#+end_src
#+RESULTS:
: ['org.gnome.Terminal.desktop', 'org.gnome.Settings.desktop', 'blee3-doom-sys.desktop']
        #+end_org """)

        result = []

        bcbs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        bcb = effectiveBcb(bcbs)

        result = bcb_favoriteAppsList(bcb)

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict




####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "favoriteAppsForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<favoriteAppsForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class favoriteAppsForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i favoriteAppsForBCBs commonBcb
#+end_src
#+RESULTS:
: org.gnome.Terminal.desktop Already in Favs, append skipped
: org.gnome.Settings.desktop Already in Favs, append skipped
: blee3-doom-sys.desktop Already in Favs, append skipped
: ['org.gnome.Terminal.desktop', 'org.gnome.Settings.desktop', 'blee3-doom-sys.desktop']
        #+end_org """)

        favsList = bisosFavoriteApps_list().pyCmnd(
            argsList=argsList,
        ).results

        results = gnomeApi.favoriteApps_append().pyCmnd(
            argsList=favsList,
        ).results

        return cmndOutcome.set(opResults=results,)


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
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "BISOS Enabled Extensions" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _BISOS Enabled Extensions_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "bisosEnabledExtensions_list" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<bisosEnabledExtensions_list>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class bisosEnabledExtensions_list(cs.Cmnd):
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
  gnomeBisos.cs -i bisosEnabledExtensions_list commonBcb
#+end_src
#+RESULTS:
: ['dash-to-panel@jderose9.github.com', 'gsconnect@andyholmes.github.io', 'workspace-indicator@gnome-shell-extensions.gcampax.github.com']
        #+end_org """)

        result = []

        bcbs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        bcb = effectiveBcb(bcbs)

        result = bcb_enabledExtList(bcb)

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "enabledExtensionsForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<enabledExtensionsForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class enabledExtensionsForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i  enabledExtensionsForBCBs commonBcb
#+end_src
#+RESULTS:
: Enabled Extenstions (Pre): ['dash-to-dock@micxgx.gmail.com', 'dash-to-panel@jderose9.github.com', 'gsconnect@andyholmes.github.io', 'workspace-indicator@gnome-shell-extensions.gcampax.github.com']
: dash-to-panel@jderose9.github.com Already in extensions, append skipped
: gsconnect@andyholmes.github.io Already in extensions, append skipped
: workspace-indicator@gnome-shell-extensions.gcampax.github.com Already in extensions, append skipped
: Enabled Extenstions (Post): ['dash-to-dock@micxgx.gmail.com', 'dash-to-panel@jderose9.github.com', 'gsconnect@andyholmes.github.io', 'workspace-indicator@gnome-shell-extensions.gcampax.github.com']
: ['dash-to-dock@micxgx.gmail.com', 'dash-to-panel@jderose9.github.com', 'gsconnect@andyholmes.github.io', 'workspace-indicator@gnome-shell-extensions.gcampax.github.com']
        #+end_org """)

        results  = gnomeApi.extensionsEnabled_get().pyCmnd(
        ).results
        print(f"Enabled Extenstions (Pre): {results}")

        extentionsList = bisosEnabledExtensions_list().pyCmnd(
            argsList=argsList,
        ).results

        results  = gnomeApi.extensionsEnabled_add().pyCmnd(
            argsList=extentionsList,
        ).results

        results  = gnomeApi.extensionsEnabled_get().pyCmnd(
        ).results
        print(f"Enabled Extenstions (Post): {results}")

        return cmndOutcome.set(opResults=results,)


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
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict



####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "BISOS Gnome Tweaks" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _BISOS Gnome Tweaks_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "gnomeTweaksForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<gnomeTweaksForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class gnomeTweaksForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i gnomeTweaksForBCBs commonBcb
#+end_src
#+RESULTS:
: general_overAmplification -- get -- results=True
: general_overAmplification -- true -- results=True
: windowsTitlebars_minAndMax -- get -- results=appmenu:minimize,maximize,close
: windowsTitlebars_minAndMax -- on -- results=appmenu:minimize,maximize,close
: []
        #+end_org """)

        result = []

        bcbs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        bcb = effectiveBcb(bcbs)

        bcb_gnomeTweaks(bcb)

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "dashToPanelCustomize" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _dashToPanelCustomize_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "dashToPanelCustomizeForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<dashToPanelCustomizeForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class dashToPanelCustomizeForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i dashToPanelCustomizeForBCBs commonBcb
#+end_src
#+RESULTS:
: dashToPanelCustomize -- get -- results=True
: dashToPanelCustomize -- rawBisos -- results=True
: []
        #+end_org """)

        result = []

        bcbs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        bcb = effectiveBcb(bcbs)

        if bcb == "commonBcb":

            results = gnomeApi.dashToPanelCustomize().pyCmnd(
                argsList=['get'],
            ).results
            print(f"dashToPanelCustomize -- get -- results={results}")

            results = gnomeApi.dashToPanelCustomize().pyCmnd(
                argsList=['rawBisos'],
            ).results
            print(f"dashToPanelCustomize -- rawBisos -- results={results}")

        elif  bcb == "outerRimEnv":
            print("processing outerRimEnv")
        elif  bcb == "innerRimEnv":
            print("processing innerRimEnv")
        elif  bcb == "exposedRimEnv":
            print("processing exposedRimEnv")
        elif  bcb == "mediaCenter":
            print("processing mediaCenter")
        elif  bcb == "lcntProduction":
            print("processing lcntProduction")
        else:
            print(f"unknown bcb={bcb}")

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "BISOS Desktop Background" :anchor ""  :extraInfo "CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _BISOS Desktop Background_: |]]  CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "deskBackgroundForBCBs" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "fromData"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<deskBackgroundForBCBs>>  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=fromData   [[elisp:(org-cycle)][| ]]
#+end_org """
class deskBackgroundForBCBs(cs.Cmnd):
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
  gnomeBisos.cs -i deskBackgroundForBCBs commonBcb
#+end_src
#+RESULTS:
: desktopBackground -- get (Pre)-- results=#77767B
: desktopBackground -- set rawBisos -- results=#77767B
: []
        #+end_org """)

        result = []

        bcbs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)
        bcb = effectiveBcb(bcbs)

        bcb_desktopBackground(bcb)

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
            argPosition="0&9999",
            argName="bcbs",
            argDefault='',
            argChoices=[],
            argDescription="List of BISOS Capability Bundels"
        )

        return cmndArgsSpecDict

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Classes" :anchor ""  :extraInfo "InMail_Control"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Classes_: |]]  InMail_Control  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:class/decl :className "ConfigFile_gnomeBisosAutostart" :superClass "configFile.ConfigFile" :comment "" :classType "basic"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-basic  [[elisp:(outline-show-subtree+toggle)][||]] /ConfigFile_gnomeBisosAutostart/  superClass=configFile.ConfigFile  [[elisp:(org-cycle)][| ]]
#+end_org """
class ConfigFile_gnomeBisosAutostart(configFile.ConfigFile):
####+END:
    """ #+begin_org
** [[elisp:(org-cycle)][| DocStr| ]]  InMail Service Access Instance Class for an Accessible Abstract Service.
    #+end_org """

####+BEGIN: b:py3:cs:method/typing :methodName "configFilePath" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /configFilePath/  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def configFilePath(
####+END:
            self,
    ) -> pathlib.Path:
        """ #+begin_org
*** [[elisp:(org-cycle)][| DocStr| ]]  Return path
        #+end_org """
        serviceFilePath = pathlib.Path.joinpath(pathlib.Path.home(), ".config/autostart/gnomeBisos.desktop")
        return serviceFilePath

####+BEGIN: b:py3:cs:method/typing :methodName "configFileStr" :methodType "" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /configFileStr/  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def configFileStr(
####+END
            self,
    ) -> str:
        """ #+begin_org
*** [[elisp:(org-cycle)][| DocStr| ]]  Returns string
        #+end_org """
        templateStr = """\
[Desktop Entry]
Name=gnomeBisos
GenericName=Customize Gnome BISOS Desktop
Comment=Depends on ~/.config/bisos
Exec=bash -c '/bisos/pipx/bin/gnomeBisos.cs  -i gnomeAutostartForBCBs commonCaps &>> $HOME/.config/bisos/gnomeAutostartForBCBs.log'
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true"""
        return templateStr


####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showallq### local variables:
### no-byte-compile: t
### end:
####+END:
