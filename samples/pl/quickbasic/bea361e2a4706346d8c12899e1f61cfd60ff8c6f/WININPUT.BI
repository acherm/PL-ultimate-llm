'**************************************************************
'*
'* Include File: WinInput
'*
'* Requires:     none
'*
'* Description:  Keyboard and mouse input stuff
'*
'*************************************************************

'** Keyboard and mouse input COMMON subsection 
DECLARE FUNCTION WinSetFocus%(BYVAL hwndDesktop AS LONG,_
                              BYVAL hwndSetFocus AS LONG)

DECLARE FUNCTION WinFocusChange%(BYVAL hwndDesktop AS LONG,_
                                 BYVAL hwndSetFocus AS LONG,_
                                 BYVAL fsFocusChange AS INTEGER)

CONST FCNOSETFOCUS              = &H0001
CONST FCNOLOSEFOCUS             = &H0002
CONST FCNOSETACTIVE             = &H0004
CONST FCNOLOSEACTIVE            = &H0008
CONST FCNOSETSELECTION          = &H0010
CONST FCNOLOSESELECTION         = &H0020

CONST QFCNEXTINCHAIN             = &H0001
CONST QFCACTIVE                  = &H0002
CONST QFCFRAME                   = &H0003
CONST QFCSELECTACTIVE            = &H0004

DECLARE FUNCTION WinSetCapture%(BYVAL hwndDesktop AS LONG,_
                                BYVAL hwnd AS LONG)

DECLARE FUNCTION WinQueryCapture&(BYVAL hwndDesktop AS LONG,_
                                  BYVAL fLock AS INTEGER)

' Mouse input messages 

CONST WMMOUSEFIRST       = &H0070
CONST WMMOUSELAST        = &H0079
CONST WMBUTTONCLICKFIRST = &H0071
CONST WMBUTTONCLICKLAST  = &H0079

CONST WMMOUSEMOVE        = &H0070

CONST WMBUTTON1DOWN      = &H0071

CONST WMBUTTON1UP        = &H0072
CONST WMBUTTON1DBLCLK    = &H0073
CONST WMBUTTON2DOWN      = &H0074
CONST WMBUTTON2UP        = &H0075
CONST WMBUTTON2DBLCLK    = &H0076
CONST WMBUTTON3DOWN      = &H0077
CONST WMBUTTON3UP        = &H0078
CONST WMBUTTON3DBLCLK    = &H0079

DECLARE FUNCTION WinQueryFocus&(BYVAL hwndDesktop AS LONG,_
                                BYVAL fLock AS INTEGER)

' Key/Character input msg     

CONST WMCHAR             = &H007a
CONST WMVIOCHAR          = &H007b

' WMCHAR fs field bits 

CONST KCCHAR             = &H0001
CONST KCVIRTUALKEY       = &H0002
CONST KCSCANCODE         = &H0004

CONST KCSHIFT            = &H0008
CONST KCCTRL             = &H0010
CONST KCALT              = &H0020
CONST KCKEYUP            = &H0040
CONST KCPREVDOWN         = &H0080
CONST KCLONEKEY          = &H0100
CONST KCDEADKEY          = &H0200
CONST KCCOMPOSITE        = &H0400
CONST KCINVALIDCOMP      = &H0800
CONST KCTOGGLE           = &H1000
CONST KCINVALIDCHAR      = &H2000
CONST KCDBCSRSRVD1	    = &H4000
CONST KCDBCSRSRVD2	    = &H8000

'
' * The following structure and macro are used to access the
' * WMMOUSEMOVE, and WMBUTTON* message parameters
' 
TYPE MOUSEMSG 
    codeHitTest AS INTEGER     ' mp2 
    unused AS INTEGER
    x AS INTEGER               ' mp1 
    y AS INTEGER
END TYPE

'
' * The following structure and macro are used to access the
' * WMCHAR message parameters.
' 
TYPE CHARMSG 
    chr AS INTEGER             ' mp2 
    vkey AS INTEGER
    fs AS INTEGER              ' mp1 
    cRepeat AS STRING *1
    scancode AS STRING *1
END TYPE

'** Virtual key values 

CONST VKBUTTON1      = &H01
CONST VKBUTTON2      = &H02
CONST VKBUTTON3      = &H03
CONST VKBREAK        = &H04
CONST VKBACKSPACE    = &H05
CONST VKTAB          = &H06
CONST VKBACKTAB      = &H07
CONST VKNEWLINE      = &H08
CONST VKSHIFT        = &H09
CONST VKCTRL         = &H0A
CONST VKALT          = &H0B
CONST VKALTGRAF      = &H0C
CONST VKPAUSE        = &H0D
CONST VKCAPSLOCK     = &H0E
CONST VKESC          = &H0F
CONST VKSPACE        = &H10
CONST VKPAGEUP       = &H11
CONST VKPAGEDOWN     = &H12
CONST VKEND          = &H13
CONST VKHOME         = &H14
CONST VKLEFT         = &H15
CONST VKUP           = &H16
CONST VKRIGHT        = &H17
CONST VKDOWN         = &H18
CONST VKPRINTSCRN    = &H19
CONST VKINSERT       = &H1A
CONST VKDELETE       = &H1B
CONST VKSCRLLOCK     = &H1C
CONST VKNUMLOCK      = &H1D
CONST VKENTER        = &H1E
CONST VKSYSRQ        = &H1F
CONST VKF1           = &H20
CONST VKF2           = &H21
CONST VKF3           = &H22
CONST VKF4           = &H23
CONST VKF5           = &H24
CONST VKF6           = &H25
CONST VKF7           = &H26
CONST VKF8           = &H27
CONST VKF9           = &H28
CONST VKF10          = &H29
CONST VKF11          = &H2A
CONST VKF12          = &H2B
CONST VKF13          = &H2C
CONST VKF14          = &H2D
CONST VKF15          = &H2E
CONST VKF16          = &H2F
CONST VKF17          = &H30
CONST VKF18          = &H31
CONST VKF19          = &H32
CONST VKF20          = &H33
CONST VKF21          = &H34
CONST VKF22          = &H35
CONST VKF23          = &H36
CONST VKF24          = &H37

DECLARE FUNCTION WinGetKeyState%(BYVAL hwndDesktop AS LONG,_
                                 BYVAL vkey AS INTEGER)

DECLARE FUNCTION WinGetPhysKeyState%(BYVAL hwndDesktop AS LONG,_
                                     BYVAL sc AS INTEGER)

DECLARE FUNCTION WinEnablePhysInput%(BYVAL hwndDesktop AS LONG,_
                                     BYVAL fEnable AS INTEGER)

DECLARE FUNCTION WinIsPhysInputEnabled%(BYVAL hwndDesktop AS LONG)

DECLARE FUNCTION WinSetKeyboardStateTable%(BYVAL hwndDesktop AS LONG,_
                                           BYVAL pKeyStateTable AS LONG,_
                                           BYVAL fSet AS INTEGER)

' Journal Notification messages  
CONST WMJOURNALNOTIFY    = &H007c

'** Define the valid commands (lParm1) for journal notify message 
CONST JRNQUEUESTATUS     = &H00000001
CONST JRNPHYSKEYSTATE    = &H00000002
