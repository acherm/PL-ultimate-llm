# bb-example .bb build file
# place this in your meta- layer folder under
# recipes/bb-example/bb-example.bb

DESCRIPTION = "bb-example code"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58"
DEPENDS = ""

SRC_URI = "git://github.com/kingcoyote/bb-example.git;protocol=git"
SRCREV = "master"
PR = "r0"
S="${WORKDIR}/git"

do_compile () {
make
}

do_install () {
install -d ${D}${bindir}
install -m 0755 bb-example ${D}${bindir}
}
