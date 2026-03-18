# SIM_STATUS

Parses an Adams message file (usually with an .msg extension), and returns an array of simulation status codes corresponding to the tag: ALVSIM:STATUS.

## Format
```
SIM_STATUS (fileName)
```

## Arguments

**fileName**
: Name of the file in which to look for simulation status codes.

## Returns

**0**
: NOERRS

**-101**
: INPERR

**-102**
: BADSIT

**-105**
: ERINPT

**-117**
: ERVRFY

**-118**
: ERMEMO

**-119**
: ERRVRS

**-120**
: ERRDIM

**-121**
: ERRLCK

**-122**
: BADMEM

**-123**
: BADAMD

**-124**
: ERRSML

**-125**
: NOTCXX

**-998**
: TERMNT

**-997**
: INPTRM

**-996**
: PRFLER

**-995**
: ERTERM

**-994**
: SNHALT

**-993**
: TRMRCR

**-200**
: QUITFL

**100**
: BADCMD
